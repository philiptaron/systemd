---
layout: post
title: "systemd 258 Feature Highlight #10"
date: 2025-06-04
source: https://mastodon.social/@pid_eins/114623820293284298
author: Lennart Poettering
---

1️⃣0️⃣ Here's the 10th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In datacenter setups as well as for local test infrastructure it's very useful to network boot systems, so that they read their boot files not from a local hard disk but from some networked server.

In a modern UEFI world this is taken care of by HTTP boot: the UEFI firmware natively implements HTTP, can acquire either a single EFI program via that, or a disk image, and boot into that.

## Thread Continuation

*2025-06-04* ([source](https://mastodon.social/@pid_eins/114623844177201218))

… and even if it performs reasonably well, if your disk image is large it might take ages to fully download it before the firmware can transition into it.

So, what options are there to make things better? The key is to break the image into pieces and simply download less, and leave as much of that downloading to userspace.

systemd-boot in v258 will help you with that. We have extended the Boot Loader Spec Type #1 files (those .conf files in /boot/loader/entries) to support a new stanza:

*2025-06-04* ([source](https://mastodon.social/@pid_eins/114623855905217380))

"uki-url". This is used in a very similar way to the current "linux" stanza: you point it to a kernel to boot. In this case however it can be an URL where a UKI is placed.

So what can you do with this? You can build a tiny disk image that consists of just an UEFI ESP with systemd-boot in it, plus one or more Type #1 files, one for each potential kernel you want to boot, each with an "uki-url" line. This disk image is small of course, it contains only one binary, a few directory inodes…

*2025-06-04* ([source](https://mastodon.social/@pid_eins/114623867209570150))

…and a few tiny text files for the kernels. This will nicely populate the systemd-boot menu. And once you select an entry (or once auto-selection did it), that's when the listed UKI is downloaded and transitioned into. It's the UKIs job then to acquire/find a root disk (which we'll talk about in a later episode).

Now, here's one nice trick: the "uki-url" stanza can actually be relative, in which case a combined URL is generated from the URL sd-boot's image was placed on, plus the listed suffix.

*2025-06-04* ([source](https://mastodon.social/@pid_eins/114623880077186256))

With that you can hence build a nice boot chain: you tell your firmware the URL of the small ESP disk image, and the later stages can then be derived from that automatically.

*2025-06-04* ([source](https://mastodon.social/@pid_eins/114623882822108003))

Oh, and "mkosi" has been updated to generate images for this kind of network booting.

And did I mention that OVMF (i.e. qemu in uefi mode) supports network booting with this just fine?

*2025-06-04* ([source](https://mastodon.social/@pid_eins/114625604001995364))

[@GabrielKerneis](https://oc.todon.fr/@GabrielKerneis) One can extract that from the "device path" of the sd-boot "image".

See <https://github.com/systemd/systemd/blob/main/src/boot/url-discovery.c>

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114623829671046223):** This is actually excellent in many ways, as this is reasonably current tech, and it requires very little preparation: it's good enough so that you can just take a regular disk image and network boot it, and it mostly will just work.

Except of course, that while this basically works, it might not be what you actually want to do: if you have a large disk image you need a lot of RAM to load it into. Moreover the networking implementation in UEFI mode might not be the most efficient, …

… and even if it performs reasonably well, if your disk image is large it might take ages to fully download it before the firmware can transition into it.

So, what options are there to make things better? The key is to break the image into pieces and simply download less, and leave as much of that downloading to userspace.

systemd-boot in v258 will help you with that. We have extended the Boot Loader Spec Type #1 files (those .conf files in /boot/loader/entries) to support a new stanza:

## Sources

- [Original post](https://mastodon.social/@pid_eins/114623820293284298)
- [Thread continuation](https://mastodon.social/@pid_eins/114623844177201218)
- [Thread continuation](https://mastodon.social/@pid_eins/114623855905217380)
- [Thread continuation](https://mastodon.social/@pid_eins/114623867209570150)
- [Thread continuation](https://mastodon.social/@pid_eins/114623880077186256)
- [Thread continuation](https://mastodon.social/@pid_eins/114623882822108003)
- [Thread continuation](https://mastodon.social/@pid_eins/114625604001995364)
