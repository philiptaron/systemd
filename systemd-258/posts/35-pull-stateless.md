---
layout: post
title: "Stateless booting via rd.systemd.pull"
date: 2025-08-08
---

Here's the 35th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258) [#systemd](https://mastodon.social/tags/systemd)

In various stateless situations it makes sense to boot directly into a root file system that is downloaded as part of the boot process and placed into system RAM. With v258 there's now native support for this: a new `rd.systemd.pull=` kernel command-line option may be used to download DDIs or tarballs into a `tmpfs`, optionally authenticate them, and then boot into them.

## Details

DDIs can be automatically attached to a loopback block device, to make this work (via the new generic `systemd-loop@.service` template service which just attaches a DDI to a loopback device), and tarballs can be unpacked automatically, too.

Here's an example kernel command-line parameter for booting into a DDI:

```
rd.systemd.pull=raw,machine,verify=no,blockdev:image:https://192.168.100.1:8081/image.raw root=/dev/disk/by-loop-ref/image.raw-part2
```

This example disables authentication (the `verify=no` option does that), which sounds dangerous, but doesn't really have to be if the referenced disk image is a proper DDI (i.e., carries Verity information and a signature for it).

There's one further twist to all this: the specified download URL can also be just a relative path, and the additional `bootorigin` option can be added. In that case the actual URL to download from is synthesized from the UEFI HTTP boot source URL in combination with the specified relative path.

Or in other words: this integrates really nicely with UEFI HTTP network boot, since the root fs image can be looked for automatically at the same place as the UKI that was booted from was downloaded from.

## Q&A

> **[@mupuf@treehouse.systems](https://social.treehouse.systems/@mupuf)** Nice! Had this existed 5 years ago, I would not have started the boot2container project! Do you think it could provide some sort of caching and avoid running fully from RAM, or is that reimplementing container runtimes too much?

(No direct response recorded in thread)

> **[@philipmolloy](https://mastodon.social/@philipmolloy)** (Query about mkosi and DDI tools)

Yeah, `mkosi` only outputs DDIs. If you want something more raw (i.e., just turn some pre-prepared directory tree into a DDI) use `systemd-repart` with the `-P` option.

> **[@alwayscurious@infosec.exchange](https://infosec.exchange/@alwayscurious)** (Discussion about partition table signing and security)

I don't really grok why that would be desirable though. Generally, Linux file systems must be authenticated before use (because kernel fs drivers are not robust against attacks via fs corruption), which you have to do via `dm-verity`/`dm-crypt`/`dm-integrity` pretty much. But once you did that then they are safe regardless which fs. Signing the part table is unnecessary too, given systemd's image policy logic, which protects things in a more flexible way, since it allows growing partitions to allow for adapting to local systems/disk sizes. Moreover signing part tables would fixate part UUIDs too which means even writable fs for every deployed system would have the same identifiers, which is not just weird but also very broken. (Signature partitions can already carry sigs for many root hashes/partitions, you already have that part hence, if you like). I mean, not sure i grok your security model, but in mine signing part tables/`fstypes` is either counterproductive or even problematic. (In one case systemd's `gpt` dissection logic hard pins an `fstype` btw: for the `esp` we enforce `vfat`, because `esp` is generally not protected cryptographically, and hence needs this kind of stricter logic)

---

[systemd-loop@.service]: https://www.freedesktop.org/software/systemd/man/258/systemd-loop@.service.html
[systemd-repart]: https://www.freedesktop.org/software/systemd/man/258/systemd-repart.html
[mkosi]: https://github.com/systemd/mkosi

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114991974361745422) (2025-08-08)
