---
layout: post
title: "systemd 258 Feature Highlight #39"
date: 2025-08-15
source: https://mastodon.social/@pid_eins/115032087612846572
author: Lennart Poettering
---

3️⃣9️⃣ Here's the 39th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

One thing we make use of a lot in systemd are DDIs ("discoverable disk images"), which ultimately are just GPT partitioned disk images, which use a variety of GPT partition type UUID that somewhat comprehensively describe not just which OS a partition belongs to, but how it is supposed to be used. Emphasis is that DDIs carry not only file systems themselves but also…

## Thread Continuation

*2025-08-15* ([source](https://mastodon.social/@pid_eins/115032121377549561))

…and everything else. 

In the latter cases it might make sense to "merge" a DDI onto an existing GPT formatted disk: i.e. let's say you already have Windows installed, and now you want to add your Linux based OS to it that comes as a DDI. That generally works fine, you can do that, just add a bunch more partitions, because the GPT partition type UUIDs that DDIs rely on are distinct from those that Windows uses.

But what if you now want to combine multiple Linux based OSes on a single disk?

*2025-08-15* ([source](https://mastodon.social/@pid_eins/115032131943257594))

The GPT partition type UUIDs are generic, and shared by both, hence it's not clear anymore by just looking at the GPT table how to mount what, and partitions associated with one of the too might end up mounted by the other, in a combination that doesn't really work.

Bummer!

Except, that in v258 we have something to address the issue. Specifically, there's now a "systemd.image_filter=" kernel cmdline switch. It takes a shell glob (i.e. an expression with * and ?) that is used when mounting…

*2025-08-15* ([source](https://mastodon.social/@pid_eins/115032140980769328))

…DDIs, most importantly for the root disk itself. The dissection logic will only take partitions into account whose GPT partition name string matches that glob.

Or in other words, let's say you maintain your own private OS "ToyOS". Just name all your partitions "ToyOS_xyz" (e.g. "ToyOS_root" or "ToyOS_swap" or so), and then use "systemd.image_filter=ToyOS_*" and the dissection logic will only take partitions into account that are actually associated with your OS.

Also note that all…

*2025-08-15* ([source](https://mastodon.social/@pid_eins/115032144182821125))

…the various tools that can deal with DDIs in systemd also gained --image-filter= as a new switch to accept a similar filtering glob, including of course the "systemd-dissect" tool itself (which is a tool that can be used to look into a DDI, and analyze it).

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115032105333976517):** …supplementary partitions that carry cryptographic metadata (Verity + Verity signatures), so that they are comprehensively protected both offline and online.

But you probably knew all this already – after all you are following these stories I keep posting here on Mastodon, right?

DDIs are quite generic and universal: you can package containers in them, system extensions, configuration extensions, portable services, but also the VM or bare metal OS installations, with a boot loader and kernel…

…and everything else. 

In the latter cases it might make sense to "merge" a DDI onto an existing GPT formatted disk: i.e. let's say you already have Windows installed, and now you want to add your Linux based OS to it that comes as a DDI. That generally works fine, you can do that, just add a bunch more partitions, because the GPT partition type UUIDs that DDIs rely on are distinct from those that Windows uses.

But what if you now want to combine multiple Linux based OSes on a single disk?

## Sources

- [Original post](https://mastodon.social/@pid_eins/115032087612846572)
- [Thread continuation](https://mastodon.social/@pid_eins/115032121377549561)
- [Thread continuation](https://mastodon.social/@pid_eins/115032131943257594)
- [Thread continuation](https://mastodon.social/@pid_eins/115032140980769328)
- [Thread continuation](https://mastodon.social/@pid_eins/115032144182821125)
