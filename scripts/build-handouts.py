#!/usr/bin/env python3
"""Validate developer aides and build the 2-page printable PDF handout.

Single source of truth:
  - skills/*/SKILL.md (YAML frontmatter: live catalog and auto-trigger flags)
  - docs/quick-reference.md (command descriptions and groupings)
  - docs/assets/architecture-overview.svg (overview diagram)
  - scripts/handout-template.html (print layout)
  - plugin.json (version metadata)
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
QUICK_REF_MD = REPO_ROOT / "docs" / "quick-reference.md"
OVERVIEW_SVG = REPO_ROOT / "docs" / "assets" / "architecture-overview.svg"
TEMPLATE_HTML = REPO_ROOT / "scripts" / "handout-template.html"
PDF_OUT = REPO_ROOT / "docs" / "handouts" / "agent-skills-handout.pdf"
PLUGIN_JSON = REPO_ROOT / "plugin.json"

LINK_CHECK_DOCS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "docs" / "overview.md",
    REPO_ROOT / "docs" / "quick-reference.md",
    REPO_ROOT / "docs" / "harness.md",
    REPO_ROOT / "docs" / "validation.md",
    REPO_ROOT / "skills" / "develop" / "SKILL.md",
    REPO_ROOT / "skills" / "develop" / "references" / "config-and-subagents.md",
]
LEFT_GROUP_TITLES = {"Understand", "Frame and design"}
EXPECTED_PDF_PAGES = 2
STALE_PATTERN = re.compile(
    r"poteto-mode|poteto-agent|comment-sicko|pstack-models|cursor-team-kit|"
    r"/deslop|no-comments|control-ui|control-cli|principle-|\.cursor/plugins|"
    r"claude-opus-5-5|claude-fable-5-2"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_skill_catalog() -> list[dict]:
    """Read skill name, description presence, and invocation mode from skills/*/SKILL.md."""
    skills: list[dict] = []
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        lines = read_text(skill_md).splitlines()
        if len(lines) < 3 or lines[0].strip() != "---":
            raise ValueError(f"Missing YAML frontmatter in {skill_md}")
        close_idx = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), -1)
        if close_idx < 2:
            raise ValueError(f"Unclosed YAML frontmatter in {skill_md}")
        fm = "\n".join(lines[1:close_idx])
        name_m = re.search(r"(?m)^name:[ \t]*(\S+)[ \t]*$", fm)
        if not name_m or name_m.group(1) != skill_dir.name:
            raise ValueError(f"Frontmatter name mismatch in {skill_md}")
        if not re.search(r"(?m)^description:[ \t]*\S", fm):
            raise ValueError(f"Missing or blank description in {skill_md}")
        manual_only = bool(re.search(r"(?m)^disable-model-invocation:[ \t]*true[ \t]*$", fm))
        skills.append({"name": skill_dir.name, "manual_only": manual_only})
    return skills


def find_stale_references() -> list[str]:
    targets = list(SKILLS_DIR.rglob("*.md")) + [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "docs" / "harness.md",
        REPO_ROOT / "docs" / "overview.md",
        REPO_ROOT / "docs" / "quick-reference.md",
    ]
    hits: list[str] = []
    for path in targets:
        if not path.is_file():
            continue
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            if STALE_PATTERN.search(line):
                hits.append(f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}")
    return hits


def parse_tables_by_heading(md_text: str) -> dict[str, list[list[str]]]:
    """Map each H2 or H3 heading to the data rows of its Markdown table."""
    tables: dict[str, list[list[str]]] = {}
    heading = ""
    raw_lines: list[str] = []

    def flush() -> None:
        if heading and len(raw_lines) >= 3:
            tables[heading] = [
                [c.strip() for c in ln.strip("|").split("|")] for ln in raw_lines[2:]
            ]

    for line in md_text.splitlines():
        m = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if m:
            flush()
            heading = m.group(1)
            raw_lines = []
        elif line.strip().startswith("|"):
            raw_lines.append(line.strip())
    flush()
    return tables


def strip_code(text: str) -> str:
    return re.sub(r"`([^`]+)`", r"\1", text).strip()


def format_inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def format_tags(raw: str) -> str:
    tags = [strip_code(part) for part in raw.split(",") if part.strip()]
    out: list[str] = []
    for tag in tags:
        cls = "tag"
        if tag == "auto":
            cls += " tag-auto"
        elif tag == "pauses":
            cls += " tag-pauses"
        out.append(f'<span class="{cls}">{html.escape(tag)}</span>')
    return "".join(out)


def validate_svg(path: Path) -> str:
    svg_text = read_text(path)
    root = ET.fromstring(svg_text)
    if not root.tag.endswith("svg"):
        raise ValueError(f"Expected <svg> root in {path}")
    return svg_text


def validate_links(ignore: set[Path] | None = None) -> list[str]:
    ignored = {p.resolve() for p in (ignore or set())}
    broken: list[str] = []
    for doc in LINK_CHECK_DOCS:
        if not doc.is_file():
            continue
        body = re.sub(r"```.*?```", "", read_text(doc), flags=re.DOTALL)
        for m in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", body):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            rel = unquote(target.split("#", 1)[0])
            if not rel:
                continue
            resolved = (doc.parent / rel).resolve()
            if resolved not in ignored and not resolved.exists():
                broken.append(f"{doc.relative_to(REPO_ROOT)} -> {target}")
    return broken


def compute_fingerprint(skills: list[dict], quick_ref: str, svg: str, template: str, version: str) -> str:
    h = hashlib.sha256()
    h.update(json.dumps({"skills": skills, "version": version}, sort_keys=True).encode("utf-8"))
    for chunk in (quick_ref, svg, template):
        h.update(chunk.replace("\r\n", "\n").encode("utf-8"))
    return h.hexdigest()[:12]


def inspect_pdf(path: Path) -> tuple[int, str | None]:
    """Return ``(page_count, embedded_rev_fingerprint)`` from a PDF file."""
    data = path.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise ValueError(f"Invalid PDF header: {path}")
    counts = [
        int(m.group(1))
        for m in re.finditer(rb"/Type\s*/Pages\b[^<>]*?/Count\s+(\d+)", data, re.DOTALL)
    ]
    leaf = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", data))
    pages = max(counts) if counts else leaf
    if counts and leaf and pages != leaf:
        raise ValueError(f"PDF page count mismatch: /Count={pages}, /Page={leaf}")
    rev_m = re.search(rb"/Title\s*\([^)]*\[rev ([0-9a-f]{12})\][^)]*\)", data)
    return pages, rev_m.group(1).decode("ascii") if rev_m else None


