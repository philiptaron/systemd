#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.requests python3Packages.beautifulsoup4

"""
Fetch and parse systemd man page index to create data files.

This script downloads the man page index from freedesktop.org and creates
YAML data files for each man page, organized by type/section.

Usage:
    ./fetch_manpages.py 258
    ./fetch_manpages.py 259

Output:
    Creates _data/manpages/vXXX/ with subdirectories:
    - command/     (section 1 - user commands)
    - function/    (section 3 - library functions)
    - configuration/ (section 5 - config files)
    - concept/     (section 7 - overviews)
    - daemon/      (section 8 - system services)
"""

import argparse
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Map section numbers to directory names
SECTION_MAP = {
    "1": "command",
    "3": "function",
    "5": "configuration",
    "7": "concept",
    "8": "daemon",
}


def fetch_manpage_index(version: str) -> str:
    """Fetch the man page index HTML."""
    url = f"https://www.freedesktop.org/software/systemd/man/{version}/"
    print(f"Fetching index from {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def parse_manpage_index(html: str, version: str) -> list[dict]:
    """Parse the man page index HTML to extract page info."""
    soup = BeautifulSoup(html, "html.parser")

    manpages = []
    seen = set()  # Track seen names to avoid duplicates

    # Find all citerefentry spans - format:
    # <a href="name.html#"><span class="citerefentry">
    #   <span class="refentrytitle">name</span>(section)
    # </span></a> — Description
    for citeref in soup.find_all("span", class_="citerefentry"):
        # Get the parent link
        link = citeref.find_parent("a")
        if not link:
            continue

        href = link.get("href", "")
        # Remove the # anchor if present
        href = href.split("#")[0]
        if not href.endswith(".html"):
            continue

        # Get name from refentrytitle span
        title_span = citeref.find("span", class_="refentrytitle")
        if not title_span:
            continue

        name = title_span.get_text().strip()

        # Get section from the text after the title span
        # Format: "name(section)"
        full_text = citeref.get_text()
        match = re.search(r"\((\d+)\)$", full_text)
        if not match:
            continue

        section = match.group(1)

        # Skip duplicates (same name appears multiple times)
        key = f"{name}_{section}"
        if key in seen:
            continue
        seen.add(key)

        # Get description - it follows the link as text node
        # The structure is: <a>...</a> — Description<br>
        description = ""
        sibling = link.next_sibling
        if sibling and isinstance(sibling, str):
            desc_text = sibling.strip()
            # Remove em dash prefix using regex (handles encoding variations)
            desc_text = re.sub(r"^[\s\u2014\u2013\-—â]+", "", desc_text).strip()
            description = desc_text

        # Build full URL
        url = f"https://www.freedesktop.org/software/systemd/man/{version}/{href}"

        manpages.append({
            "name": name,
            "section": section,
            "description": description,
            "url": url,
        })

    return manpages


def create_data_files(manpages: list[dict], version: str, output_dir: Path):
    """Create YAML data files for each man page."""
    # Create directory structure
    for section_name in SECTION_MAP.values():
        (output_dir / section_name).mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0

    for page in manpages:
        section = page["section"]
        section_name = SECTION_MAP.get(section)

        if not section_name:
            # Unknown section, skip
            skipped += 1
            continue

        # Create YAML file
        filename = f"{page['name']}.yaml"
        filepath = output_dir / section_name / filename

        # Write YAML content (simple format, no library needed)
        content = f"description: {page['description']}\n"
        content += f"url: {page['url']}\n"

        with open(filepath, "w") as f:
            f.write(content)

        created += 1

    return created, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and parse systemd man page index"
    )
    parser.add_argument(
        "version",
        help="systemd version number (e.g., 258, 259)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: _data/manpages/vVERSION)",
    )
    args = parser.parse_args()

    version = args.version

    # Set up output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f"_data/manpages/v{version}")

    print(f"Fetching man pages for systemd v{version}")
    print(f"Output directory: {output_dir}")
    print()

    # Step 1: Fetch the index
    html = fetch_manpage_index(version)

    # Step 2: Parse the index
    manpages = parse_manpage_index(html, version)
    print(f"Found {len(manpages)} man pages")

    # Count by section
    sections = {}
    for page in manpages:
        sec = page["section"]
        sections[sec] = sections.get(sec, 0) + 1

    print("By section:")
    for sec, count in sorted(sections.items()):
        name = SECTION_MAP.get(sec, "other")
        print(f"  Section {sec} ({name}): {count}")
    print()

    # Step 3: Create data files
    created, skipped = create_data_files(manpages, version, output_dir)

    print(f"Created {created} data files")
    if skipped:
        print(f"Skipped {skipped} (unknown sections)")

    print(f"\nDone! Data saved to {output_dir}")


if __name__ == "__main__":
    main()
