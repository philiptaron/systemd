---
layout: post
title: "systemd 258 Feature Highlight #15"
date: 2025-06-12
source: https://mastodon.social/@pid_eins/114669334251141174
author: Lennart Poettering
---

1️⃣5️⃣ Here's the 15th  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In v257 we extended systemd-stub so that the UKI it is placed in can carry multiple Devicetree blobs, and that it can match the host's hardware against these blobs, and pass the right, matching one to the invoked kernel. The matching is based on Devicetree "compatible" strings, as well as SMBIOS metadata.

## Thread Continuation

*2025-06-12* ([source](https://mastodon.social/@pid_eins/114669354364816668))

… there's a major chunk of code that comes with the PC (and hence the VM), and not with the OS (i.e. the payload of the system): and that's the firmware (sloppily just called "BIOS" by many, regardless if EFI or not).

On one hand the firmware is necessary to just be there, so that you can boot the VM like PC, but on the other hand it shouldn't be there, because it would come from the VMM, and hence in a CoCo world you cannot trust it.

*2025-06-12* ([source](https://mastodon.social/@pid_eins/114669365453703422))

The CoCo people came up with a solution to that: "Bring-Your-Own-Firmware" (BYOF). This means: as a CoCo VM ("CVM") boots up for the first time it might come with the original VMM provided firmware, but the OS then may issue an immediate firmware update, to a firmware version provideded by the VM owner, and reboot. On the second boot now the system will come up with a owner provided firmware, and the CPU/TCB will prove to you that that's the case.

*2025-06-12* ([source](https://mastodon.social/@pid_eins/114669373640020740))

With v258 systemd-stub has been extended to optionally support BYOF environments directly: a firmware may now be embedded into a UKI (just like a Devicetree blob can), and it can be matched against the local system (via SMBIOS, just like the Devicetree blobs can). If a matching firmware is found, the update is issued, and the system rebooted.  Unless of course it can be proven that the firmware is already the right one.

*2025-06-12* ([source](https://mastodon.social/@pid_eins/114669383368970878))

With that you can hence put together a truly universal UKI: if it finds itself in a suitable CoCo environment the UKI will ensure you also own the firmware, and only then progress into the Linux world.

To me it is always particularly interesting to identify areas of common behaviour, that completely separate areas of the computing spectrum require. I.e. here we can leverage the exact same matching logic we need for Devicetree (i.e. more on the embedded side of things) also for CoCo…

*2025-06-12* ([source](https://mastodon.social/@pid_eins/114669386853188259))

…environments (i.e. more on the server side of things), and maintain somewhat simple concepts across the spectrum, that nonetheless deliver what is necessary.

*2025-06-12* ([source](https://mastodon.social/@pid_eins/114669739802635766))

[@khleedril](https://cyberplace.social/@khleedril) Unified Kernel Image.

See this for a more detailed explanation: <https://uapi-group.org/specifications/specs/unified_kernel_image/>

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114669345825134181):** This is quite powerful as it allows supercharging UKIs with system-specific low-level metadata, to create a truely universal UKI, that does the right thing on a wide variety of hardware.

A very similar need came up in the are of Confidential Computing (CoCo). One of the fundamental ideas of CoCo is that the owner of VM owns the entire code running in it, and that the host has no control whatsoever over it. This raises interesting problems, because on PCs (and VMs typically emulate those), …

… there's a major chunk of code that comes with the PC (and hence the VM), and not with the OS (i.e. the payload of the system): and that's the firmware (sloppily just called "BIOS" by many, regardless if EFI or not).

On one hand the firmware is necessary to just be there, so that you can boot the VM like PC, but on the other hand it shouldn't be there, because it would come from the VMM, and hence in a CoCo world you cannot trust it.

> **[@khleedril@cyberplace.social](https://cyberplace.social/@khleedril/114669734152297494):** [@pid_eins](https://mastodon.social/@pid_eins) What does 'UKI' stand for?

[@khleedril](https://cyberplace.social/@khleedril) Unified Kernel Image.

See this for a more detailed explanation: <https://uapi-group.org/specifications/specs/unified_kernel_image/>

## Sources

- [Original post](https://mastodon.social/@pid_eins/114669334251141174)
- [Thread continuation](https://mastodon.social/@pid_eins/114669354364816668)
- [Thread continuation](https://mastodon.social/@pid_eins/114669365453703422)
- [Thread continuation](https://mastodon.social/@pid_eins/114669373640020740)
- [Thread continuation](https://mastodon.social/@pid_eins/114669383368970878)
- [Thread continuation](https://mastodon.social/@pid_eins/114669386853188259)
- [Thread continuation](https://mastodon.social/@pid_eins/114669739802635766)
