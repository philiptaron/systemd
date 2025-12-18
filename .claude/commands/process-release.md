# Process systemd Release Notes

This playbook documents how to process a new systemd release version. Replace `vXXX` with the actual version number (e.g., `v260`).

## Phase 1: Get Raw Content

### 1.1 Download Release Notes
- Fetch from `https://github.com/systemd/systemd/releases/tag/vXXX`
- Save to `systemd-XXX/release-notes.md`

### 1.2 Format Release Notes
- One sentence per line (semantic line breaks) for better diffs
- Use `-` for bullet points, not `*`
- Normalize heading spacing
- Remove excessive indentation

### 1.3 Track Mastodon Posts
- Find Lennart's announcement posts tagged `#systemdXXX` on `https://mastodon.social/@pid_eins`
- Create a TODO list tracking which posts need processing
- Posts typically follow pattern: "Here's the Nth post highlighting key new features..."

### 1.4 Download Mastodon Posts
For each post:
- Fetch via Mastodon API: `https://mastodon.social/api/v1/statuses/{POST_ID}`
- Also fetch thread context: `https://mastodon.social/api/v1/statuses/{POST_ID}/context`
- Save raw JSON for reference

### 1.5 Convert Posts to Markdown
- Create `systemd-XXX/posts/NN-slug.md` for each post
- Add Jekyll front matter (layout, title, date)
- Convert HTML content to markdown
- Preserve hashtag links

## Phase 2: Link Content Together

### 2.1 Link Posts to Release Notes
- Add "See also: [Lennart's explanation](posts/NN-slug.md)" to relevant release notes sections
- Match post topics to release notes sections

### 2.2 Generate Man Page Data
- Download man page index from `https://www.freedesktop.org/software/systemd/man/XXX/`
- Parse to extract: name, section number, description, URL
- Create `_data/manpages/vXXX/` directory structure:
  - `command/` - section 1 (user commands)
  - `function/` - section 3 (library functions)
  - `configuration/` - section 5 (config files)
  - `concept/` - section 7 (overviews)
  - `daemon/` - section 8 (system services)
- Each file: `name.yaml` with `description:` and `url:` fields

## Phase 3: Process Commentary Posts

For each post in `systemd-XXX/posts/`:

### 3.1 Restructure for Readability
- Remove "Thread Continuation" headers and individual timestamps
- Merge text split across posts into continuous prose
- Move source links to "## Sources" section at bottom
- Remove redundant author bylines

### 3.2 Add Q&A Context
- Fetch reply context from thread JSON
- Add blockquotes showing questions Lennart is replying to
- Format: `> **[@username](url):** Question text`
- Lennart's reply follows without redundant @-mention

### 3.3 Apply Semantic Line Breaks
- One sentence per line
- Makes diffs cleaner and editing easier

### 3.4 Wrap Technical Terms in Backticks
- systemd binaries/services: `systemd-resolved`, `systemd-repart`
- Command line flags: `--bind-user=`, `--defer-partitions=`
- Function calls: `dlopen()`, `sd_notify()`
- Configuration options: `DynamicUser=1`, `Format=empty`
- File paths: `/etc/modules-load.d/`, `/dev/disk/by-id/`
- NSS modules and libraries: `nss-mymachines`, `libsystemd.so`

### 3.5 Link Tools to Man Pages
- Convert first mention of each tool from `` `tool` `` to `` [`tool`][tool] ``
- Add reference definitions at bottom: `[tool]: https://www.freedesktop.org/software/systemd/man/XXX/tool.html`
- Only link tools that have man pages in `_data/manpages/vXXX/`

### 3.6 Expand Referenced Threads
- If a post references another person's thread (like "I'm going to top-post @someone's story...")
- Fetch that thread via Mastodon API
- Include the relevant content directly in the post
- Credit both sources

## Phase 4: Process Release Notes

### 4.1 Wrap Technical Terms in Backticks
Same categories as posts, plus:
- Environment variables: `$LISTEN_FDS`, `$HOME`, `$NOTIFY_SOCKET`
- D-Bus properties/methods: `Unit.List()`, `Reload()`, `Encrypt()`
- Flags and constants: `BLKRRPART`, `WNOWAIT`, `CAP_SYS_ADMIN`
- Protocol identifiers: `io.systemd.Resolve.Hook`

### 4.2 Link Tools to Man Pages
- Same process as posts
- Check all backticked tool names against `_data/manpages/vXXX/`
- Add links for tools that have man pages

## Phase 5: Verify

### 5.1 Check All Links
```bash
# Extract URLs and verify they return HTTP 200
grep -oE 'https://www.freedesktop.org/software/systemd/man/XXX/[^"]+\.html' \
  systemd-XXX/release-notes.md | sort -u | \
  xargs -P10 -I{} curl -s -o /dev/null -w "%{http_code} {}\n" --head {}
```

### 5.2 Review Content
- Read through posts for coherence
- Check that Q&A sections make sense
- Verify man page links are correct

## Notes

- The Jekyll site structure (layouts, sidebar, etc.) is set up once and reused
- Man page data structure allows quick lookups without token limits
- Semantic line breaks make future edits and diffs much cleaner
- Reference-style markdown links keep the prose readable
