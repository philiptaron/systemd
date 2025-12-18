---
layout: post
title: "UKI Addons Support"
date: 2025-06-12
---

Here's the 15th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In v257 we extended `systemd-stub` so that the UKI it's placed in can carry multiple Devicetree blobs and match the host's hardware against these blobs, passing the right one to the invoked kernel. The matching is based on Devicetree "compatible" strings and SMBIOS metadata.

This is quite powerful as it allows supercharging UKIs with system-specific low-level metadata, to create a truly universal UKI, that does the right thing on a wide variety of hardware.

A very similar need came up in the area of Confidential Computing (CoCo). One of the fundamental ideas of CoCo is that the owner of a VM owns the entire code running in it, and the host has no control whatsoever over it. This raises interesting problems because on PCs (and VMs typically emulate those), there's a major chunk of code that comes with the PC (and hence the VM) but not with the OS (i.e., the payload of the system): the firmware (sloppily called "BIOS" by many, regardless if UEFI or not).

On one hand the firmware needs to be there so you can boot the VM like a PC, but on the other hand it shouldn't be there because it would come from the `VMM`, and hence in a CoCo world you cannot trust it.

The CoCo people came up with a solution: "Bring-Your-Own-Firmware" (`BYOF`). This means as a CoCo VM ("`CVM`") boots for the first time, it might come with the original `VMM`-provided firmware, but the OS can then issue an immediate firmware update to a firmware version provided by the VM owner and reboot. On the second boot, the system will come up with owner-provided firmware, and the `CPU`/`TCB` will prove that's the case.

With v258 `systemd-stub` has been extended to optionally support `BYOF` environments directly: a firmware may now be embedded into a UKI (just like a Devicetree blob), and it can be matched against the local system (via `SMBIOS`, just like the Devicetree blobs). If a matching firmware is found, the update is issued and the system rebooted, unless it can be proven that the firmware is already the right one.

With that you can hence put together a truly universal UKI: if it finds itself in a suitable CoCo environment the UKI will ensure you also own the firmware, and only then progress into the Linux world.

I find it particularly interesting to identify areas of common behavior that completely separate areas of the computing spectrum require. Here we can leverage the exact same matching logic we need for Devicetree (more on the embedded side of things) for CoCo environments (more on the server side of things), maintaining somewhat simple concepts across the spectrum that nonetheless deliver what's necessary.

---

## Q&A

> **What does 'UKI' stand for?**

Unified Kernel Image.

See this for a more detailed explanation: [https://uapi-group.org/specifications/specs/unified_kernel_image/](https://uapi-group.org/specifications/specs/unified_kernel_image/)

---

[systemd-stub]: https://www.freedesktop.org/software/systemd/man/258/systemd-stub.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114669334251141174) (2025-06-12)
