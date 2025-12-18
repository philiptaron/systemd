---
layout: post
title: "eBPF delegation"
date: 2025-09-17
---

Here's the 55th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Everybody loves `eBPF`, i.e. the Linux kernel's virtual machine for tracing, filtering, security mechanisms and a lot more. Many of the `BPF` concepts are tied to the cgroup hierarchy: you can pin a `BPF` program to a cgroup (and thus a service or container or so), and this will cause it to be applied to all processes running in that cgroup.

One major feature of cgroups is that they are a delegation concept: the top-level cgroups are owned by root, but it can choose to delegate a subgroup or more to some UID, chown() it to it, and then allow it to manage its own subtree there. Whatever manages that can then decide to delegate things further, and so on.

`eBPF` on the other hand has always been a privileged concept mostly: attaching a `BPF` program to a cgroup requires privileges. But a key resource tied to cgroups cannot actually participate in the delegation.

With v258 there are four new settings for unit files: `BPFDelegateCommands=`, `BPFDelegateMaps=`, `BPFDelegatePrograms=`, and `BPFDelegateAttachments=`. These allow delegating certain `BPF` functionality to subcgroups, while prohibiting the rest. This hence allows fine-grained delegation, breaking up the strict requirement to be privileged.

This requires a fairly new kernel that implements `bpf tokens`.

---

## Questions and Answers

> **[@chris_bloke](https://mastodon.acm.org/@chris_bloke)** Am I right in thinking that 6.12 is the first kernel that has `BPF` tokens?

We'd need to check the kernel version, but that aligns with the requirement for a fairly new kernel.

> **[@kmichal](https://fosstodon.org/@kmichal)** "delegating certain `BPF` functionality to subcgroups" the delegation scope for tokens are user namespaces and when you're in such, then you can decorate visible cgroups with allowed `BPF` programs.

That's right - the delegation scope for `BPF` tokens is user namespaces, allowing you to decorate visible cgroups with allowed `BPF` programs when operating within those namespaces.

---

## Reference

- [`systemd.exec` - bpf* configuration options](https://www.freedesktop.org/software/systemd/man/258/systemd.exec.html)

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115218897129957361) (2025-09-17)
