---
layout: post
title: "systemd 258 Feature Highlight #35"
date: 2025-08-08
source: https://mastodon.social/@pid_eins/114991974361745422
author: Lennart Poettering
---

3️⃣5️⃣ Here's the 35th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258) 

In various stateless situations it makes sense to boot directly into a root file system that is downloaded as part of the boot process and placed into system RAM. With v258 there's now native support for this: a new rd.systemd.pull= kernel command line option may be used to download DDIs or tarballs into a tmpfs, optionally authenticate them, and then boot into them.

## Thread Continuation

*2025-08-08* ([source](https://mastodon.social/@pid_eins/114991999323263269))

…(the verify=no is doing that), which sounds dangerous, but doesn't really have to be, if the referenced disk image is a proper DDI, i.e. carries Verity information and a signature for it.

There's one further twist to all this: the specified download URL can also be just a relative path, and the additional option "bootorigin" can be added. In that case the actual URL to download from is synthesized from UEFI HTTP boot source URL, in combination with the specified relative path.

*2025-08-08* ([source](https://mastodon.social/@pid_eins/114992007201389263))

Or in other words: this integrates really nicely with UEFI HTTP network boot, since the root fs image can be looked for automatically at the same place as the UKI that was booted from was downloaded from.

*2025-08-08* ([source](https://mastodon.social/@pid_eins/114993355776265038))

[@mupuf](https://social.treehouse.systems/@mupuf) you mean caching on a persistent disk? The thing kinda supports that already if you set up things correctly, but doesnt do version checks or so to see if cached image if it exists matches image to download, hence not sure how useful IRL.

*2025-08-08* ([source](https://mastodon.social/@pid_eins/114995141863608734))

[@philipmolloy](https://mastodon.social/@philipmolloy) yeah, mkosi only outputs DDIs.

If you want something more raw (i.e. just turn some pre-prepared directory tree into a DDI) use "systemd-repart -P"

*2025-08-12* ([source](https://mastodon.social/@pid_eins/115015558212370887))

[@alwayscurious](https://infosec.exchange/@alwayscurious) i dont really grok why that would be desirable though. Generally, Linux file systems must be authenticated before use (because kernel fs drivers are not robust against attacks via fs corruption), which you have to do via dm-verity/dm-crypt/dm-integrity pretty much. But once you did that then they are safe regardless which fs. Signing the part table is unnecessary too, given systemd's image policy logic, which protects things in a more flexible way, since it allows growing...

*2025-08-12* ([source](https://mastodon.social/@pid_eins/115015611835927417))

[@alwayscurious](https://infosec.exchange/@alwayscurious) ... partitions to allow for adapting to local systems/disk sizes. Moreover signing part tables would fixate part uuids too which means even writable fs for every deployed system would have the same identifiers, which is not just weird but also very broken?

(Signature partitions can already carry sigs for many root hashes/partitions, you already have that part hence, if you like)

I mean, not sure i grok your security model, but in mine signing part tables/fstypes...

*2025-08-12* ([source](https://mastodon.social/@pid_eins/115015618463783440))

[@alwayscurious](https://infosec.exchange/@alwayscurious) ... Is either counterproductive or even problematic.

(In one case systemd's gpt dissection logic hard pins an fstype btw: for the esp we enforce vfat, because esp is generally not protected cryptographically, and hence needs this kind of stricter logic)

*2025-08-13* ([source](https://mastodon.social/@pid_eins/115020098920691981))

[@alwayscurious](https://infosec.exchange/@alwayscurious) note that systemd's dissection logic is very restrictive with the fstypes it accepts and recognizes. Only the big Linux ones, i.e. ext4/btrfs/xfs/squashfs/erofs. I really don't see how it would be realistic to use a replay attack to change the fs signature from one of these 5 to another of these 5. 

Also note that btrfs these days supports cryptographic checksumming too, and its even fairly efficient given native cpu support these days.

*2025-08-13* ([source](https://mastodon.social/@pid_eins/115020106096579348))

[@alwayscurious](https://infosec.exchange/@alwayscurious) but dunno, what confuses me is why you think replay attacks could be avoided if gpt partition tables could be signed as a whole or the choice of fstype could be included in the signed data?

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114991986441127571):** DDIs can be automatically attached to a loopback block device, to make this work (via the new generic systemd-loop@.service template service which just attaches a DDI to a loopback device), and tarballs can be unpacked automatically, too.

Here's an example for a kernel cmdline switch for booting into a DDI:

rd.systemd.pull=raw,machine,verify=no,blockdev:image:https://192.168.100.1:8081/image.raw root=/dev/disk/by-loop-ref/image.raw-part2

This example disables authentication…

…(the verify=no is doing that), which sounds dangerous, but doesn't really have to be, if the referenced disk image is a proper DDI, i.e. carries Verity information and a signature for it.

There's one further twist to all this: the specified download URL can also be just a relative path, and the additional option "bootorigin" can be added. In that case the actual URL to download from is synthesized from UEFI HTTP boot source URL, in combination with the specified relative path.

> **[@mupuf@treehouse.systems](https://social.treehouse.systems/@mupuf/114992320469745281):** [@pid_eins](https://mastodon.social/@pid_eins) Nice!

Had this existed 5 years ago, I would not have started the boot2container project!

Do you think it could provide some sort of caching and avoid running fully from RAM, or is that reimplementing container runtimes too much?

[@mupuf](https://social.treehouse.systems/@mupuf) you mean caching on a persistent disk? The thing kinda supports that already if you set up things correctly, but doesnt do version checks or so to see if cached image if it exists matches image to download, hence not sure how useful IRL.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114991974361745422)
- [Thread continuation](https://mastodon.social/@pid_eins/114991999323263269)
- [Thread continuation](https://mastodon.social/@pid_eins/114992007201389263)
- [Thread continuation](https://mastodon.social/@pid_eins/114993355776265038)
- [Thread continuation](https://mastodon.social/@pid_eins/114995141863608734)
- [Thread continuation](https://mastodon.social/@pid_eins/115015558212370887)
- [Thread continuation](https://mastodon.social/@pid_eins/115015611835927417)
- [Thread continuation](https://mastodon.social/@pid_eins/115015618463783440)
- [Thread continuation](https://mastodon.social/@pid_eins/115020098920691981)
- [Thread continuation](https://mastodon.social/@pid_eins/115020106096579348)
