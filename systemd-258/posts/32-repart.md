---
layout: post
title: "systemd 258 Feature Highlight #32"
date: 2025-07-14
source: https://mastodon.social/@pid_eins/114850389356673130
author: Lennart Poettering
---

3️⃣2️⃣ Here's the 32st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

systemd-repart is systemd's dynamic repartitioner and disk image (DDIs) builder. One of its strengths is in the area of cryptographic protection: the ability to generate Verity enabled file systems + signing them, and including all that in the final image (file system + Verity data + signature for the top-level root hash).

## Thread Continuation

*2025-07-14* ([source](https://mastodon.social/@pid_eins/114850416985900956))

…there are security models that differ from this, and focus on the protection of the files themselves only, not so much the data structures to access them. While the previously described Verity logic focuses on the block device layer, and is implemented in the kernel subsystem "dm-verity", the latter security model can be implemented via the "fs-verity" subsystem of the kernel, which is available for various file systems, including ext4.

With v258 systemd-repart also supports generating…

*2025-07-14* ([source](https://mastodon.social/@pid_eins/114850427719737809))

…images that make use of fs-verity rather than dm-verity. Or in other words: every file placed in generated images can be locked down with fs-verity, and made immutable. The CopyFiles= setting in repart.d/ drop-ins gained the new "fsverity=" option string, which may be used to enable this logic.

This is useful for building images for consumption by "composefs", usually found in ostree deployments.

*2025-07-14* ([source](https://mastodon.social/@pid_eins/114852456268751759))

[@alwayscurious](https://infosec.exchange/@alwayscurious) fancier programming languages than C won't protect you from algorithmic attacks here, i.e. data structures that are purposefully invalid. 

modern file systems are insanely complex data structures, some of the most complex data structures we deal with every day. which language you use to implement them won't change a bit about that…

*2025-08-07* ([source](https://mastodon.social/@pid_eins/114987636916127145))

[@arrieseveneight](https://hachyderm.io/@arrieseveneight) modern file systems are some of the most complex, largest data structures of today's practical computing. If an attacker can alter them, this is a major attack avenue on the OS kernel, in particular as Linux file system engineers made repeatedly clear that they do not consider block-level attacks on file systems security issues, but regular bugs only — if at all. Thus, it's essential you authenticate the fs blocks *before* they reach the fs drivers.

*2025-08-07* ([source](https://mastodon.social/@pid_eins/114987642304015629))

[@arrieseveneight](https://hachyderm.io/@arrieseveneight) dm-verity provides that, fs-verity doesnt. To me this diminishes the usefulness of fs-verity drastically, i just dont see what precisely the security model behind it is.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114850406617083097):** This kind of protection – so far – focused on block-level protection: not only the files are protected, but their whole arrangement in the data structures of the file system is too. Thus an fs driver can be reasonably sure that if a file system comes from a properly signed Verity-protected image it's structure is safe to access.

While I strongly believe in a security model where trust into file system images must be established before accessing it – in a way like the one describe above –…

…there are security models that differ from this, and focus on the protection of the files themselves only, not so much the data structures to access them. While the previously described Verity logic focuses on the block device layer, and is implemented in the kernel subsystem "dm-verity", the latter security model can be implemented via the "fs-verity" subsystem of the kernel, which is available for various file systems, including ext4.

With v258 systemd-repart also supports generating…

## Sources

- [Original post](https://mastodon.social/@pid_eins/114850389356673130)
- [Thread continuation](https://mastodon.social/@pid_eins/114850416985900956)
- [Thread continuation](https://mastodon.social/@pid_eins/114850427719737809)
- [Thread continuation](https://mastodon.social/@pid_eins/114852456268751759)
- [Thread continuation](https://mastodon.social/@pid_eins/114987636916127145)
- [Thread continuation](https://mastodon.social/@pid_eins/114987642304015629)
