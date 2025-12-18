---
layout: post
title: "systemd 258 Feature Highlight #55"
date: 2025-09-17
source: https://mastodon.social/@pid_eins/115218897129957361
author: Lennart Poettering
---

5️⃣5️⃣ Here's the 55th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Everybody loves eBPF, i.e. the Linux kernel's virtual machine for tracing, filtering, security mechanisms and a lot more. Many of the BPF concepts are tied to the cgroup hierarchy: you can pin a BPF program to a cgroup (and thus a service or container or so), and this will cause it to be applied to all processes running in that cgroup.

## Thread Continuation

*2025-09-17* ([source](https://mastodon.social/@pid_eins/115218915414102719))

…but a key resource tied to cgroups cannot actually participate in the delegation. Sniff! 😥

Well, no more! 🤔

With v258 there are four new settings for unit files: BPFDelegateCommands=, BPFDelegateMaps=, BPFDelegatePrograms=, BPFDelegateAttachments=. These allow delegating certain BPF functionality to subcgroups, while prohibiting the rest. This hence allows fine grained delegation, breaking up the strict requirement to be privileged. 🤓 ✨

*2025-09-17* ([source](https://mastodon.social/@pid_eins/115218930829429917))

This requires a fairly new kernel that implements "bpf tokens".

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115218905911471984):** One major feature of cgroups is that they are a delegation concept: the top-level cgroups are owned by root, but it can choose to delegate a subgroup or more to some UID, chown() it to it, and then allow it to manage its own subtree there. Whatever manages that can then decide to delegate things further, and so on.

eBPF on the other hand has always been a privileged concept mostly: attaching a BPF program to a cgroup requires privs. So, … uh, … now we have this nice delegation concept, …

…but a key resource tied to cgroups cannot actually participate in the delegation. Sniff! 😥

Well, no more! 🤔

With v258 there are four new settings for unit files: BPFDelegateCommands=, BPFDelegateMaps=, BPFDelegatePrograms=, BPFDelegateAttachments=. These allow delegating certain BPF functionality to subcgroups, while prohibiting the rest. This hence allows fine grained delegation, breaking up the strict requirement to be privileged. 🤓 ✨

## Sources

- [Original post](https://mastodon.social/@pid_eins/115218897129957361)
- [Thread continuation](https://mastodon.social/@pid_eins/115218915414102719)
- [Thread continuation](https://mastodon.social/@pid_eins/115218930829429917)
