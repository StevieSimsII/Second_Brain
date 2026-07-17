from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess

from ingest.github import _find_local_source, build_page_id
from ingest.lesson import render_markdown
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


if __name__ == "__main__":
    unittest.main()
