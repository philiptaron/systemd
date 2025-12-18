#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.requests

"""
Fetch Mastodon posts for a systemd release.

This script downloads:
1. All posts from Lennart (@pid_eins) tagged with #systemdXXX
2. All replies to those posts (the "context")
3. Organizes them into a structured JSON file

Usage:
    ./fetch_mastodon_posts.py 258
    ./fetch_mastodon_posts.py 259

Or with nix-shell explicitly:
    nix-shell -p python3 python3Packages.requests --run 'python3 fetch_mastodon_posts.py 258'

Output:
    Creates systemd-XXX/posts/raw/manifest.json with all posts and their threads
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

MASTODON_INSTANCE = "https://mastodon.social"
LENNART_USERNAME = "pid_eins"


def get_account_id(username: str) -> str:
    """Look up a Mastodon account ID by username."""
    url = f"{MASTODON_INSTANCE}/api/v1/accounts/lookup"
    resp = requests.get(url, params={"acct": username})
    resp.raise_for_status()
    return resp.json()["id"]


def fetch_hashtag_timeline(hashtag: str, limit: int = 40, max_id: str = None) -> list:
    """Fetch posts from a hashtag timeline."""
    url = f"{MASTODON_INSTANCE}/api/v1/timelines/tag/{hashtag}"
    params = {"limit": limit}
    if max_id:
        params["max_id"] = max_id
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_status(status_id: str) -> dict:
    """Fetch a single status by ID."""
    url = f"{MASTODON_INSTANCE}/api/v1/statuses/{status_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def fetch_context(status_id: str) -> dict:
    """Fetch the context (ancestors and descendants) of a status."""
    url = f"{MASTODON_INSTANCE}/api/v1/statuses/{status_id}/context"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def fetch_all_hashtag_posts(hashtag: str, username: str) -> list:
    """
    Fetch all posts with a given hashtag from a specific user.
    Handles pagination automatically.
    """
    print(f"Fetching posts tagged #{hashtag} from @{username}...")

    all_posts = []
    max_id = None
    page = 1

    while True:
        print(f"  Page {page}...", end=" ", flush=True)
        posts = fetch_hashtag_timeline(hashtag, max_id=max_id)

        if not posts:
            print("done (no more posts)")
            break

        # Filter to just the target user's posts
        user_posts = [p for p in posts if p["account"]["username"] == username]
        all_posts.extend(user_posts)
        print(f"found {len(user_posts)} posts from @{username}")

        # Get the last post ID for pagination
        max_id = posts[-1]["id"]
        page += 1

        # Rate limiting
        time.sleep(0.3)

        # Safety limit
        if page > 20:
            print("  Warning: hit page limit")
            break

    # Sort by creation date
    all_posts.sort(key=lambda p: p["created_at"])

    print(f"Total: {len(all_posts)} posts from @{username}")
    return all_posts


def fetch_threads_for_posts(posts: list, username: str) -> dict:
    """
    For each post, fetch its full thread context.
    Returns a dict mapping post_id -> thread data.
    """
    threads = {}

    print(f"\nFetching thread context for {len(posts)} posts...")

    for i, post in enumerate(posts):
        post_id = post["id"]
        print(f"  [{i+1}/{len(posts)}] Post {post_id}...", end=" ", flush=True)

        try:
            context = fetch_context(post_id)

            # Filter descendants to include:
            # 1. Direct replies from anyone
            # 2. Lennart's replies to those replies
            descendants = context.get("descendants", [])

            # Build reply chains
            replies = []
            lennart_followups = []

            for desc in descendants:
                # Is this a direct reply to the main post?
                if desc.get("in_reply_to_id") == post_id:
                    replies.append(desc)
                # Is this Lennart replying to someone?
                elif desc["account"]["username"] == username:
                    lennart_followups.append(desc)

            threads[post_id] = {
                "post": post,
                "ancestors": context.get("ancestors", []),
                "replies": replies,
                "lennart_followups": lennart_followups,
                "all_descendants": descendants,
            }

            print(f"{len(replies)} replies, {len(lennart_followups)} followups")

        except Exception as e:
            print(f"ERROR: {e}")
            threads[post_id] = {
                "post": post,
                "error": str(e),
            }

        # Rate limiting
        time.sleep(0.3)

    return threads


def identify_thread_starters(posts: list) -> list:
    """
    Identify which posts are thread starters (not replies to other posts).
    Returns list of post IDs that start threads.
    """
    starters = []
    for post in posts:
        if post.get("in_reply_to_id") is None:
            starters.append(post["id"])
    return starters


def create_manifest(posts: list, threads: dict, version: str) -> dict:
    """Create a manifest summarizing all the posts and threads."""
    thread_starters = identify_thread_starters(posts)

    # Group posts by thread (posts that are part of a thread chain)
    post_threads = {}  # Maps each starter to its chain of posts

    for post in posts:
        post_id = post["id"]
        if post_id in thread_starters:
            # This post starts a thread
            # Find all posts in this thread (replies from same author)
            chain = [post]
            thread_data = threads.get(post_id, {})

            # Add any posts that are replies in this thread
            for other in posts:
                if other["id"] != post_id:
                    # Check if this post is a reply in the same thread
                    if other.get("in_reply_to_id") == post_id:
                        chain.append(other)
                    # Or replies to replies in the chain
                    for c in chain:
                        if other.get("in_reply_to_id") == c["id"]:
                            if other not in chain:
                                chain.append(other)

            chain.sort(key=lambda p: p["created_at"])
            post_threads[post_id] = chain

    manifest = {
        "version": version,
        "hashtag": f"systemd{version}",
        "total_posts": len(posts),
        "thread_starters": len(thread_starters),
        "posts": [],
        "threads": {},
    }

    # Add simplified post info
    for post in posts:
        manifest["posts"].append({
            "id": post["id"],
            "created_at": post["created_at"],
            "url": post["url"],
            "is_thread_starter": post["id"] in thread_starters,
            "in_reply_to_id": post.get("in_reply_to_id"),
            "content_preview": post.get("content", "")[:200],
        })

    # Add thread info
    for starter_id, chain in post_threads.items():
        thread_data = threads.get(starter_id, {})
        manifest["threads"][starter_id] = {
            "post_count": len(chain),
            "post_ids": [p["id"] for p in chain],
            "reply_count": len(thread_data.get("replies", [])),
            "lennart_followup_count": len(thread_data.get("lennart_followups", [])),
        }

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Mastodon posts for a systemd release"
    )
    parser.add_argument(
        "version",
        help="systemd version number (e.g., 258, 259)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: systemd-VERSION/posts/raw)",
    )
    args = parser.parse_args()

    version = args.version
    hashtag = f"systemd{version}"

    # Set up output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f"systemd-{version}/posts/raw")

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching posts for systemd v{version}")
    print(f"Output directory: {output_dir}")
    print()

    # Step 1: Fetch all posts from Lennart with the hashtag
    posts = fetch_all_hashtag_posts(hashtag, LENNART_USERNAME)

    if not posts:
        print("No posts found!")
        sys.exit(1)

    # Step 2: Fetch thread context for each post
    threads = fetch_threads_for_posts(posts, LENNART_USERNAME)

    # Step 3: Create manifest
    manifest = create_manifest(posts, threads, version)

    # Step 4: Save everything
    print("\nSaving data...")

    # Save individual posts
    for post in posts:
        post_file = output_dir / f"{post['id']}.json"
        with open(post_file, "w") as f:
            json.dump(post, f, indent=2)

    # Save thread contexts
    for post_id, thread_data in threads.items():
        context_file = output_dir / f"{post_id}_context.json"
        with open(context_file, "w") as f:
            json.dump(thread_data, f, indent=2)

    # Save manifest
    manifest_file = output_dir / "manifest.json"
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"  Saved {len(posts)} post files")
    print(f"  Saved {len(threads)} context files")
    print(f"  Saved manifest.json")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total posts: {manifest['total_posts']}")
    print(f"Thread starters: {manifest['thread_starters']}")
    print()
    print("Thread starters by date:")
    for post in manifest["posts"]:
        if post["is_thread_starter"]:
            preview = post["content_preview"][:60].replace("\n", " ")
            # Strip HTML tags for preview
            import re
            preview = re.sub(r"<[^>]+>", "", preview)
            print(f"  {post['created_at'][:10]} | {post['id']} | {preview}...")

    print(f"\nDone! Data saved to {output_dir}")


if __name__ == "__main__":
    main()
