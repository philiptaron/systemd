---
layout: post
title: "systemd 258 Feature Highlight #22"
date: 2025-06-26
source: https://mastodon.social/@pid_eins/114748482077172097
author: Lennart Poettering
---

2️⃣2️⃣ Here's the 22nd  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Modern OS images created via mkosi typically use systemd-repart not just to build the base image, but also carry systemd-repart to grow/augment the image once booted: the tool can grow partitions, and it can create/encrypt new ones. This has many benefits:

The OS image self-adapts to the system in ends up being booted in, i.e. makes use of the full disk size available, …

## Thread Continuation

*2025-06-26* ([source](https://mastodon.social/@pid_eins/114748517412717098))

… space to the end of the image, so that once the system boots up we actually have space we can grow partitions too and create new ones. Previously I did this manually with the truncate or fallocate shell commands. But half the time I forgot, and because one of the tools wants the size specification with "-l" and the other with "-s" I just constantly called it the wrong way. 

With v258 vmspawn gained a new switch --grow-image= (or -G for short) which  does this step natively.

*2025-06-26* ([source](https://mastodon.social/@pid_eins/114748524653116530))

It's a bit safer that way (because it strictly grows the image, never truncates, unlike the truncate tool), and more space efficient. Moreover it does so after discovering the image first in the search directories, which makes things easier to use in many way.

Or in other words, once mkosi spits out a minimized image I can now directly invoke it via vmspawn, which expands the image as I want, and then boots it up immediately.

*2025-06-26* ([source](https://mastodon.social/@pid_eins/114748533200694651))

As the system now boots up, from the initrd systemd-repart will then "take possession" of the additional space at the end of the disk, growing existing file systems or creating new ones, and then continues booting into them.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114748503849975234):** …and the disk encryption keys can be created locally on the target system and kept there, which is really useful to deploy secure TPM-bound images. And all that even though the original downloaded image has minimal footprint, because it "auto-expands" after all.

I test such images basically every day, and I do so with systemd-vmspawn, because it's just so nice to use. But there's one preparatory step I need to do before I can boot such minimal images: I  need to add extra…

… space to the end of the image, so that once the system boots up we actually have space we can grow partitions too and create new ones. Previously I did this manually with the truncate or fallocate shell commands. But half the time I forgot, and because one of the tools wants the size specification with "-l" and the other with "-s" I just constantly called it the wrong way. 

With v258 vmspawn gained a new switch --grow-image= (or -G for short) which  does this step natively.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114748482077172097)
- [Thread continuation](https://mastodon.social/@pid_eins/114748517412717098)
- [Thread continuation](https://mastodon.social/@pid_eins/114748524653116530)
- [Thread continuation](https://mastodon.social/@pid_eins/114748533200694651)