def load_and_validate(check_pdf: bool) -> dict:
    skills = load_skill_catalog()
    quick_ref_text = read_text(QUICK_REF_MD)
    svg_text = validate_svg(OVERVIEW_SVG)
    template_text = read_text(TEMPLATE_HTML)
    version = json.loads(read_text(PLUGIN_JSON)).get("version", "")

    tables = parse_tables_by_heading(quick_ref_text)
    everyday_key = next((k for k in tables if k.startswith("Everyday")), None)
    if not everyday_key:
        raise ValueError("Missing '## Everyday ...' table in docs/quick-reference.md")
    everyday_rows = tables[everyday_key]
    group_tables = {
        k: v for k, v in tables.items() if k != everyday_key and not k.startswith("Settings")
    }

    doc_cmds: list[str] = []
    for row in everyday_rows:
        doc_cmds.append(strip_code(row[0]).lstrip("/"))
    for rows in group_tables.values():
        for row in rows:
            doc_cmds.append(strip_code(row[0]).lstrip("/"))

    live_names = [s["name"] for s in skills]
    if len(doc_cmds) != len(set(doc_cmds)):
        raise ValueError("Duplicate commands in docs/quick-reference.md")
    missing = sorted(set(live_names) - set(doc_cmds))
    extra = sorted(set(doc_cmds) - set(live_names))
    if missing or extra:
        raise ValueError(f"Skill mismatch vs docs/quick-reference.md (missing={missing}, extra={extra})")

    broken = validate_links(ignore=set() if check_pdf else {PDF_OUT})
    if broken:
        raise ValueError("Broken Markdown links:\n  " + "\n  ".join(broken))
    stale = find_stale_references()
    if stale:
        raise ValueError("Stale upstream or retired references:\n  " + "\n  ".join(stale))

    fingerprint = compute_fingerprint(skills, quick_ref_text, svg_text, template_text, version)
    if check_pdf:
        if not PDF_OUT.is_file():
            raise ValueError(f"Missing PDF: {PDF_OUT.relative_to(REPO_ROOT)}")
        pages, pdf_rev = inspect_pdf(PDF_OUT)
        if pages != EXPECTED_PDF_PAGES:
            raise ValueError(f"Expected {EXPECTED_PDF_PAGES} PDF pages, found {pages}")
        if pdf_rev != fingerprint:
            raise ValueError(
                f"PDF handout is stale (expected rev {fingerprint}, found {pdf_rev}). "
                "Run: python scripts/build-handouts.py"
            )

    return {
        "skills": skills,
        "everyday_rows": everyday_rows,
        "group_tables": group_tables,
        "svg": svg_text,
        "template": template_text,
        "version": f"v{version}" if version else "",
        "fingerprint": fingerprint,
    }


