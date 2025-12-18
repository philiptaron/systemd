---
layout: post
title: "`PrivateUsers=` namespace sandboxing"
date: 2025-09-10
---

Here's the 52nd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

`PrivateUsers=` is one of the many sandboxing knobs in service unit files. It configures a minimal user namespace for the service code to run in. Previously you could set it to `self`, which would set up the user namespace mapping for the service to map the root user and the service's user to itself, and leave everything else unmapped.

Setting the knob to `self` would somewhat disconnect the service from the host user table: all inodes, processes, and other objects it sees will be owned by itself, by `root`, or by the `nobody` user (which is where unmapped users are mapped to).

In v257, the setting learned a new value `identity`. If used, the first 64K users plus the service's own user (if outside the 64K range) would be mapped, nothing else. In other words, the service would be limited to the 16-bit UID range.

With v258, a third value has been added: `full`. If used, the user namespace's UID mapping would map all 2^32 UIDs to themselves. You might wonder: what's the point of a user namespace if it has a full mapping of the host UID range without altering anything? Here's the thing: user namespaces are not just about mappings, they also make various operations inaccessible to processes contained in them, and they can "own" other namespace types.

---

> **[@markstos](https://urbanists.social/@markstos)** Will this help rootless podman to run as a systemd service? Currently setting `User=` to run a podman service doesn't work without hacks.

I don't have information addressing this specific use case yet. Additional context from Lennart on this would be helpful.

---

[systemd]: https://www.freedesktop.org/software/systemd/man/258/systemd.exec.html#PrivateUsers=

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115179113138417200) (2025-09-10)
