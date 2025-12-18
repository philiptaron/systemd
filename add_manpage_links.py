#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.pyyaml

"""
Add reference-style man page links to release notes.

This script:
1. Finds systemd tools mentioned in the release notes
2. Converts them to reference-style links like [`tool`][tool]
3. Adds reference link definitions at the bottom
"""

import re
import sys
from pathlib import Path


def load_manpages(version: str) -> dict[str, str]:
    """Load available man pages and return a mapping of name -> URL."""
    manpages = {}
    base_url = f"https://www.freedesktop.org/software/systemd/man/{version}"
    manpage_dir = Path(f"_data/manpages/v{version}")

    if not manpage_dir.exists():
        print(f"Warning: {manpage_dir} not found")
        return manpages

    for category in manpage_dir.iterdir():
        if category.is_dir():
            for f in category.glob("*.yaml"):
                name = f.stem
                # Determine the HTML filename
                if name.endswith(".service"):
                    html_name = f"{name}.html"
                else:
                    html_name = f"{name}.html"
                manpages[name] = f"{base_url}/{html_name}"

    return manpages


def find_systemd_tools(text: str) -> set[str]:
    """Find systemd tools mentioned in the text."""
    # Match patterns like:
    # - systemd-foo (plain text)
    # - `systemd-foo` (backticked)
    # - systemd-foo's (possessive)
    patterns = [
        r'\bsystemd-[\w-]+',
        r'\b(?:systemctl|journalctl|loginctl|machinectl|hostnamectl|localectl|timedatectl|networkctl|resolvectl|bootctl|busctl|coredumpctl|homectl|importctl|oomctl|portablectl|userdbctl|varlinkctl|udevadm|run0)\b',
        r'\bpam_systemd(?:_\w+)?\b',
        r'\bnss-(?:systemd|resolve|myhostname|mymachines)\b',
        r'\bsd-[\w-]+\b',
    ]

    tools = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            # Clean up possessives and strip backticks
            clean = m.strip('`')
            if clean.endswith("'s"):
                clean = clean[:-2]
            tools.add(clean)

    return tools


def process_release_notes(content: str, manpages: dict[str, str], version: str) -> str:
    """Process release notes to add reference-style links."""

    # Find all tools mentioned
    tools_found = find_systemd_tools(content)

    # Filter to only tools we have man pages for
    linkable_tools = {}
    for tool in tools_found:
        if tool in manpages:
            linkable_tools[tool] = manpages[tool]
        # Try with .service suffix for daemons
        elif f"{tool}.service" in manpages:
            linkable_tools[tool] = manpages[f"{tool}.service"]
        # Try removing .service suffix
        elif tool.endswith(".service") and tool[:-8] in manpages:
            linkable_tools[tool] = manpages[tool[:-8]]

    # Sort by length (longest first) to avoid partial replacements
    tools_sorted = sorted(linkable_tools.keys(), key=len, reverse=True)

    # Track which tools we actually link
    used_links = {}

    for tool in tools_sorted:
        # Skip if already linked (check for reference-style link)
        if f"[{tool}]" in content:
            continue

        # First, link any backticked occurrences: `tool` -> [`tool`][tool]
        pattern = rf'(?<!\[)`{re.escape(tool)}`(?!\])'
        new_content, count = re.subn(pattern, rf'[`{tool}`][{tool}]', content, count=1)
        if count > 0:
            content = new_content
            used_links[tool] = linkable_tools[tool]
            continue

        # Then, link plain text occurrences (word boundaries, not followed by .socket etc)
        # Use word boundary but check not already in markdown link syntax
        pattern = rf'(?<![`\[])\b{re.escape(tool)}\b(?![`\].\w])'
        new_content, count = re.subn(pattern, rf'[`{tool}`][{tool}]', content, count=1)
        if count > 0:
            content = new_content
            used_links[tool] = linkable_tools[tool]

    # Check for existing reference links
    existing_refs = set(re.findall(r'^\[([^\]]+)\]:', content, re.MULTILINE))

    # Add reference link definitions at the bottom
    if used_links:
        # Remove existing reference section if present
        content = re.sub(r'\n\[[\w-]+\]: https://www\.freedesktop\.org/software/systemd/man/.*$', '', content, flags=re.MULTILINE)

        # Add new references
        ref_lines = []
        for tool in sorted(used_links.keys()):
            if tool not in existing_refs:
                ref_lines.append(f"[{tool}]: {used_links[tool]}")

        if ref_lines:
            # Ensure we end with newlines before refs
            content = content.rstrip() + "\n\n" + "\n".join(ref_lines) + "\n"

    return content


def main():
    if len(sys.argv) < 2:
        print("Usage: add_manpage_links.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    release_notes_path = Path(f"systemd-{version}/release-notes.md")

    if not release_notes_path.exists():
        print(f"Error: {release_notes_path} not found")
        sys.exit(1)

    # Load man pages
    manpages = load_manpages(version)
    print(f"Loaded {len(manpages)} man pages for v{version}")

    # Read release notes
    content = release_notes_path.read_text()

    # Process
    new_content = process_release_notes(content, manpages, version)

    # Write back
    release_notes_path.write_text(new_content)
    print(f"Updated {release_notes_path}")


if __name__ == "__main__":
    main()
