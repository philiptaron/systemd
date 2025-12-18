---
layout: post
title: "systemd-resolved delegate zones"
date: 2025-05-23
---

Here's the 3rd post highlighting key new features of the upcoming v258 release of systemd.

`systemd-resolved` is a local DNS cache, widely deployed on Linux systems.
What makes it different from older solutions is that it manages DNS settings primarily as a per network interface setting, instead of a per system setting.
This reflects today's world better where systems tend to be connected to multiple networks at different times (or continuously), instead of strictly remaining connected to a single network, of which they are considered to be part of for good.
This maps nicely to how DHCP leases work, i.e. that they are handed out individually for each network, have a lifecycle and so on.

This of course means that at any given time multiple DNS server configurations can be active at the same time, and queries must be routed to the right ones.
One of resolved's strengths on this is that it accepts a certain level of ambiguity:

Company networks/VPNs often serve their own non-public zones, and thus there is not just "the one DNS", but many, and if in doubt we might need to ask multiple sources at the same time, and take what we can get.

With systemd v258 the query routing logic in `systemd-resolved` got substantially upgraded: in addition to routing queries to the DNS config of each interface (and optionally one additional global one), there's now the ability to define arbitrary numbers of additional "delegate zones":

These are basically just combinations of DNS servers along with the domains to match queries with that shall be routed there.
For now this configuration is static (i.e. based on config files), but we hope to open this up to IPC too, i.e. that additional delegate zones can be added and removed any time.
In a way, delegate zones are like adding additional "dummy" network interfaces to the system that come with their own DNS config, but without any real connectivity.

---

> **[@equinox](https://chaos.social/@equinox):** are you aware DNS settings have been made part of PvDs 10 years ago? RFC7556.
> The ultimate takeaway (after you follow down the rathole and discard overly complex/dead approaches) is that distinct IPv6 LL addresses advertising distinct prefixes in RA/PIOs need to be treated as distinct networks on the same interface.
> Either way, you need multiple distinct sets per interface.
> (Good that we're catching up from 20 years ago to 10 years ago, but can we get to now?)

nah, this change shows that the config sets can relatively easily be made independent of interfaces.

> **[@quantum](https://mastodon.online/@quantum):** dns over https will it be enabled in this release?

(No direct response recorded)

---

[systemd-resolved]: https://www.freedesktop.org/software/systemd/man/258/systemd-resolved.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114556401535348313) (2025-05-23)
