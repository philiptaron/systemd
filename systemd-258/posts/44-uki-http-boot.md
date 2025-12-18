---
layout: post
title: "UKI HTTP boot"
date: 2025-08-22
---

Back in episode 10 of this series we talked about the new `url-uki` stanza in boot loader spec type 1 entries, which configures UKIs that are placed on a remote URL rather than stored locally in ESP/XBOOTLDR. This story already hinted that UEFI HTTP network boot of UKIs is actually a thing now.

Back in episode 35 we talked about booting into a DDI root filesystem that's downloaded via HTTP inside the initrd and placed into memory.

These two things complement each other nicely: the firmware downloads the UKI and transitions into it, and the initrd in the UKI then downloads the rootfs and transitions into that.

To make this really nice, there's value in being able to derive the rootfs URL from the UKI URL, so that both files can be placed on the same server, and only the first URL has to be declared in full.

To make this work, `systemd-stub` learnt a new trick in v258: if it detects it is run as a PE binary downloaded from HTTP, it will determine the source URL and then set the generic `LoaderDeviceURL` EFI variable to it. This EFI variable is part of the boot loader interface and mirrors nicely the existing `LoaderDevicePartUUID` EFI variable that indicates the GPT partition UUID that the UKI was booted from. The former EFI variable is hence set for remote boots, the latter for local boots.

`bootctl` has been updated to show the new variable. But more importantly, the `systemd.pull=` kernel cmdline switch we talked about in episode 35 now knows the new `bootorigin` flag. If used, the URL to download an image from can just be a relative path, which is then combined with the UKI URL reported by `systemd-stub` to form a full URL.

Example:

```
rd.systemd.pull=raw,machine,verify=no,blockdev,bootorigin:rootdisk:image.raw.xz root=/dev/disk/by-loop-ref/rootdisk.raw-part2
```

If such a switch is built into the command line of a UKI and that UKI is placed on a server `http://example.com/foobar/uki.efi` then this will result in the root disk being downloaded from `http://example.com/foobar/image.raw.xz`.

TLDR: it's now really nice to do UKI+DDI booting from UEFI HTTP.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115071247493189919) (2025-08-22)
