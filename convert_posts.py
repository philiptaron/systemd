#!/usr/bin/env python3
"""Convert Mastodon JSON posts to Markdown."""

import json
import re
import os
from datetime import datetime
from html import unescape

# Post metadata
POSTS = {
    "01": ("115570095861864513", "resolved-hooks"),
    "02": ("115575271970490767", "dlopen-dependencies"),
    "03": ("115580882123596509", "dlopen-metadata"),
    "04": ("115586469819973533", "run0-empower"),
    "05": ("115605598751722319", "vmspawn-bind-user"),
    "06": ("115611051983920298", "musl-libc"),
    "07": ("115614881738923176", "repart-size-calc"),
    "08": ("115620451885638963", "modules-load-parallel"),
    "09": ("115627835871078915", "tpm-verified-boot"),
    "10": ("115646310576910417", "analyze-nvpcrs"),
    "11": ("115662198906484836", "repart-varlink"),
    "12": ("115666147093865447", "vmspawn-disk"),
    "13": ("115740831317295811", "defer-partitions"),
}


def html_to_markdown(html):
    """Convert HTML content to Markdown."""
    if not html:
        return ""

    text = html

    # Handle line breaks
    text = re.sub(r'<br\s*/?>', '\n', text)

    # Handle paragraphs
    text = re.sub(r'</p>\s*<p>', '\n\n', text)
    text = re.sub(r'</?p>', '', text)

    # Handle links
    def replace_link(match):
        href = match.group(1)
        content = match.group(2)
        # Strip any nested spans/invisibles from link text
        content = re.sub(r'<[^>]+>', '', content)
        # If the content is just the URL, simplify
        if content.strip() == href or content.strip().startswith(href[:20]):
            return href
        return f'[{content}]({href})'

    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', replace_link, text, flags=re.DOTALL)

    # Handle code/pre blocks
    text = re.sub(r'<code>', '`', text)
    text = re.sub(r'</code>', '`', text)
    text = re.sub(r'<pre>', '\n```\n', text)
    text = re.sub(r'</pre>', '\n```\n', text)

    # Handle bold/strong
    text = re.sub(r'<strong>', '**', text)
    text = re.sub(r'</strong>', '**', text)
    text = re.sub(r'<b>', '**', text)
    text = re.sub(r'</b>', '**', text)

    # Handle italic/em
    text = re.sub(r'<em>', '*', text)
    text = re.sub(r'</em>', '*', text)
    text = re.sub(r'<i>', '*', text)
    text = re.sub(r'</i>', '*', text)

    # Remove span tags (often used for invisible text in Mastodon)
    text = re.sub(r'<span[^>]*class="[^"]*invisible[^"]*"[^>]*>.*?</span>', '', text, flags=re.DOTALL)
    text = re.sub(r'<span[^>]*class="[^"]*ellipsis[^"]*"[^>]*>(.*?)</span>', r'\1...', text, flags=re.DOTALL)
    text = re.sub(r'</?span[^>]*>', '', text)

    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Unescape HTML entities
    text = unescape(text)

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def format_date(iso_date):
    """Format ISO date to readable format."""
    dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M UTC')


def convert_post(num, post_id, slug):
    """Convert a single post and its context to markdown."""
    raw_dir = "posts/raw"

    # Load main post
    with open(f"{raw_dir}/{num}.json") as f:
        post = json.load(f)

    # Load context (replies)
    with open(f"{raw_dir}/{num}-context.json") as f:
        context = json.load(f)

    # Build markdown
    lines = []

    # Header
    post_url = post.get('url', f"https://mastodon.social/@pid_eins/{post_id}")
    created = format_date(post['created_at'])

    lines.append(f"# v259 Feature Highlight #{num.lstrip('0')}")
    lines.append("")
    lines.append(f"**Author:** [{post['account']['display_name']}]({post['account']['url']})")
    lines.append(f"**Posted:** {created}")
    lines.append(f"**Original:** [{post_url}]({post_url})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Main content
    content = html_to_markdown(post['content'])
    lines.append(content)
    lines.append("")

    # Handle media attachments
    if post.get('media_attachments'):
        lines.append("")
        lines.append("## Attachments")
        lines.append("")
        for media in post['media_attachments']:
            if media['type'] == 'image':
                desc = media.get('description', 'Image')
                lines.append(f"![{desc}]({media['url']})")
            else:
                lines.append(f"[{media['type']}: {media.get('description', 'attachment')}]({media['url']})")
        lines.append("")

    # Thread replies (descendants from the author)
    descendants = context.get('descendants', [])
    author_replies = [d for d in descendants if d['account']['id'] == post['account']['id']]

    if author_replies:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Thread Continuation")
        lines.append("")

        for reply in author_replies:
            reply_url = reply.get('url', '')
            reply_date = format_date(reply['created_at'])
            reply_content = html_to_markdown(reply['content'])

            lines.append(f"### [{reply_date}]({reply_url})")
            lines.append("")
            lines.append(reply_content)
            lines.append("")

            # Media in reply
            if reply.get('media_attachments'):
                for media in reply['media_attachments']:
                    if media['type'] == 'image':
                        desc = media.get('description', 'Image')
                        lines.append(f"![{desc}]({media['url']})")
                    else:
                        lines.append(f"[{media['type']}: {media.get('description', 'attachment')}]({media['url']})")
                lines.append("")

    # Footer
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Source: [Mastodon]({post_url})*")

    return '\n'.join(lines)


def main():
    os.chdir('/home/philip/Work/systemd-259-release-notes')

    for num, (post_id, slug) in POSTS.items():
        print(f"Converting post {num}: {slug}")
        markdown = convert_post(num, post_id, slug)

        output_path = f"posts/{num}-{slug}.md"
        with open(output_path, 'w') as f:
            f.write(markdown)

        print(f"  -> {output_path}")

    print("Done!")


if __name__ == '__main__':
    main()
