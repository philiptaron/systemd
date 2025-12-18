---
layout: post
title: "systemd 258 Feature Highlight #54"
date: 2025-09-17
source: https://mastodon.social/@pid_eins/115218817138427511
author: Lennart Poettering
---

5️⃣4️⃣ Here's the 54th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Since a longer time systemd has been providing support for DDIs, i.e. for GPT disk images that carry expressive GPT partition types for their partitions so that the GPT partition table alone is enough to know how to assemble things and where to mount what. The logic in systemd that processes the GPT information and assembles it is named "image dissection".

## Thread Continuation

*2025-09-17* ([source](https://mastodon.social/@pid_eins/115218854506397568))

There's now a "dissect_image" built-in in udev. ("built-ins" in udev are little programs that udev can invoke on a device via udev rules, that are linked directly into the udev binary, i.e. are not implemented via external call-out binaries). 

The new builtin is automatically invoked on the root disk booted into via a new udev rules file (90-image-dissect.rules). The results are used to generate a bunch of symlinks to the right partition block devices in the /dev/disk/by-designator/… subdir.

*2025-09-17* ([source](https://mastodon.social/@pid_eins/115218866057205267))

Or in other words: if you boot into a DDI, you will now have symlinks such as /dev/disk/by-designator/root, /dev/disk/by-designator/usr, /dev/disk/by-designator/home, /dev/disk/by-designator/esp and so on, that make it very easy to generically reference partition block devices that are closely associated to the booted root fs, as per the DDI specs.

The dissection done through the udev built-in takes the the image policy/filtering into consideration that is specified on the kernel cmdline…

*2025-09-17* ([source](https://mastodon.social/@pid_eins/115218871789187203))

…, just like systemd-gpt-auto-generator.

TLDR: it's even nicer now to boot physically into a proper DDI, because the designations made in the GPT partition table now directly translate to device symlinks in /dev/.

*2025-09-17* ([source](https://mastodon.social/@pid_eins/115219743602842553))

[@grawity](https://social.treehouse.systems/@grawity) we have that. Any gpt disk qualifies as ddi after all, at least to the point of an esp, as that's always recognizable correctly.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115218828416801585):** Image dissection underpins RootImage= in unit files, systemd-nspawn's --image= switch or systemd-gpt-auto-generator, the various --image= switches of tools such as systemd-tmpfiles, systemd-sysusers and so on, and is also what systemd-mountfsd wraps for unprivileged clients.

The dissection logic is quite powerful, it can enforce security policies on what it is doing there and can unlock images with LUKS or Verity. 

With systemd v258 there's one more place where image dissection is used:

There's now a "dissect_image" built-in in udev. ("built-ins" in udev are little programs that udev can invoke on a device via udev rules, that are linked directly into the udev binary, i.e. are not implemented via external call-out binaries). 

The new builtin is automatically invoked on the root disk booted into via a new udev rules file (90-image-dissect.rules). The results are used to generate a bunch of symlinks to the right partition block devices in the /dev/disk/by-designator/… subdir.

## Sources

- [Original post](https://mastodon.social/@pid_eins/115218817138427511)
- [Thread continuation](https://mastodon.social/@pid_eins/115218854506397568)
- [Thread continuation](https://mastodon.social/@pid_eins/115218866057205267)
- [Thread continuation](https://mastodon.social/@pid_eins/115218871789187203)
- [Thread continuation](https://mastodon.social/@pid_eins/115219743602842553)
