"""
Build a static HTML second-brain site from wiki/pages/*.md.
Output goes to the Second_Brain repo as a single index.html
that can be hosted on GitHub Pages.

Usage:
    python build_site.py
    python build_site.py --out C:/path/to/output/index.html
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
WIKI_PAGES = HERE / "wiki" / "pages"
DEFAULT_OUT = HERE / "index.html"


# ── Frontmatter parser ────────────────────────────────────────────────────────

def _parse_page(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")

    # Split frontmatter from body
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not fm_match:
        body = text.strip()
        fm_raw, body = "", body
    else:
        fm_raw, body = fm_match.group(1), fm_match.group(2).strip()

    def _fm(key: str, default: str = "") -> str:
        m = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', fm_raw, re.MULTILINE)
        return m.group(1).strip() if m else default

    def _fm_tags() -> list[str]:
        m = re.search(r'^tags:\s*\[([^\]]*)\]', fm_raw, re.MULTILINE)
        if not m:
            return []
        return [t.strip().strip('"').strip("'") for t in m.group(1).split(",") if t.strip()]

    title = _fm("title") or path.stem
    date  = _fm("date")
    source = _fm("source")
    tags  = _fm_tags()

    if not body:
        return None

    # If frontmatter source is "personal notes", try to pull the real URL out of
    # the ## Personal Notes section (e.g. "Source: https://...") before stripping it.
    if source in ("personal notes", ""):
        url_match = re.search(
            r"## Personal Notes\b.*?(?:^Source:\s*)(https?://[^\s\n]+)",
            body, re.DOTALL | re.MULTILINE,
        )
        if url_match:
            source = url_match.group(1).strip()

    # Strip the ## Personal Notes section (contains raw email body / Notion links)
    body = re.sub(r"\n## Personal Notes\b.*?(?=\n## |\Z)", "", body, flags=re.DOTALL).strip()

    return {
        "id":     path.stem,
        "title":  title,
        "date":   date,
        "tags":   tags,
        "source": source,
        "content": body,
    }


# ── HTML template ─────────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Stevie's Second Brain</title>
<script src="https://cdn.jsdelivr.net/npm/marked@9/marked.min.js"></script>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #0d1117;
    --sidebar:   #161b22;
    --border:    #30363d;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --accent:    #58a6ff;
    --accent2:   #3fb950;
    --card-bg:   #161b22;
    --card-hover:#1f2937;
    --tag-bg:    #21262d;
    --code-bg:   #1c2128;
    --sidebar-w: 340px;
  }

  html, body { height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); font-size: 15px; line-height: 1.6; }

  /* ── Layout ── */
  .app { display: flex; height: 100vh; overflow: hidden; }

  /* ── Sidebar ── */
  .sidebar { width: var(--sidebar-w); min-width: var(--sidebar-w); background: var(--sidebar); border-right: 1px solid var(--border); display: flex; flex-direction: column; overflow: hidden; }

  .sidebar-header { padding: 20px 16px 12px; border-bottom: 1px solid var(--border); }
  .sidebar-header h1 { font-size: 16px; font-weight: 600; color: var(--text); letter-spacing: 0.3px; }
  .sidebar-header .count { font-size: 12px; color: var(--muted); margin-top: 2px; }

  .search-wrap { padding: 12px 16px; border-bottom: 1px solid var(--border); }
  .search-wrap input {
    width: 100%; background: var(--bg); border: 1px solid var(--border);
    border-radius: 6px; color: var(--text); padding: 7px 12px; font-size: 13px;
    outline: none; transition: border-color .15s;
  }
  .search-wrap input:focus { border-color: var(--accent); }
  .search-wrap input::placeholder { color: var(--muted); }

  .tags-wrap { padding: 10px 16px; border-bottom: 1px solid var(--border); display: flex; flex-wrap: wrap; gap: 6px; max-height: 90px; overflow-y: auto; }
  .tag-pill {
    background: var(--tag-bg); color: var(--muted); border: 1px solid var(--border);
    border-radius: 20px; padding: 2px 10px; font-size: 11px; cursor: pointer;
    transition: all .15s; user-select: none; white-space: nowrap;
  }
  .tag-pill:hover { border-color: var(--accent); color: var(--accent); }
  .tag-pill.active { background: var(--accent); color: #0d1117; border-color: var(--accent); font-weight: 600; }

  .article-list { flex: 1; overflow-y: auto; padding: 8px 0; }
  .article-list::-webkit-scrollbar { width: 4px; }
  .article-list::-webkit-scrollbar-track { background: transparent; }
  .article-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  .article-card {
    padding: 12px 16px; cursor: pointer; border-left: 3px solid transparent;
    transition: background .12s, border-color .12s;
  }
  .article-card:hover { background: var(--card-hover); }
  .article-card.active { border-left-color: var(--accent); background: var(--card-hover); }
  .article-card .card-title { font-size: 13px; font-weight: 500; color: var(--text); line-height: 1.4; margin-bottom: 4px; }
  .article-card .card-meta { font-size: 11px; color: var(--muted); display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .article-card .card-tags { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 5px; }
  .article-card .card-tag { background: var(--tag-bg); color: var(--muted); border-radius: 3px; padding: 1px 6px; font-size: 10px; }

  .no-results { padding: 24px 16px; color: var(--muted); font-size: 13px; text-align: center; }

  /* ── Main content ── */
  .main { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .main::-webkit-scrollbar { width: 6px; }
  .main::-webkit-scrollbar-track { background: transparent; }
  .main::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  .welcome { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--muted); gap: 12px; padding: 40px; text-align: center; }
  .welcome .big { font-size: 48px; }
  .welcome h2 { font-size: 20px; color: var(--text); }
  .welcome p { font-size: 14px; max-width: 360px; }

  .article-view { padding: 40px 48px; max-width: 820px; width: 100%; }

  .article-view .art-header { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
  .article-view .art-title { font-size: 26px; font-weight: 700; color: var(--text); line-height: 1.3; margin-bottom: 10px; }
  .article-view .art-source { margin-bottom: 8px; }
  .article-view .art-source a { color: var(--accent); text-decoration: none; font-size: 13px; }
  .article-view .art-source a:hover { text-decoration: underline; }
  .article-view .art-meta { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; font-size: 13px; color: var(--muted); }
  .art-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
  .art-tag { background: var(--tag-bg); color: var(--accent); border: 1px solid var(--border); border-radius: 20px; padding: 2px 10px; font-size: 12px; cursor: pointer; }
  .art-tag:hover { background: var(--accent); color: #0d1117; }

  /* ── Markdown styles ── */
  .md-body h1, .md-body h2, .md-body h3, .md-body h4 { color: var(--text); margin: 1.5em 0 .6em; line-height: 1.3; }
  .md-body h1 { font-size: 22px; } .md-body h2 { font-size: 18px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
  .md-body h3 { font-size: 16px; } .md-body h4 { font-size: 14px; color: var(--muted); }
  .md-body p { margin: .8em 0; color: var(--text); }
  .md-body a { color: var(--accent); text-decoration: none; }
  .md-body a:hover { text-decoration: underline; }
  .md-body ul, .md-body ol { margin: .8em 0 .8em 1.4em; }
  .md-body li { margin: .3em 0; }
  .md-body strong { color: var(--text); font-weight: 600; }
  .md-body em { color: var(--muted); font-style: italic; }
  .md-body code { background: var(--code-bg); border: 1px solid var(--border); border-radius: 4px; padding: 1px 6px; font-size: 13px; font-family: "SFMono-Regular", Consolas, monospace; color: #f0883e; }
  .md-body pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; overflow-x: auto; margin: 1em 0; }
  .md-body pre code { background: none; border: none; padding: 0; color: var(--text); font-size: 13px; }
  .md-body blockquote { border-left: 3px solid var(--accent); margin: 1em 0; padding: 4px 16px; color: var(--muted); background: var(--code-bg); border-radius: 0 6px 6px 0; }
  .md-body table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 14px; }
  .md-body th, .md-body td { border: 1px solid var(--border); padding: 8px 12px; }
  .md-body th { background: var(--code-bg); font-weight: 600; }
  .md-body hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }

  /* ── Sidebar footer ── */
  .sidebar-footer { padding: 12px 16px; border-top: 1px solid var(--border); font-size: 12px; color: var(--muted); display: flex; flex-direction: column; gap: 4px; }
  .sidebar-footer a { color: var(--muted); text-decoration: none; display: flex; align-items: center; gap: 6px; transition: color .15s; }
  .sidebar-footer a:hover { color: var(--accent); }

  /* ── Responsive ── */
  @media (max-width: 768px) {
    .app { flex-direction: column; }
    .sidebar { width: 100%; min-width: unset; max-height: 50vh; border-right: none; border-bottom: 1px solid var(--border); }
    .article-view { padding: 24px 20px; }
  }
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>&#129504; Stevie's Second Brain</h1>
      <div class="count" id="count"></div>
    </div>
    <div class="search-wrap">
      <input id="search" type="text" placeholder="Search articles..." autocomplete="off"/>
    </div>
    <div class="tags-wrap" id="tags"></div>
    <div class="article-list" id="list"></div>
    <div class="sidebar-footer">
      <a href="https://github.com/StevieSimsII/Second_Brain" target="_blank" rel="noopener">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        View on GitHub
      </a>
      <a href="https://github.com/StevieSimsII/Second_Brain#readme" target="_blank" rel="noopener">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M0 1.75A.75.75 0 01.75 1h4.253c1.227 0 2.317.59 3 1.501A3.744 3.744 0 0111.006 1h4.245a.75.75 0 01.75.75v10.5a.75.75 0 01-.75.75h-4.507a2.25 2.25 0 00-1.591.659l-.622.621a.75.75 0 01-1.06 0l-.622-.621A2.25 2.25 0 005.258 13H.75a.75.75 0 01-.75-.75V1.75zm7.25 10.032V3.5a2.25 2.25 0 012.25-2.25h3.5v9H11.5a3.75 3.75 0 00-2.25.75v-.468zM6.5 12.032V11.25A3.75 3.75 0 004.253 10.5H1.5V2.5h3.5A2.25 2.25 0 017.25 4.75v8.282a.25.25 0 01-.75 0z"/></svg>
        Setup Guide / README
      </a>
    </div>
  </aside>
  <main class="main" id="main">
    <div class="welcome">
      <div class="big">&#129504;</div>
      <h2>Stevie's Second Brain</h2>
      <p>Select an article from the sidebar to start reading.</p>
    </div>
  </main>
</div>

<script>
const ARTICLES = __ARTICLES_JSON__;

// ── State ─────────────────────────────────────────────────────────────────────
let activeId     = null;
let activeTag    = null;
let searchQuery  = "";

// ── Tag index ─────────────────────────────────────────────────────────────────
const tagCounts = {};
ARTICLES.forEach(a => (a.tags || []).forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; }));
const allTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).map(e => e[0]);

// ── Render tags ───────────────────────────────────────────────────────────────
function renderTags() {
  const wrap = document.getElementById("tags");
  wrap.innerHTML = allTags.map(t =>
    `<span class="tag-pill${activeTag === t ? " active" : ""}" data-tag="${t}">${t}</span>`
  ).join("");
  wrap.querySelectorAll(".tag-pill").forEach(el => el.addEventListener("click", () => {
    activeTag = activeTag === el.dataset.tag ? null : el.dataset.tag;
    renderTags(); renderList();
  }));
}

// ── Filter articles ───────────────────────────────────────────────────────────
function filtered() {
  const q = searchQuery.toLowerCase();
  return ARTICLES.filter(a => {
    if (activeTag && !(a.tags || []).includes(activeTag)) return false;
    if (q && !a.title.toLowerCase().includes(q) && !a.content.toLowerCase().includes(q)) return false;
    return true;
  });
}

// ── Render list ───────────────────────────────────────────────────────────────
function renderList() {
  const list = document.getElementById("list");
  const items = filtered();
  document.getElementById("count").textContent = `${items.length} of ${ARTICLES.length} articles`;
  if (!items.length) { list.innerHTML = `<div class="no-results">No articles found</div>`; return; }
  list.innerHTML = items.map(a => `
    <div class="article-card${a.id === activeId ? " active" : ""}" data-id="${a.id}">
      <div class="card-title">${escHtml(a.title)}</div>
      <div class="card-meta">
        <span>${a.date || ""}</span>
      </div>
      ${a.tags && a.tags.length ? `<div class="card-tags">${a.tags.map(t => `<span class="card-tag">${t}</span>`).join("")}</div>` : ""}
    </div>`).join("");
  list.querySelectorAll(".article-card").forEach(el => el.addEventListener("click", () => openArticle(el.dataset.id)));
}

// ── Open article ──────────────────────────────────────────────────────────────
function openArticle(id) {
  const a = ARTICLES.find(x => x.id === id);
  if (!a) return;
  activeId = id;
  renderList();

  const sourceHtml = a.source && a.source !== "personal notes"
    ? `<div class="art-source"><a href="${escHtml(a.source)}" target="_blank" rel="noopener">↗ ${escHtml(a.source)}</a></div>`
    : "";

  const tagsHtml = (a.tags || []).map(t =>
    `<span class="art-tag" data-tag="${t}">${t}</span>`
  ).join("");

  const bodyHtml = marked.parse(a.content || "");

  document.getElementById("main").innerHTML = `
    <div class="article-view">
      <div class="art-header">
        <div class="art-title">${escHtml(a.title)}</div>
        ${sourceHtml}
        <div class="art-meta">
          <span>${a.date || ""}</span>
        </div>
        ${tagsHtml ? `<div class="art-tags">${tagsHtml}</div>` : ""}
      </div>
      <div class="md-body">${bodyHtml}</div>
    </div>`;

  document.getElementById("main").querySelectorAll(".art-tag").forEach(el =>
    el.addEventListener("click", () => {
      activeTag = activeTag === el.dataset.tag ? null : el.dataset.tag;
      renderTags(); renderList();
    })
  );

  window.location.hash = id;
  document.getElementById("main").scrollTop = 0;
}

// ── Search ────────────────────────────────────────────────────────────────────
document.getElementById("search").addEventListener("input", e => {
  searchQuery = e.target.value;
  renderList();
});

// ── Helpers ───────────────────────────────────────────────────────────────────
function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

// ── Init ──────────────────────────────────────────────────────────────────────
renderTags();
renderList();

// Open article from URL hash on load
const hash = window.location.hash.slice(1);
if (hash && ARTICLES.find(a => a.id === hash)) openArticle(hash);
</script>
</body>
</html>
"""


# ── Build ─────────────────────────────────────────────────────────────────────

def build(out_path: Path) -> None:
    if not WIKI_PAGES.exists():
        log.error("Wiki pages directory not found: %s", WIKI_PAGES)
        return

    md_files = sorted(WIKI_PAGES.glob("*.md"), key=lambda p: p.name)
    md_files = [f for f in md_files if f.name != ".gitkeep"]

    articles = []
    for path in md_files:
        page = _parse_page(path)
        if page:
            articles.append(page)

    # Sort newest first
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)

    log.info("Loaded %d articles from %s", len(articles), WIKI_PAGES)

    articles_json = json.dumps(articles, ensure_ascii=False, indent=2)
    html = HTML_TEMPLATE.replace("__ARTICLES_JSON__", articles_json)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    log.info("Built: %s  (%d KB)", out_path, out_path.stat().st_size // 1024)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build second brain static site.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help=f"Output path (default: {DEFAULT_OUT})")
    args = parser.parse_args()
    build(args.out)


if __name__ == "__main__":
    main()
