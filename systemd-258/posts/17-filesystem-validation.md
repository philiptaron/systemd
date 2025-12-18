---
layout: post
title: "File system validation"
date: 2025-06-16
---

In systemd we focus a lot on the integrity of the OS. Among various other things this means strong support for Verity protected, immutable file systems. You can run the OS from one, and you can run services from them, as well as containers.

We generally recommend placing Verity protected file systems in DDIs ("Discoverable Disk Images"), which ultimately are just GPT partitioned disk images, which use a number of well-known patition type UUIDs to properly mark the data partition, the Verity protection partition and possibly a signature protection. (See https://uapi-group.org/specifications/specs/discoverable_disk_image/ for more information).

While Verity protects the actual payload of such DDIs, there's some data it does *not* protect: the various bits and fields the GPT partition table itself contains.

Because of that we always have been somewhat reluctant to encode additional metadata in the GPT partition table fields, and preferred to focus more on storing any such data in the file systems themselves, wherever possible.

The idea was hence to put enough metadata in the GPT metadata so that one can assemble Verity file systems (and encrypted file systems) properly, but not more. But of course, there are limits to that.

There's in particular on facet that so far was *not* protected: The *purpose* of the file system itself is encoded in the GPT (i.e. if some fs is a root fs, or is for /usr/ or for /home/ or for something else), and by swapping out the GPT partition type one can "redirect" the purpose to something else, making the boot code assemble it incorrectly (i.e. mount a /usr/ partitions as root fs, or vice versa). While it's not obvious to me how that could be used for an attack it certainly is something we really should lock down.

Or in other words: if we discover some file system, and it looks like we shall use it for /usr/ (based on unprotected GPT metadata), and we assemble it, and mount it to /usr/ then we must verify it *actually* was intended for that, and isn't actually something entirely different, intended to be mounted to / or so.

For that we need two things:

1. File systems must be able to encode metadata about their intended purpose

2. We need some code that looks at that metadata and compares it with how things have been mounted, and acts on it somehow.

With v258 we did just that. The metadata of the intended use for file systems we decided to encode in a number of extended attributes on the root inode of the file system ("user.validatefs.*"). And there's a new mini service `systemd-validatefs@.service` that can check them, and validate them.

The xattrs encode the intended mount location for the file system, and they may also carry a copy of the GPT partition type UUID and the GPT partition label the file system is to be placed in.

`systemd-repart` has been updated to generate these xattrs automatically and by default for all images it creates. Thus, any modern OS images built via mkosi/`systemd-repart` should get this protection for free.

Effective result: if an attacker tries to manipulate the unprotected GPT metadata of a locked down DDI, and boots it up, it will progress to some point: the file systems will be mounted, and then verified. At which time the manipulation will be detected, because the protected xattr data won't match the unprotected GPT data anymore, and an immediate reboot is issued.

In a way this mechanism nicely bridges the flexibility and self-descriptiveness of the DDI/GPT approach on one hand with strong security of the image on the other, retaining one without losing the other.

For more information see the `systemd-validatefs@.service` man page. (In XML for now, the web version has not been updated with the git version yet. Sorry)

The constraints are only enforced on mounts actually relevant for the system, i.e. only for mounts placed on the rootfs, on /usr/ or /home/ or so. If you manually mount some fs to some temporary place for debugging/recovery then nothing of this applies, because such a mount is not "load bearing" for the OS.

systemd's gpt auto logic only does ddi dissection on the disk the esp used to boot is on. Thus, we should never mix&match stuff from multiple disks even if partition uuids are not unique. Hence if you plug in a 2nd disk, it might not always be clear which disk the firmware picks to boot from, but from then on it should be that one and no other.

There's also `dm-integrity` which you can either use together with `dm-crypt` or you can use standalone with an HMAC as hash func, in case you just want integrity tied to some secret, but are not interested in confidentiality. `dm-integrity` and `dm-crypt` are tightly integrated, it's relatively efficient to combine them.

[systemd-validatefs@.service]: https://www.freedesktop.org/software/systemd/man/258/systemd-validatefs@.service.html
[systemd-repart]: https://www.freedesktop.org/software/systemd/man/258/systemd-repart.html
[dm-integrity]: https://www.kernel.org/doc/html/latest/admin-guide/device-mapper/dm-integrity.html
[dm-crypt]: https://www.kernel.org/doc/html/latest/admin-guide/device-mapper/dm-crypt.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114691782651088597) (2025-06-16)
