---
layout: post
title: "DDI designators"
date: 2025-09-17
---

Here's the 54th post highlighting key new features of the upcoming v258 release of systemd.

Since a longer time systemd has been providing support for DDIs, i.e. for GPT disk images that carry expressive GPT partition types for their partitions so that the GPT partition table alone is enough to know how to assemble things and where to mount what. The logic in systemd that processes the GPT information and assembles it is named "image dissection".

Image dissection underpins `RootImage=` in unit files, `systemd-nspawn`'s `--image=` switch, `systemd-gpt-auto-generator`, the various `--image=` switches of tools such as `systemd-tmpfiles`, `systemd-sysusers`, and so on, and is also what `systemd-mountfsd` wraps for unprivileged clients. The dissection logic is quite powerful—it can enforce security policies on what it is doing there and can unlock images with LUKS or Verity.

With systemd v258 there's one more place where image dissection is used: there's now a `dissect_image` built-in in udev. Built-ins in udev are little programs that udev can invoke on a device via udev rules, that are linked directly into the udev binary (i.e. are not implemented via external call-out binaries).

The new builtin is automatically invoked on the root disk booted into via a new udev rules file (`90-image-dissect.rules`). The results are used to generate a bunch of symlinks to the right partition block devices in the `/dev/disk/by-designator/...` subdirectory.

If you boot into a DDI, you will now have symlinks such as `/dev/disk/by-designator/root`, `/dev/disk/by-designator/usr`, `/dev/disk/by-designator/home`, `/dev/disk/by-designator/esp` and so on, that make it very easy to generically reference partition block devices that are closely associated to the booted root fs, as per the DDI specs. The dissection done through the udev built-in takes the image policy/filtering into consideration that is specified on the kernel cmdline, just like `systemd-gpt-auto-generator`.

In short: it's even nicer now to boot physically into a proper DDI, because the designations made in the GPT partition table now directly translate to device symlinks in `/dev/`.

---

## Q&A

> **[@grawity](https://social.treehouse.systems/@grawity)** Would be useful to have a similar thing for `/dev/disk/current-esp` for traditional-boot systems (maybe determining current from the Loader* efivars that sd-boot already provides)

We have that. Any GPT disk qualifies as a DDI after all, at least to the point of an ESP, as that's always recognizable correctly.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115218817138427511) (2025-09-17)