def render_html(data: dict) -> str:
    skills = data["skills"]
    manual_count = sum(1 for s in skills if s["manual_only"])
    auto_names = [f"/{s['name']}" for s in skills if not s["manual_only"]]
    auto_summary = (
        f"{len(auto_names)} auto (<code>{', '.join(auto_names)}</code>)" if auto_names else "0 auto"
    )

    ev_html = []
    for cmd_raw, use_raw, input_raw in data["everyday_rows"]:
        tag_m = re.search(r"\(([^)]*(?:`(?:diff|pauses|subagents|auto)`)[^)]*)\)\s*$", input_raw)
        if tag_m:
            lead = input_raw[: tag_m.start()].strip()
            input_cell = f"{format_inline(lead)} {format_tags(tag_m.group(1))}".strip()
        else:
            input_cell = format_inline(input_raw)
        ev_html.append(
            "<tr>"
            f'<td class="ev-cmd"><code>{html.escape(strip_code(cmd_raw))}</code></td>'
            f'<td class="ev-use">{format_inline(use_raw)}</td>'
            f'<td class="ev-in">{input_cell}</td>'
            "</tr>"
        )

    left_html: list[str] = []
    right_html: list[str] = []
    for group_name, rows in data["group_tables"].items():
        items = []
        for cmd_raw, use_raw, tags_raw in rows:
            cmd = html.escape(strip_code(cmd_raw))
            tags = format_tags(tags_raw)
            items.append(
                f'<div class="cmd-item"><span class="cmd-name">{cmd}</span> '
                f"{format_inline(use_raw)}{tags}</div>"
            )
        block = (
            f'<div class="group-box">'
            f'<div class="group-head">{html.escape(group_name)}</div>'
            f'{"".join(items)}</div>'
        )
        (left_html if group_name in LEFT_GROUP_TITLES else right_html).append(block)

    replacements = {
        "{{FINGERPRINT}}": data["fingerprint"],
        "{{VERSION}}": html.escape(data["version"]),
        "{{SVG}}": data["svg"],
        "{{TOTAL_SKILLS}}": str(len(skills)),
        "{{MANUAL_COUNT}}": str(manual_count),
        "{{AUTO_SUMMARY}}": auto_summary,
        "{{EVERYDAY_ROWS}}": "".join(ev_html),
        "{{OTHER_COUNT}}": str(len(skills) - len(data["everyday_rows"])),
        "{{LEFT_GROUPS}}": "".join(left_html),
        "{{RIGHT_GROUPS}}": "".join(right_html),
    }
    out = data["template"]
    for token, value in replacements.items():
        out = out.replace(token, value)
    return out


def find_browser(explicit: str | None) -> Path | None:
    candidates = [c for c in (explicit, os.environ.get("HANDOUT_BROWSER")) if c]
    for name in ("chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    candidates.extend([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ])
    return next((Path(p) for p in candidates if Path(p).is_file()), None)


def render_pdf(browser: Path, html_path: Path, pdf_out: Path) -> None:
    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="handout-chrome-") as profile_dir:
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--allow-file-access-from-files",
            f"--user-data-dir={profile_dir}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_out.resolve()}",
            html_path.resolve().as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode != 0 or not pdf_out.is_file():
            raise RuntimeError(f"Browser PDF render failed (rc={res.returncode}): {res.stderr.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate aides and build the 2-page PDF handout.")
    parser.add_argument("--check", action="store_true", help="Verify parity, links, SVG, and fresh 2-page PDF.")
    parser.add_argument("--browser", help="Path to Chrome, Edge, or Chromium binary.")
    parser.add_argument("--html-out", type=Path, help="Optional path to save rendered HTML for manual print.")
    args = parser.parse_args()

    try:
        data = load_and_validate(check_pdf=args.check)
        if args.check:
            n = len(data["skills"])
            print(f"OK: skills={n}/{n} | svg=valid | links=ok | pdf=2 pages (rev {data['fingerprint']})")
            return 0

        rendered = render_html(data)
        if args.html_out:
            args.html_out.parent.mkdir(parents=True, exist_ok=True)
            args.html_out.write_text(rendered, encoding="utf-8")

        browser = find_browser(args.browser)
        if not browser:
            print(
                "ERROR: Chrome, Edge, or Chromium not found. Pass --browser <path> or --html-out <file>.",
                file=sys.stderr,
            )
            return 1

        with tempfile.TemporaryDirectory(prefix="handout-html-") as tmpdir:
            html_path = args.html_out if args.html_out else Path(tmpdir) / "handout.html"
            if not args.html_out:
                html_path.write_text(rendered, encoding="utf-8")
            render_pdf(browser, html_path, PDF_OUT)

        pages, rev = inspect_pdf(PDF_OUT)
        if pages != EXPECTED_PDF_PAGES or rev != data["fingerprint"]:
            raise RuntimeError(f"Unexpected PDF output: pages={pages}, rev={rev}")

        n = len(data["skills"])
        print(
            f"Built {PDF_OUT.relative_to(REPO_ROOT)} ({pages} pages, {PDF_OUT.stat().st_size:,} bytes, "
            f"rev {rev}) via {browser.name} | skills={n}/{n}"
        )
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
