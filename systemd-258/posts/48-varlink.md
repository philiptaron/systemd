---
layout: post
title: "systemd 258 Feature Highlight #48"
date: 2025-08-29
source: https://mastodon.social/@pid_eins/115114274588524270
author: Lennart Poettering
---

4️⃣8️⃣ Here's the 48th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

systemd-machined is a small service in systemd that can keep track of running VMs and full-OS containers, and provides various APIs via D-Bus to interact with them. It also integrates with NSS to do name resolution for these systems.

With v258 systemd-machined gained a pretty comprehensive set of new APIs, via Varlink.

## Thread Continuation

*2025-08-29* ([source](https://mastodon.social/@pid_eins/115114294194938972))

(But fear not, D-Bus support is going to stay, we are pluralistic in that sense, we just believe Varlink is a lot more attractive for a good chunk of uses, in particular in the server/web world, where JSON is much more common.)

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115114291884097962):** The new interfaces are pretty comprehensive and the D-Bus and Varlink API coverage of functionality should be very similar now.

This should be seen as part of our process of moving our focus away from D-Bus IPC and more towards Varlink IPC, in particular for services that are not so much desktop-affine but more relevant for server applications.

(But fear not, D-Bus support is going to stay, we are pluralistic in that sense, we just believe Varlink is a lot more attractive for a good chunk of uses, in particular in the server/web world, where JSON is much more common.)

## Sources

- [Original post](https://mastodon.social/@pid_eins/115114274588524270)
- [Thread continuation](https://mastodon.social/@pid_eins/115114294194938972)
