---
layout: post
title: "Varlink IPC for systemd-repart"
date: 2025-12-04
source: https://mastodon.social/@pid_eins/115662198906484836
---

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins) | **Posted:** 2025-12-04 16:18 UTC

---

1️⃣1️⃣ Here's the 11th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

In episode 7 of this series we already talked briefly about systemd-repart. There's another addition to systemd-repart in v259: there's now a pretty useful Varlink IPC available to systemd-repart.

It's generally useful, but I put it together with one use-case in mind in particular: to make systemd-repart useful for use in graphical installers. After all one of the things, …


---

## Thread Continuation

### [2025-12-04 16:33 UTC](https://mastodon.social/@pid_eins/115662260764497398)

… that systemd-repart is really good at is setting up a partition table, streaming file system data into it, and setting up newly formatted/encrypted file systems. But that's precisely what an interactive installer is doing, in particular for image based OSes, where the initial installation is literally just streaming a file system image 1:1 onto a new disk.

systemd-repart's Varlink IPC interface is available in two modes: you can either contact it via an AF_UNIX socket in the fs, or…

### [2025-12-04 16:36 UTC](https://mastodon.social/@pid_eins/115662270768337691)

…you can fork it off your process, and talk Varlink via an AF_UNIX socketpair(). The latter is particularly useful if a highly privileged worker process is in the mix, that drives repart plus a boot loader/kernel installer.

In fact, I already have a PR posted for v260 that adds such a worker service, that drives repart + kernel-install + bootctl + systemd-creds in a unified tool that can install an image based OS.

The Varlink interface can do a couple of more things, for example enumerate…

### [2025-12-04 16:37 UTC](https://mastodon.social/@pid_eins/115662273665523002)

…suitable block devices for installations (because that's actually not as trivial an op as one might think).


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115662198906484836)*