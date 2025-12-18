---
layout: post
title: "HTTP boot with systemd-boot"
date: 2025-06-04
---

Here's the 10th post highlighting key new features of the upcoming v258 release of systemd. #systemd258

In datacenter setups as well as for local test infrastructure it's very useful to network boot systems, so that they read their boot files not from a local hard disk but from some networked server.

In a modern UEFI world this is taken care of by HTTP boot: the UEFI firmware natively implements HTTP, can acquire either a single EFI program via that or a disk image, and boot into that.

This is actually excellent in many ways, as this is reasonably current tech, and it requires very little preparation: it's good enough so that you can just take a regular disk image and network boot it, and it mostly will just work.

Except of course, that while this basically works, it might not be what you actually want to do: if you have a large disk image you need a lot of RAM to load it into.
Besides, the networking implementation in UEFI mode might not be the most efficient.

And even if it performs reasonably well, if your disk image is large it might take ages to fully download it before the firmware can transition into it.

So, what options are there to make things better?
The key is to break the image into pieces and simply download less, and leave as much of that downloading to userspace.

`systemd-boot` in v258 will help you with that.
We have extended the Boot Loader Spec Type #1 files (those `.conf` files in `/boot/loader/entries`) to support a new stanza: `uki-url`.

This is used in a very similar way to the current `linux` stanza: you point it to a kernel to boot.
In this case however it can be a URL where a UKI is placed.

So what can you do with this?
You can build a tiny disk image that consists of just an UEFI ESP with `systemd-boot` in it, plus one or more Type #1 files, one for each potential kernel you want to boot, each with a `uki-url` line.
This disk image is small of course, it contains only one binary, a few directory inodes...

...and a few tiny text files for the kernels.
This will nicely populate the `systemd-boot` menu.
And once you select an entry (or once auto-selection did it), that's when the listed UKI is downloaded and transitioned into.
It's the UKIs job then to acquire/find a root disk (which we'll talk about in a later episode).

Now, here's one nice trick: the `uki-url` stanza can actually be relative, in which case a combined URL is generated from the URL the `sd-boot` image was placed on, plus the listed suffix.

With that you can hence build a nice boot chain: you tell your firmware the URL of the small ESP disk image, and the later stages can then be derived from that automatically.

Oh, and [`mkosi`][mkosi] has been updated to generate images for this kind of network booting.

And did I mention that OVMF (i.e. qemu in UEFI mode) supports network booting with this just fine?

---

> **[@GabrielKerneis](https://oc.todon.fr/@GabrielKerneis):** How does sd-boot know its URL?
> Is it passed as some kind of parameter/environment by UEFI HTTP boot?

One can extract that from the device path of the `sd-boot` image.

See [url-discovery.c](https://github.com/systemd/systemd/blob/main/src/boot/url-discovery.c)

---

[systemd-boot]: https://www.freedesktop.org/software/systemd/man/258/systemd-boot.html
[mkosi]: https://www.freedesktop.org/software/systemd/man/258/mkosi.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114623820293284298) (2025-06-04)
