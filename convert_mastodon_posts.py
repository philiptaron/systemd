#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.requests python3Packages.beautifulsoup4

"""
Convert downloaded Mastodon posts to markdown files.

This script reads the raw JSON posts downloaded by fetch_mastodon_posts.py
and converts them to markdown files suitable for Jekyll.

Usage:
    ./convert_mastodon_posts.py 258
    ./convert_mastodon_posts.py 259

Or with nix-shell explicitly:
    nix-shell -p python3 python3Packages.beautifulsoup4 --run 'python3 convert_mastodon_posts.py 258'

Output:
    Creates systemd-XXX/posts/NN-slug.md files for each numbered post
"""

import argparse
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup


def html_to_markdown(html_content: str) -> str:
    """Convert HTML content from Mastodon to markdown."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Process links
    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text()

        # Handle hashtags
        if "hashtag" in a.get("class", []):
            # Keep hashtag links
            a.replace_with(f"[{text}]({href})")
        # Handle mentions
        elif "mention" in a.get("class", []):
            a.replace_with(f"[{text}]({href})")
        # Handle invisible spans (Mastodon truncates long URLs visually)
        elif a.find("span", class_="invisible"):
            # Get the full URL from href
            a.replace_with(f"<{href}>")
        else:
            # Regular link
            if text == href or text.startswith("http"):
                a.replace_with(f"<{href}>")
            else:
                a.replace_with(f"[{text}]({href})")

    # Process line breaks
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Process paragraphs
    for p in soup.find_all("p"):
        p.insert_after("\n\n")
        p.unwrap()

    # Get text and clean up
    text = soup.get_text()

    # Decode HTML entities
    text = html.unescape(text)

    # Clean up excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    return text


def extract_post_number(content: str) -> int | None:
    """Extract the post number from content like '1️⃣ Here's the 1st post...'"""
    # Look for emoji number patterns
    emoji_numbers = {
        "1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5,
        "6️⃣": 6, "7️⃣": 7, "8️⃣": 8, "9️⃣": 9, "0️⃣": 0,
    }

    # Check for combined emoji numbers like "1️⃣0️⃣" for 10
    numbers = []
    i = 0
    while i < len(content):
        for emoji, num in emoji_numbers.items():
            if content[i:].startswith(emoji):
                numbers.append(num)
                i += len(emoji)
                break
        else:
            if numbers:
                break
            i += 1

    if numbers:
        result = 0
        for n in numbers:
            result = result * 10 + n
        return result

    return None


def generate_slug(content: str, post_number: int | None) -> str:
    """Generate a URL-friendly slug from post content."""
    # Extract key topics from the content
    content_lower = content.lower()

    # Common topic patterns to look for
    topics = {
        "credentials": "credentials",
        "tpm": "tpm",
        "varlink": "varlink",
        "nspawn": "nspawn",
        "vmspawn": "vmspawn",
        "homed": "homed",
        "homectl": "homed",
        "repart": "repart",
        "networkd": "networkd",
        "resolved": "resolved",
        "udev": "udev",
        "journal": "journal",
        "boot": "boot",
        "stub": "stub",
        "uki": "uki",
        "cryptenroll": "cryptenroll",
        "factory reset": "factory-reset",
        "dissect": "dissect",
        "mount": "mount",
        "socket": "socket",
        "timer": "timer",
        "slice": "slice",
        "cgroup": "cgroup",
        "namespace": "namespace",
        "bpf": "bpf",
        "quota": "quota",
        "logind": "logind",
        "machined": "machined",
        "importd": "importd",
        "sysext": "sysext",
        "confext": "confext",
        "portable": "portable",
        "run0": "run0",
        "analyze": "analyze",
        "coredump": "coredump",
        "oomd": "oomd",
        "firstboot": "firstboot",
        "hostnamed": "hostnamed",
        "hostname": "hostname",
        "ask-password": "ask-password",
        "ssh": "ssh",
        "vsock": "vsock",
        "delegate": "delegate",
        "user namespace": "userns",
        "foreign uid": "foreign-uid",
        "pid1": "pid1",
        "service manager": "service-manager",
    }

    for keyword, slug in topics.items():
        if keyword in content_lower:
            return slug

    # Fallback to generic slug
    return "feature"


def format_date(iso_date: str) -> str:
    """Format ISO date to YYYY-MM-DD."""
    return iso_date[:10]


