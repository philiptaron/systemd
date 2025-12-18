---
layout: post
title: "systemd 258 Feature Highlight #45"
date: 2025-08-25
source: https://mastodon.social/@pid_eins/115088154755010165
author: Lennart Poettering
---

4️⃣5️⃣ Here's the 45th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

The "feature" for today isn't strictly a feature. This series is supposed to be about features and features only, but today we'll focus on something else: the *removal* of a feature, not the addition of one.

Specifically, v258 is the first release of systemd where cgroupv1 support is gone, removed, dead, of the past, futschikato!

If you are still stuck in cgroupv1 land then v257 is the…

## Thread Continuation

*2025-08-25* ([source](https://mastodon.social/@pid_eins/115088166426127937))

… as long as we didn't have something better!

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115088165140443645):** …last release for you, as systemd v258 cannot boot with the cgroupv1 hierarchy in place anymore.

This allowed us to remove a lot of code and simplify the logic of cgroup handling quite substantially. The removal is not 100% complete, at various places there are still some fragments of support lurking, but the key parts are all gone now.

And if you still run software that doesn't do cgroupv2, then it's really time to get it updated.

Good riddance, cgroupv1, it was a good time with you, …

… as long as we didn't have something better!

## Sources

- [Original post](https://mastodon.social/@pid_eins/115088154755010165)
- [Thread continuation](https://mastodon.social/@pid_eins/115088166426127937)
