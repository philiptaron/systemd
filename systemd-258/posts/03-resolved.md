---
layout: post
title: "systemd 258 Feature Highlight #3"
date: 2025-05-23
source: https://mastodon.social/@pid_eins/114556401535348313
author: Lennart Poettering
---

3️⃣ Here's the 3rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

systemd-resolved  is a local DNS cache, widely deployed on Linux systems. What makes it different from older solutions is that it manages DNS settings primarily as a per network interface setting, instead of a per system setting. This reflects today's world better where systems tend to be connected to multiple networks at different times (or continously), instead of…

## Thread Continuation

*2025-05-23* ([source](https://mastodon.social/@pid_eins/114556426600380439))

company networks/VPNs often serve their own non-public zones, and thus there is not just "the one DNS", but many, and if in doubt we might need to ask multiple sources at the same time, and take what we can get.

With systemd v258 the query routing logic in systemd-resolved got substantially upgraded: in addition to routing queries to the DNS config of each interface (and optionaly one additional global one), there's now the ability to define arbitrary numbers of additional "delegate zones":

*2025-05-23* ([source](https://mastodon.social/@pid_eins/114556437709396360))

These are basically just combinations of DNS servers along with the domains to match queries with that shall be routed there.

For now this configuration is static (i.e. based on config files), but we hope to open this up to IPC too, i.e. that additional delegate zones can be added and removed any time.

In a way, delegate zones are like adding additional "dummy" network interfaces to the system that come with their own DNS config, but without any real connectivity.

*2025-05-23* ([source](https://mastodon.social/@pid_eins/114557653200869180))

[@equinox](https://chaos.social/@equinox) nah, this change shows that the config sets can relatively easily be made independent of interfaces.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114556416384475176):** …strictly remaining connected to a single network, of which they are considered to be part of – for good. This maps nicely to how DHCP leases work, i.e. that they are handed out individually for each network, have a lifecycle and so on.

This of course means that at any given time multiple DNS server configurations can be active at the same time, and queries must be routed to the right ones. One of resolved's strengths on this is that it accepts a certain level of ambiguity:

company networks/VPNs often serve their own non-public zones, and thus there is not just "the one DNS", but many, and if in doubt we might need to ask multiple sources at the same time, and take what we can get.

With systemd v258 the query routing logic in systemd-resolved got substantially upgraded: in addition to routing queries to the DNS config of each interface (and optionaly one additional global one), there's now the ability to define arbitrary numbers of additional "delegate zones":

## Sources

- [Original post](https://mastodon.social/@pid_eins/114556401535348313)
- [Thread continuation](https://mastodon.social/@pid_eins/114556426600380439)
- [Thread continuation](https://mastodon.social/@pid_eins/114556437709396360)
- [Thread continuation](https://mastodon.social/@pid_eins/114557653200869180)
