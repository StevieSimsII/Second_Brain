from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ingest.codex import ensure_chatgpt_auth, run_codex_structured
from ingest.github import _find_local_source, build_page_id
from ingest.lesson import generate_lesson, render_markdown
from ingest.sources import FetchedSource, SourceQualityError, validate_source
from ingest.urls import normalize_url, source_fingerprint, youtube_video_id
from ingest.youtube import fetch_transcript


class UrlTests(unittest.TestCase):
    def test_youtube_variants_have_one_identity(self) -> None:
        shared = "https://youtu.be/abc123?si=tracking"
        watch = "https://www.youtube.com/watch?v=abc123&utm_source=test"
        self.assertEqual(normalize_url(shared), "https://www.youtube.com/watch?v=abc123")
        self.assertEqual(source_fingerprint(shared), source_fingerprint(watch))
        self.assertEqual(youtube_video_id(watch), "abc123")

    def test_generic_tracking_is_removed_but_meaningful_query_remains(self) -> None:
        url = "https://Example.com/article/?id=42&utm_medium=social#comments"
        self.assertEqual(normalize_url(url), "https://example.com/article?id=42")


class SourceQualityTests(unittest.TestCase):
    def test_thin_youtube_capture_is_rejected(self) -> None:
        source = FetchedSource(
            url="https://www.youtube.com/watch?v=abc123",
            kind="youtube",
            content="video page stub",
        )
        with self.assertRaises(SourceQualityError):
            validate_source(source)

    @patch("ingest.youtube.subprocess.run")
    def test_transcript_worker_has_a_hard_timeout(self, run) -> None:
        run.side_effect = subprocess.TimeoutExpired(cmd="youtube", timeout=5)
        with self.assertRaises(TimeoutError):
            fetch_transcript("abc123", timeout=5)


class MarkdownTests(unittest.TestCase):
    def test_rendered_page_keeps_evidence_metadata(self) -> None:
        source = FetchedSource(
            url="https://example.com/article",
            kind="web",
            content="x" * 2000,
        )
        lesson = {
            "title": 'A "Quoted" Lesson',
            "tags": ["AI Agents", "retrieval"],
            "overview": "Overview text.",
            "key_concepts": [{"name": "Grounding", "explanation": "Use evidence."}],
            "how_it_works": "Mechanics.",
            "training_exercise": "Try it.",
            "further_reading": [],
        }
        markdown = render_markdown(
            lesson, source=source, date="2026-07-16", fingerprint="abc123def0"
        )
        self.assertIn('title: "A \\"Quoted\\" Lesson"', markdown)
        self.assertIn('source_type: "web"', markdown)
        self.assertIn('source_fingerprint: "abc123def0"', markdown)
        self.assertIn("tags: [ai-agents, retrieval]", markdown)
        self.assertIn("## Key Concepts", markdown)

    def test_page_id_is_stable_and_contains_fingerprint(self) -> None:
        page_id = build_page_id("A Useful Lesson", "abc123def0", "2026-07-16")
        self.assertEqual(page_id, "2026-07-16-a-useful-lesson-abc123def0")

    def test_legacy_source_is_found_without_regeneration(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            pages = root / "wiki" / "pages"
            pages.mkdir(parents=True)
            page = pages / "2026-01-01-existing.md"
            page.write_text(
                '---\ntitle: "Existing"\nsource: "https://example.com/post?utm_source=x"\n---\nBody',
                encoding="utf-8",
            )
            with patch("ingest.github.config.REPO_ROOT", root):
                result = _find_local_source("https://example.com/post")
            self.assertIsNotNone(result)
            self.assertTrue(result.duplicate)
            self.assertEqual(result.page_id, "2026-01-01-existing")


class CodexAuthTests(unittest.TestCase):
    def test_chatgpt_auth_requires_tokens(self) -> None:
        with TemporaryDirectory() as directory:
            home = Path(directory)
            auth = home / "auth.json"
            auth.write_text('{"auth_mode":"api"}', encoding="utf-8")
            with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
                with self.assertRaises(RuntimeError):
                    ensure_chatgpt_auth()

    def test_chatgpt_auth_accepts_plan_tokens(self) -> None:
        with TemporaryDirectory() as directory:
            home = Path(directory)
            auth = home / "auth.json"
            auth.write_text(
                json.dumps(
                    {
                        "auth_mode": "chatgpt",
                        "tokens": {
                            "access_token": "access",
                            "refresh_token": "refresh",
                        },
                    }
                ),
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
                self.assertEqual(ensure_chatgpt_auth(), auth)

    @patch("ingest.codex.subprocess.run")
    @patch("ingest.codex.resolve_codex_bin", return_value="/usr/local/bin/codex")
    def test_structured_exec_uses_schema_and_stdin(self, _bin, run) -> None:
        lesson = {
            "title": "From Codex",
            "tags": ["codex"],
            "overview": "Overview",
            "key_concepts": [{"name": "Auth", "explanation": "ChatGPT plan"}],
            "how_it_works": "How",
            "training_exercise": "Try",
            "further_reading": [],
        }

        def fake_run(command, input, capture_output, text, timeout, check):
            self.assertEqual(command[0], "/usr/local/bin/codex")
            self.assertIn("exec", command)
            self.assertIn("--output-schema", command)
            self.assertIn("-o", command)
            self.assertEqual(command[-1], "-")
            self.assertIn("BEGIN SOURCE", input)
            output_flag = command.index("-o")
            Path(command[output_flag + 1]).write_text(
                json.dumps(lesson), encoding="utf-8"
            )
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        run.side_effect = fake_run
        with TemporaryDirectory() as directory:
            home = Path(directory)
            (home / "auth.json").write_text(
                json.dumps(
                    {
                        "auth_mode": "chatgpt",
                        "tokens": {
                            "access_token": "access",
                            "refresh_token": "refresh",
                        },
                    }
                ),
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
                result = run_codex_structured(
                    "prompt with --- BEGIN SOURCE ---",
                    schema={"type": "object"},
                    model="gpt-5.4",
                    timeout=30,
                )
        self.assertEqual(result["title"], "From Codex")

    @patch("ingest.lesson.run_codex_structured")
    def test_generate_lesson_uses_codex(self, run_codex) -> None:
        run_codex.return_value = {
            "title": "Lesson",
            "tags": ["agents"],
            "overview": "Overview",
            "key_concepts": [{"name": "A", "explanation": "B"}],
            "how_it_works": "How",
            "training_exercise": "Do",
            "further_reading": [],
        }
        source = FetchedSource(
            url="https://example.com/post",
            kind="web",
            content="x" * 2000,
        )
        lesson = generate_lesson(source)
        self.assertEqual(lesson["title"], "Lesson")
        self.assertTrue(run_codex.called)
        prompt = run_codex.call_args.args[0]
        self.assertIn(source.url, prompt)
        self.assertIn("BEGIN SOURCE", prompt)


if __name__ == "__main__":
    unittest.main()
