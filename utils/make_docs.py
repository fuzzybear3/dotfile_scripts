#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path.cwd()

TEMPLATE = SCRIPT_DIR / "Manual.html5"

PANDOC_HTML = [
    "-f", "gfm+alerts", "--standalone", "--embed-resources",
    f"--template={TEMPLATE}", "--toc"
]
PANDOC_HTML_PLAIN = [
    "-f", "gfm+alerts", "--standalone", "--embed-resources"
]
PANDOC_PDF = [
    "--pdf-engine=xelatex", "-V", "mainfont=Noto Sans CJK JP"
]

FORMATS = ["html", "html-plain", "pdf", "pdf-dark"]

def build(src: Path, fmt: str):
    out_dir = PROJECT_ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    ext = ".pdf" if fmt.startswith("pdf") else ".html"
    out = out_dir / f"{src.stem}{ext}"

    if fmt == "html":
        cmd = ["pandoc", *PANDOC_HTML, str(src), "-o", str(out)]
    elif fmt == "html-plain":
        cmd = ["pandoc", *PANDOC_HTML_PLAIN, str(src), "-o", str(out)]
    elif fmt == "pdf":
        cmd = ["pandoc", str(src), "-o", str(out), *PANDOC_PDF]
    elif fmt == "pdf-dark":
        dark_tex = SCRIPT_DIR / "dark.tex"
        cmd = ["pandoc", str(src), "-o", str(out), *PANDOC_PDF, "-H", str(dark_tex)]
    else:
        print(f"Unknown format: {fmt}")
        sys.exit(1)

    print(f"Building {fmt}: {src} → {out}")
    subprocess.run(cmd, check=True)
    print(f"Done: {out}\n")

def usage():
    print("""Usage: make-docs <file.md> [format]
       make-docs all [format]

Arguments:
  file.md   Markdown file to convert, or 'all' to process every .md in CWD

Formats:
  html        HTML with template and TOC (default)
  html-plain  HTML without template
  pdf         PDF via xelatex with CJK font support
  pdf-dark    PDF with dark theme (requires dark.tex)

Examples:
  make-docs freecad_manual.md
  make-docs freecad_manual.md pdf
  make-docs all html
  make-docs all pdf-dark""")

args = sys.argv[1:]
if not args or args[0] in ("-h", "--help"):
    usage()
    sys.exit(0 if args else 1)

fmt = args[1] if len(args) > 1 else "html"

if args[0] == "all":
    for f in sorted(PROJECT_ROOT.glob("*.md")):
        build(f, fmt)
elif Path(args[0]).exists():
    build(Path(args[0]), fmt)
else:
    print(f"File not found: {args[0]}")
    usage()
    sys.exit(1)
