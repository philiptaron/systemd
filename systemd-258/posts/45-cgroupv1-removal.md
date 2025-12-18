---
layout: post
title: "cgroupv1 removal"
date: 2025-08-25
---

45 Here's the 45th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

The "feature" for today isn't strictly a feature. This series is supposed to be about features and features only, but today we'll focus on something else: the *removal* of a feature, not the addition of one.

Specifically, v258 is the first release of systemd where `cgroupv1` support is gone, removed, dead, of the past, futschikato!

If you are still stuck in `cgroupv1` land then v257 is the last release for you, as systemd v258 cannot boot with the `cgroupv1` hierarchy in place anymore.

This allowed us to remove a lot of code and simplify the logic of cgroup handling quite substantially. The removal is not 100% complete, at various places there are still some fragments of support lurking, but the key parts are all gone now.

And if you still run software that doesn't do `cgroupv2`, then it's really time to get it updated.

Good riddance, `cgroupv1`, it was a good time with you, as long as we didn't have something better!

---

## Community responses

> **tapeloop** You mean it's passed on? As in this feature is no more! It has ceased to be! It's expired and gone to meet its maker! It's a stiff! Bereft of life, it rests in peace! If you hadn't nailed it to the perch it'd be pushing up the daisies! Its metabolic processes are now history! It's off the twig! It's kicked the bucket, it's shuffled off its mortal coil, run down the curtain and joined the bleedin' choir invisible!! THIS IS AN EX-FEATURE!!

Indeed, that's quite fitting.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115088154755010165) (2025-08-25)
