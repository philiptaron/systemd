---
layout: post
title: "systemd-repart fs-verity support"
date: 2025-07-14
---

Here's the 32nd post highlighting key new features of the upcoming v258 release of systemd. #systemd258

`systemd-repart` is systemd's dynamic repartitioner and disk image (DDIs) builder. One of its strengths is in the area of cryptographic protection: the ability to generate Verity enabled file systems + signing them, and including all that in the final image (file system + Verity data + signature for the top-level root hash).

This kind of protection so far focused on block-level protection: not only the files are protected, but their whole arrangement in the data structures of the file system is too. Thus an fs driver can be reasonably sure that if a file system comes from a properly signed Verity-protected image it's structure is safe to access.

While there are security models that differ from this, and focus on the protection of the files themselves only, not so much the data structures to access them. While the previously described Verity logic focuses on the block device layer, and is implemented in the kernel subsystem `dm-verity`, the latter security model can be implemented via the `fs-verity` subsystem of the kernel, which is available for various file systems, including `ext4`.

With v258 `systemd-repart` also supports generating images that make use of `fs-verity` rather than `dm-verity`. Or in other words: every file placed in generated images can be locked down with `fs-verity`, and made immutable. The `CopyFiles=` setting in `repart.d/` drop-ins gained the new `fsverity=` option string, which may be used to enable this logic.

This is useful for building images for consumption by `composefs`, usually found in `ostree` deployments.

---

> **[@arrieseveneight](https://hachyderm.io/@arrieseveneight)** (Aug 7) Sorry if this is necroposting, but what are the practical advantages to validating at the block device layer as opposed to the file layer? is it down to simplicity, are there any other types of attacks that it prevents, or?

Modern file systems are some of the most complex, largest data structures of today's practical computing. If an attacker can alter them, this is a major attack avenue on the OS kernel, in particular as Linux file system engineers made repeatedly clear that they do not consider block-level attacks on file systems security issues, but regular bugs only — if at all. Thus, it's essential you authenticate the fs blocks *before* they reach the fs drivers.

> **[@arrieseveneight](https://hachyderm.io/@arrieseveneight)** (Aug 7) Thanks so much for explaining, that clears things up!

`dm-verity` provides that, `fs-verity` doesn't. To me this diminishes the usefulness of `fs-verity` drastically, I just don't see what precisely the security model behind it is.

> **[@alwayscurious](https://infosec.exchange/@alwayscurious)** (Jul 14) Wanting to access files on a filesystem that is not fully trusted, without having to copy the entire block device, is a valid use case. Sadly, current filesystem drivers do not support it, for which I blame the C language more than anything else.

Fancier programming languages than C won't protect you from algorithmic attacks here, i.e. data structures that are purposefully invalid. Modern file systems are insanely complex data structures, some of the most complex data structures we deal with every day. Which language you use to implement them won't change a bit about that…

> **[@alwayscurious](https://infosec.exchange/@alwayscurious)** (Jul 14) What they *do* prevent is memory unsafety leading to code execution in the driver. That said, Linux being a monolithic kernel is also a huge part of the problem. If every filesystem used `FUSE` then the impact would be limited to the driver for the filesystem, and microkernels have much faster `IPC` which should mitigate much of the performance impact.

---

[systemd-repart]: https://www.freedesktop.org/software/systemd/man/258/systemd-repart.html
[dm-verity]: https://www.freedesktop.org/software/systemd/man/258/dm-verity.html
[fs-verity]: https://www.freedesktop.org/software/systemd/man/258/fs-verity.html
[composefs]: https://www.freedesktop.org/software/systemd/man/258/composefs.html
[ostree]: https://ostree.readthedocs.io/

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114850389356673130) (2025-07-14)
