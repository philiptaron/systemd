---
layout: post
title: "systemd 258 Feature Highlight #11"
date: 2025-06-05
source: https://mastodon.social/@pid_eins/114629842058448119
author: Lennart Poettering
---

1️⃣1️⃣ Here's the 11th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Sometimes, when debugging the early boot process of Linux userspace it's useful to acquire a shell at various points of progress, and delaying further boot-up until that shell has exited.

The dracut initrd generator has supported a concept for this for a longer time: the rd.break= kernel command line option defines a bunch of "breakpoints" that give you just that during the initrd phase.

## Thread Continuation

*2025-06-05* ([source](https://mastodon.social/@pid_eins/114629866890064810))

First of all, the concept is so useful, we want it on the host too, i.e. have additional breakpoints *after* the initrd→host transition, and that means Dracut is no longer in control then.

Secondly, there's a push towards avoiding initrd generators altogether and instead building initrds just like any other OS disk image (see for example mkosi-initrd), directly from distro packages, using the same codepaths as are used after the initrd→host transition.

*2025-06-05* ([source](https://mastodon.social/@pid_eins/114629878208264230))

In such a non-Dracut world it's very useful to have the breakpoint concept too.

TLDR: starting with v258 you can add rd.systemd.break=pre-udev to the kernel cmdline and get a pretty early interactive shell to debug stuff.

*2025-06-05* ([source](https://mastodon.social/@pid_eins/114630881203901302))

[@Sparky](https://the.gayest.dev/@Sparky) you certainly can. But only really in very simple setups. Thing is anything non-trivial really should do disk encryption for the rootfs and that implies some userspace. Either to do the tpm stuff, or to query user for pw, or to do fido2. Its not going to happen that the kernel will do all that itself

But sure if you have a very simple device, dont care about authentication/encryption of the basic OS file systems and have no complex storage, sure you can do without initrd, already today.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114629855185345468):** With systemd v258 we are supporting equivalent functionality natively in systemd. Specifically, there's now systemd.break= and rd.systemd.break= on the kernel command line that give you roughly equivalent functionality.

This is implemented in systemd-debug-generator, which already provides support for a bunch of other debugging tools.

Why implement in the systemd suite? Why isn't the Dracut implementation good enough? Two reasons primarily:

First of all, the concept is so useful, we want it on the host too, i.e. have additional breakpoints *after* the initrd→host transition, and that means Dracut is no longer in control then.

Secondly, there's a push towards avoiding initrd generators altogether and instead building initrds just like any other OS disk image (see for example mkosi-initrd), directly from distro packages, using the same codepaths as are used after the initrd→host transition.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114629842058448119)
- [Thread continuation](https://mastodon.social/@pid_eins/114629866890064810)
- [Thread continuation](https://mastodon.social/@pid_eins/114629878208264230)
- [Thread continuation](https://mastodon.social/@pid_eins/114630881203901302)
