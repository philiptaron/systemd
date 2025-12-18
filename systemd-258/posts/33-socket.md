---
layout: post
title: "systemd 258 Feature Highlight #33"
date: 2025-08-06
source: https://mastodon.social/@pid_eins/114980359479311999
author: Lennart Poettering
---

3️⃣3️⃣ Here's the 33rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

The Linux kernel recently gained two new socket options (as in getsockopt() commands) for AF_UNIX sockets: SO_PASSPIDFD and SO_PASSRIGHTS. The former complements SO_PASSCREDS (which a receiver can set and ensures that sender UID/GID/PID information identifying the sender is sent along with payload on the socket). It simply sends a stable, new-style pidfd reference instead of a plain pid…

## Thread Continuation

*2025-08-06* ([source](https://mastodon.social/@pid_eins/114980383786137619))

…problematic, since it's relatively easy to create fds that will block for a long time if closed.

Long story short: both mechanisms are major improvements when writing secure AF_UNIX services. And hence with v258 they are now exposed via the new AcceptFileDescriptor= and PassPIDFD= .socket unit file settings.

(Ideally, we'd just default to AcceptFileDescriptor= to off for security reasons, but that would be a major compat break I guess).

*2025-08-06* ([source](https://mastodon.social/@pid_eins/114980994968799619))

[@jamesh](https://aus.social/@jamesh) that's why we have it on the .socket units now so that you can enable it before listen() or connect() and thus is effectively always in effect.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114980371146654596):** …along with the payload. The latter may be used by a receiver to control whether it is willing to accept arbitrary file descriptors being sent over an AF_UNIX socket and installed in its file descriptor table. The latter in particular addresses a major gap on the security model of AF_UNIX sockets: for the first time accepting fds can be turned off! 

Previously that was always enabled if one dared to use the recvmsg() syscall (instead of recvfrom(), recv() or read()) – and that's quite…

…problematic, since it's relatively easy to create fds that will block for a long time if closed.

Long story short: both mechanisms are major improvements when writing secure AF_UNIX services. And hence with v258 they are now exposed via the new AcceptFileDescriptor= and PassPIDFD= .socket unit file settings.

(Ideally, we'd just default to AcceptFileDescriptor= to off for security reasons, but that would be a major compat break I guess).

> **[@jamesh@aus.social](https://aus.social/@jamesh/114980735937065001):** [@pid_eins](https://mastodon.social/@pid_eins) does it have the same issue as SO_PASSCRED that packets sent before either end has enabled the socket option won't have credentials attached?

[@jamesh](https://aus.social/@jamesh) that's why we have it on the .socket units now so that you can enable it before listen() or connect() and thus is effectively always in effect.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114980359479311999)
- [Thread continuation](https://mastodon.social/@pid_eins/114980383786137619)
- [Thread continuation](https://mastodon.social/@pid_eins/114980994968799619)
