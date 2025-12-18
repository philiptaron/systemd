---
layout: post
title: "DDI partition filtering"
date: 2025-08-15
---

39th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

One thing we make use of a lot in systemd are `DDI`s ("discoverable disk images"), which ultimately are just `GPT` partitioned disk images, which use a variety of `GPT` partition type `UUID`s that somewhat comprehensively describe not just which `OS` a partition belongs to, but how it is supposed to be used.
Emphasis is that `DDI`s carry not only file systems themselves but also supplementary partitions that carry cryptographic metadata (`Verity` + `Verity signatures`), so that they are comprehensively protected both offline and online.

`DDI`s are quite generic and universal: you can package containers in them, system extensions, configuration extensions, portable services, but also the `VM` or bare metal `OS` installations, with a boot loader and kernel, and everything else.

In the latter cases it might make sense to "merge" a `DDI` onto an existing `GPT` formatted disk: i.e. let's say you already have Windows installed, and now you want to add your Linux based `OS` to it that comes as a `DDI`.
That generally works fine, you can do that, just add a bunch more partitions, because the `GPT` partition type `UUID`s that `DDI`s rely on are distinct from those that Windows uses.

But what if you now want to combine multiple Linux based `OS`es on a single disk?

The `GPT` partition type `UUID`s are generic, and shared by both, hence it's not clear anymore by just looking at the `GPT` table how to mount what, and partitions associated with one of the two might end up mounted by the other, in a combination that doesn't really work.

Except that in v258 we have something to address the issue.
Specifically, there's now a `systemd.image_filter=` kernel command line switch.
It takes a shell glob (i.e. an expression with `*` and `?`) that is used when mounting `DDI`s, most importantly for the root disk itself.
The dissection logic will only take partitions into account whose `GPT` partition name string matches that glob.

Or in other words, let's say you maintain your own private `OS` "ToyOS".
Just name all your partitions "ToyOS_xyz" (e.g. "ToyOS_root" or "ToyOS_swap" or so), and then use `systemd.image_filter=ToyOS_*` and the dissection logic will only take partitions into account that are actually associated with your `OS`.

Also note that all the various tools that can deal with `DDI`s in systemd also gained `--image-filter=` as a new switch to accept a similar filtering glob, including of course the `systemd-dissect` tool itself (which is a tool that can be used to look into a `DDI`, and analyze it).

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115032087612846572) (2025-08-15)
