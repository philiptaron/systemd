---
layout: post
title: "systemd 258 Feature Highlight #20"
date: 2025-06-20
source: https://mastodon.social/@pid_eins/114715785929761972
author: Lennart Poettering
---

2️⃣0️⃣ Here's the 20th  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Kernel files systems learn new mount options all the time. Often one wants to enable an option in a graceful fashion: if the kernel is new enough and provides the mount option, use it – and if not, then not.

We ran into this problem when we enabled quota support on tmpfs (see other story in this series): only new kernels support it, old kernels do not.

## Thread Continuation

*2025-06-20* ([source](https://mastodon.social/@pid_eins/114715805914205248))

If the kernel supports that mount option it is added as regular mount option to the option string, but if it does not, its is suppressed. The tmp.mount unit hence uses this option setting now:

Options=mode=1777,strictatime,nosuid,nodev,size=50%%,nr_inodes=1m,x-systemd.graceful-option=usrquota

This works for any kernel mount option, not just the quota options. However, it will *not* work for userspace mount options, that some file systems support, in particular fuse ones.

*2025-06-20* ([source](https://mastodon.social/@pid_eins/114715808925831418))

(If you try anyway to use userspace mount options with this new pseudo-option then the mount option will be assumed to be unsupported, i.e. the setting has no effect).

*2025-06-20* ([source](https://mastodon.social/@pid_eins/114715829955310349))

[@agowa338](https://chaos.social/@agowa338) Two reasons: this implies per-user mount namespaces, so that /tmp/ can be over-mounted.  This also means that we need to disable mount propagation from user namespace to host somewhat (because otherwise the per-user tmpfs would propagate too, which is after all explicitly not what we want). But that also means many mounts can no longer established from user context, because noone else would see them. Which might be OK in some scenarios, but is not universally accepted as OK.

*2025-06-20* ([source](https://mastodon.social/@pid_eins/114715838423705824))

[@agowa338](https://chaos.social/@agowa338) And then there's the other thing: applications use /tmp/ not just for storing temporary stuff, but also as a way to communicate, and that breaks when you disassociate /tmp/ for each user. For example X11 puts its sockets there, mysql used to, as well. It's all pretty awful, but we probably cannot ignore that this is done.

*2025-06-20* ([source](https://mastodon.social/@pid_eins/114715844329384763))

[@agowa338](https://chaos.social/@agowa338) PrivateTmp= as service setting works because it is opt-in, and per service, so that one can decide for each service individually if mount prop being off is a problem, or if they use /tmp/ for communication.  But doing this blanket for all user process is likely going to piss off a lot of people.

*2025-06-20* ([source](https://mastodon.social/@pid_eins/114715845996461084))

[@agowa338](https://chaos.social/@agowa338) I am not saying we shouldn't do this eventually, but it's certainly not a clear-cut "let's just do this" thing.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114715797495392444):** While user quota on /tmp/ is certainly an important feature to lock down what bad code can do with this highly problematic directory, one can argue that not enabling it is also OK, after all this is how this worked for the last decades. Hence, being able to use the new knob, but gracefully suppress it on old kernels makes a lot of sense.

With the new x-systemd.graceful-option= pseudo mount option we implement a way out for this, in v258. As argument it takes a mount option string.

If the kernel supports that mount option it is added as regular mount option to the option string, but if it does not, its is suppressed. The tmp.mount unit hence uses this option setting now:

Options=mode=1777,strictatime,nosuid,nodev,size=50%%,nr_inodes=1m,x-systemd.graceful-option=usrquota

This works for any kernel mount option, not just the quota options. However, it will *not* work for userspace mount options, that some file systems support, in particular fuse ones.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114715785929761972)
- [Thread continuation](https://mastodon.social/@pid_eins/114715805914205248)
- [Thread continuation](https://mastodon.social/@pid_eins/114715808925831418)
- [Thread continuation](https://mastodon.social/@pid_eins/114715829955310349)
- [Thread continuation](https://mastodon.social/@pid_eins/114715838423705824)
- [Thread continuation](https://mastodon.social/@pid_eins/114715844329384763)
- [Thread continuation](https://mastodon.social/@pid_eins/114715845996461084)
