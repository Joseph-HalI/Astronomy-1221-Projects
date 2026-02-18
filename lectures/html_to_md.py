"""
Convert all HTML lecture files in this directory to Markdown using markdownify.
"""

import re
from pathlib import Path

from markdownify import markdownify as md
from bs4 import BeautifulSoup


def strip_header_footer(text: str) -> str:
    """Remove nav links at start and footer + MathJax script at end."""
    # Remove "[Coding Essentials for Astronomers](...)\n[Back to overview](...)" and following blank lines
    text = re.sub(
        r"^\[Coding Essentials for Astronomers\]\([^)]+\)\s*\[Back to overview\]\([^)]+\)\s*\n+",
        "",
        text,
    )
    # Remove "Part of the Coding Essentials..." and everything after (footer + MathJax script)
    text = re.sub(
        r"\n+\s*Part of the Coding Essentials for Astronomers lecture series\.\s*\n+.*$",
        "",
        text,
        flags=re.DOTALL,
    )
    return text.strip() + "\n"


def html_to_markdown(html_path: Path, output_path: Path | None = None) -> None:
    """Convert one HTML file to Markdown. Writes to output_path or same name with .md."""
    html_path = Path(html_path)
    output_path = output_path or html_path.with_suffix(".md")

    html_text = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_text, "html.parser")

    # Convert only the body to avoid head/scripts/styles in the markdown
    body = soup.find("body")
    if body is None:
        content = html_text
    else:
        # Remove in-page anchor links (e.g. "[¶](#heading-id)") from headings
        for a in body.find_all("a", href=True):
            if a["href"].startswith("#"):
                a.decompose()
        # Remove all images (avoids base64 blobs and external image refs in markdown)
        for img in body.find_all("img"):
            img.decompose()
        content = str(body)

    markdown_text = md(
        content,
        heading_style="ATX",  # # style headers
        strip=["script", "style"],
    )
    markdown_text = strip_header_footer(markdown_text)

    output_path.write_text(markdown_text, encoding="utf-8")
    print(f"Wrote {output_path.name}")


def main():
    folder = Path(__file__).resolve().parent
    for html_file in sorted(folder.glob("*.html")):
        html_to_markdown(html_file)


if __name__ == "__main__":
    main()
