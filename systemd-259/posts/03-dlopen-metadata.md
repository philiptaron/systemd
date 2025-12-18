---
layout: post
title: "systemd-analyze dlopen-metadata"
date: 2025-11-20
---

3️⃣ Here's the 3rd post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

This one is quick and closely related to what I discussed in the previous installment:

There's now a new verb "dlopen-metadata" in systemd-analyze that extracts the dlopen() metadata from an ELF file and displays it in tabular form.

As an example, here's how its output looks like for libsystemd-shared-259.so, i.e. the shared library that contains much of systemd's code that is shared between all its many binaries:

https://paste.centos.org/view/raw/95455033

And that's is already.

---

> **[@pemensik](https://fosstodon.org/@pemensik)** Yes. But I am more interested in how app linking to libsystemd will generate their mandatory requires. When it uses sd_dbus, what it requires? If calls sd_journal*, what then? This hiding makes all libraries used detection very hard.

Well, it's more complex that that. libsystemd.so itself mostly has deps on compression libs, and those are needed by the journal code. And the journal code only needs the compression libs if you actually have journal files with fields compressed with them. In most cases all your files will only have the same compression alg used, because journald allows you to pick only one when generating them.

Hence, it doesn't depend so much purely on the tool calling into the lib, but on the files you process with the lib.

It's a bit like with gstreamer or so, where you try to play a video file and don't have the codec around. You get a soft failure too, not a hard one, and this requirement for all codecs is not ever expressed in rpm.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115580882123596509) (2025-11-20)
