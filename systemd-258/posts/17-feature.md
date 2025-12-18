---
layout: post
title: "systemd 258 Feature Highlight #17"
date: 2025-06-16
source: https://mastodon.social/@pid_eins/114691782651088597
author: Lennart Poettering
---

1️⃣7️⃣ Here's the 17th  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In systemd we focus a lot on the integrity of the OS. Among various other things this means strong support for Verity protected, immutable file systems. You can run the OS from one, and you can run services from them, as well as containers.

We generally recommend placing Verity protected file systems in DDIs ("Discoverable Disk Images"), …

## Thread Continuation

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691814836458351))

Because of that we always have been somewhat reluctant to encode additional metadata in the GPT partition table fields, and preferred to focus more on storing any such data in the file systems themselves, wherever possible.

The idea was hence to put enough metadata in the GPT metadata so that one can assemble Verity file systems (and encrypted file systems) properly, but not more. But of course, there are limits to that.

There's in particular on facet that so far was *not* protected:

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691824330539702))

The *purpose* of the file system itself is encoded in the GPT (i.e. if some fs is a root fs, or is for /usr/ or for /home/ or for something else), and by swapping out the GPT partition type one can "redirect" the purpose to something else, making the boot code assemble it incorrectly (i.e. mount a /usr/ partitions as root fs, or vice versa). While it's not obvious to me how that could  be used for an attack it certainly is something we really should lock down.

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691840509947430))

Or in other words: if we discover some file system, and it looks like we shall use it for /usr/ (based on unprotected GPT metadata), and we assemble it, and mount it to /usr/ then we must verify it *actually* was intended for that, and isn't actually something entirely different, intended to be mounted to / or so. 

For that we need two things: 
1. File systems must be able to encode metadata about their intended purpose

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691852900047056))

2. We need some code that looks at that metadata and compares it with how things have been mounted, and acts on it somehow.

With v258 we did just that. The metadata of the intended use for file systems we decided to encode in a number of extended attributes on the root inode of the file system ("user.validatefs.*"). And there's a new mini service systemd-validatefs@.service that can check them, and validate them.

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691862013145185))

The xattrs encode the intended mount location for the file system, and they may also carry a copy of the GPT partition type UUID and the GPT partition label the file system is to be placed in.

systemd-repart has been updated to generate these xattrs automatically and by default for all images it creates. Thus, any modern OS images built via mkosi/systemd-repart should get this protection for free.

Effective result: if an attacker tries to manipulate the unprotected GPT metadata of such…

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691870737703016))

… a locked down DDI, and boots it up, it will progress to some point: the file systems will be mounted, and then verified. At which time the manipulation will be detected, because the protected xattr data won't match the unprotected GPT data anymore, and an immediate reboot is issued.

In a way this mechanism nicely bridges the flexibility and self-descriptiveness of the DDI/GPT approach on one hand with strong security of the image on the other, retaining one without losing the other.

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114691879131013268))

For more information see the <https://github.com/systemd/systemd/blob/main/man/systemd-validatefs%40.service.xml> man page. (In XML for now, the web version has not been updated with the git version yet. Sorry)

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114692032179794875))

[@agowa338](https://chaos.social/@agowa338) The constraints are only enforced on mounts actually relevant for the system, i.e. only for mounts placed on the rootfs, on /usr/ or /home/ or so. If you manually mount some fs to some temporary place for debugging/recovery then nothing of this applies, because such a mount is not "load bearing" for the OS.

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114693005154050092))

[@agowa338](https://chaos.social/@agowa338) systemd's gpt auto logic only does ddi dissection on the disk the esp used to boot is on. Thus, we should never mix&match stuff from multiple disks even if partition uuids are not unique. Hence if you plug in a 2nd disk, it might not always be clear which disk the firmware picks to boot from, but from then on it should be that one and no other.

*2025-06-16* ([source](https://mastodon.social/@pid_eins/114693422614360474))

[@agowa338](https://chaos.social/@agowa338) not precisely an lvm fanboy here. Sorry. Also i am pretty sure lvm has no concept of cryptographic metadata integrity. I doubt using lvm and building a modern, secure OS are really compatible goals, but hey that's just my opinion.

*2025-07-10* ([source](https://mastodon.social/@pid_eins/114828555145941255))

[@alwayscurious](https://infosec.exchange/@alwayscurious) [@agowa338](https://chaos.social/@agowa338) [@QubesOS](https://mastodon.social/@QubesOS) there's dm-integrity which you can either use together with dm-crypt or you can use standalone with an HMAC as hash func, in case you just want integrity tied to some secret, but are not interested in confidentiality.

*2025-07-10* ([source](https://mastodon.social/@pid_eins/114828741926403666))

[@agowa338](https://chaos.social/@agowa338) [@alwayscurious](https://infosec.exchange/@alwayscurious) [@QubesOS](https://mastodon.social/@QubesOS) dm-integrity and dm-crypt are tightly integrated, it's relatively efficient to combine them. See docs of dm-integrity.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114691798171971621):** … which ultimately are just GPT partitioned disk images, which use a number of well-known patition type UUIDs to properly mark the data partition, the Verity protection partition and possibly a signature protection. (See <https://uapi-group.org/specifications/specs/discoverable_disk_image/> for more information).

While Verity protects the actual payload of such DDIs, there's some data it does *not* protect: the various bits and fields the GPT partition table itself contains.

Because of that we always have been somewhat reluctant to encode additional metadata in the GPT partition table fields, and preferred to focus more on storing any such data in the file systems themselves, wherever possible.

The idea was hence to put enough metadata in the GPT metadata so that one can assemble Verity file systems (and encrypted file systems) properly, but not more. But of course, there are limits to that.

There's in particular on facet that so far was *not* protected:

## Sources

- [Original post](https://mastodon.social/@pid_eins/114691782651088597)
- [Thread continuation](https://mastodon.social/@pid_eins/114691814836458351)
- [Thread continuation](https://mastodon.social/@pid_eins/114691824330539702)
- [Thread continuation](https://mastodon.social/@pid_eins/114691840509947430)
- [Thread continuation](https://mastodon.social/@pid_eins/114691852900047056)
- [Thread continuation](https://mastodon.social/@pid_eins/114691862013145185)
- [Thread continuation](https://mastodon.social/@pid_eins/114691870737703016)
- [Thread continuation](https://mastodon.social/@pid_eins/114691879131013268)
- [Thread continuation](https://mastodon.social/@pid_eins/114692032179794875)
- [Thread continuation](https://mastodon.social/@pid_eins/114693005154050092)
- [Thread continuation](https://mastodon.social/@pid_eins/114693422614360474)
- [Thread continuation](https://mastodon.social/@pid_eins/114828555145941255)
- [Thread continuation](https://mastodon.social/@pid_eins/114828741926403666)
