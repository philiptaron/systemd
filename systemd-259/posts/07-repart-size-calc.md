---
layout: post
title: "systemd-repart size calculation"
date: 2025-11-26
---

7️⃣ Here's the 7th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

systemd-repart is systemd's dynamic, elastic image generation and repartitioning tool. It can either run "online" during early boot to create/encrypt root file systems or other partitions on the running system, or it can run "offline" to prepare images that can later be booted.

With systemd v259 it gained one new trick:

Normally, you are supposed to call it with a block device path or a disk image file as argument, and it will do its thing on that. With v259 you may instead specify "-" as image/device to operate on. And if you do that, then instead of actually doing its thing it will just calculate the minimum image size required for the defined partitions and print that and exit. Or in other words, you can call this, and use the information shown to determine whether an image will fit on some disk, without actually invoking the tool on it. You can also use it to figure out how large to allocate a disk image file before running repart on it (but do note, you might as well use --empty=create for that, which will do the size determination *and* create the image file for you).

And that's all for today.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115614881738923176) (2025-11-26)
