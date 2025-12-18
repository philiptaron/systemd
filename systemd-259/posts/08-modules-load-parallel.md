---
layout: post
title: "modules-load.d parallelization"
date: 2025-11-27
---

8️⃣ Here's the 8th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

[`systemd-modules-load.service`][systemd-modules-load] is an early-boot service that loads a list of kernel modules into the kernel that is configured via `/etc/modules-load.d/` (and similar dirs under `/usr/` + `/run/` as usual).
It's half a legacy feature, because nowadays kernel modules are generally auto-loaded based on "modalias" information they expose, which binds them to certain hardware vendor/product IDs, or to userspace API access (for kmods that implement subsystems rather than device drivers).
However, it's still a popular interface, in particular for certain commercial offerings of... let's say... "questionable" engineering quality.

The `modules-load.d/` interface was never particularly cared for, since all the "good" kmods were so nicely, and efficiently covered by the udev/modalias logic.
With v259 it gets one major improvement however: udev-based module loading has been highly parallelized already (via udev's worker processes), and now we parallelize `modules-load.d/` module loading too: if you have a non-trivial number of modules configured this way this should optimize boot times quite a bit.

(Note that there might actually be "nice" uses of `modules-load.d/` in future.
For example, in certain fixed-function usecases it might make sense to load modules via this infrastructure during boot, and then "blow a fuse" for security reasons to disallow any further kmod loading during later boot.
Because of that I think this parallelization work has been worthwhile, even though I personally might not be too sympathetic to those commercial offerings I mentioned).

---

[systemd-modules-load]: https://www.freedesktop.org/software/systemd/man/259/systemd-modules-load.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115620451885638963) (2025-11-27)