def convert_post_to_markdown(
    post: dict,
    context: dict,
    post_number: int | None,
    version: str,
) -> str:
    """Convert a post and its context to markdown format."""
    content = html_to_markdown(post.get("content", ""))
    created_at = format_date(post["created_at"])
    url = post["url"]

    # Build the markdown
    lines = []

    # Front matter
    if post_number:
        title = f"systemd {version} Feature Highlight #{post_number}"
    else:
        title = f"systemd {version} Discussion"

    lines.append("---")
    lines.append("layout: post")
    lines.append(f"title: \"{title}\"")
    lines.append(f"date: {created_at}")
    lines.append(f"source: {url}")
    lines.append("author: Lennart Poettering")
    lines.append("---")
    lines.append("")

    # Main content
    lines.append(content)
    lines.append("")

    # Add Lennart's thread continuation (followups)
    followups = context.get("lennart_followups", [])
    if followups:
        # Sort by date
        followups.sort(key=lambda x: x["created_at"])

        lines.append("## Thread Continuation")
        lines.append("")

        for followup in followups:
            followup_content = html_to_markdown(followup.get("content", ""))
            followup_date = format_date(followup["created_at"])
            followup_url = followup["url"]

            lines.append(f"*{followup_date}* ([source]({followup_url}))")
            lines.append("")
            lines.append(followup_content)
            lines.append("")

    # Add notable replies with Lennart's responses
    replies = context.get("replies", [])
    lennart_followups_ids = {f["in_reply_to_id"] for f in followups}

    # Find replies that Lennart responded to
    replied_to = []
    for reply in replies:
        if reply["id"] in lennart_followups_ids:
            # Find Lennart's response to this reply
            responses = [f for f in followups if f.get("in_reply_to_id") == reply["id"]]
            if responses:
                replied_to.append((reply, responses))

    if replied_to:
        lines.append("## Q&A")
        lines.append("")

        for reply, responses in replied_to:
            reply_author = reply["account"]["display_name"] or reply["account"]["username"]
            reply_handle = f"@{reply['account']['acct']}"
            reply_content = html_to_markdown(reply.get("content", ""))
            reply_url = reply["url"]

            lines.append(f"> **[{reply_handle}]({reply_url}):** {reply_content}")
            lines.append("")

            for response in responses:
                response_content = html_to_markdown(response.get("content", ""))
                lines.append(response_content)
                lines.append("")

    # Sources section
    lines.append("## Sources")
    lines.append("")
    lines.append(f"- [Original post]({url})")
    for followup in followups:
        lines.append(f"- [Thread continuation]({followup['url']})")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Mastodon posts to markdown files"
    )
    parser.add_argument(
        "version",
        help="systemd version number (e.g., 258, 259)",
    )
    parser.add_argument(
        "--input-dir",
        default=None,
        help="Input directory with raw JSON (default: systemd-VERSION/posts/raw)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for markdown (default: systemd-VERSION/posts)",
    )
    args = parser.parse_args()

    version = args.version

    # Set up directories
    if args.input_dir:
        input_dir = Path(args.input_dir)
    else:
        input_dir = Path(f"systemd-{version}/posts/raw")

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f"systemd-{version}/posts")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load manifest
    manifest_file = input_dir / "manifest.json"
    if not manifest_file.exists():
        print(f"Error: {manifest_file} not found")
        print("Run fetch_mastodon_posts.py first")
        sys.exit(1)

    with open(manifest_file) as f:
        manifest = json.load(f)

    print(f"Converting posts for systemd v{version}")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print()

    # Process each thread starter
    converted = 0
    skipped = 0

    for post_info in manifest["posts"]:
        if not post_info["is_thread_starter"]:
            continue

        post_id = post_info["id"]

        # Load full post
        post_file = input_dir / f"{post_id}.json"
        context_file = input_dir / f"{post_id}_context.json"

        if not post_file.exists():
            print(f"  Warning: {post_file} not found, skipping")
            skipped += 1
            continue

        with open(post_file) as f:
            post = json.load(f)

        context = {}
        if context_file.exists():
            with open(context_file) as f:
                context = json.load(f)

        # Extract post number
        content = post.get("content", "")
        post_number = extract_post_number(content)

        # Skip non-numbered posts for now (meta posts, etc.)
        if post_number is None:
            print(f"  Skipping non-numbered post {post_id}")
            skipped += 1
            continue

        # Generate slug
        slug = generate_slug(content, post_number)

        # Convert to markdown
        markdown = convert_post_to_markdown(post, context, post_number, version)

        # Write output file
        output_file = output_dir / f"{post_number:02d}-{slug}.md"
        with open(output_file, "w") as f:
            f.write(markdown)

        print(f"  [{post_number:02d}] {output_file.name}")
        converted += 1

    print()
    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")
    print(f"\nDone! Files saved to {output_dir}")


if __name__ == "__main__":
    main()
