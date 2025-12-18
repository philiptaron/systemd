---
layout: post
title: "systemd 258 Feature Highlight #13"
date: 2025-06-10
source: https://mastodon.social/@pid_eins/114658726594933395
author: Lennart Poettering
---

1️⃣3️⃣ Here's the 13th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

One of systemd-resolved's fundamental jobs is to maintain per-interface and global DNS configuration (as well as per-delegate configuration, as described earlier in this series). We always provided D-Bus APIs to query the current state of this, and "resolvectl" to a large degree is just a wrapper around that.

## Thread Continuation

*2025-06-10* ([source](https://mastodon.social/@pid_eins/114658766477192784))

…a suitable IP configuration shows up, but also wait until a DNS configuration is acquired as well, making the whole logic more robust regarding dynamic network configuration.

And in case you wonder what systemd-networkd-wait-online is good for: on systems that boot off the network it makes sense to delay attempts to contact the boot servers until the moment networking is fully established (but no longer), so that no time is wasted on pointless retry cycles unnecessarily.

*2025-06-11* ([source](https://mastodon.social/@pid_eins/114663584209221942))

[@acsawdey](https://fosstodon.org/@acsawdey) [@sandro](https://c3d2.social/@sandro) My educated guess is that your network config says: pick up DNS config from IPv6 RA advertisments, and your IPv6 network sends those out.

I have no idea about netplan, I don't grok why one would need that, but maybe check what you configured there.

Also try "networkctl status" which shows you the current configuration in effect.

*2025-07-02* ([source](https://mastodon.social/@pid_eins/114782843270822327))

[@amackif](https://mastodon.social/@amackif) yeah, that might help in some scenarios like yours

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114658757452129500):** In v258 we updated this area substantially. There's now a Varlink IPC call to subscribe to all DNS configuration changes (io.systemd.Resolve.Monitor.SubscribeDNSConfiguration() on /run/systemd/resolve/io.systemd.Resolve.Monitor).

If you issue this you'll get a stream of updates of the DNS configuration as they happen.

Why is this useful? This is used by systemd-networkd-wait-online's new --dns switch. If specified it will not only wait until a suitable network interface with…

…a suitable IP configuration shows up, but also wait until a DNS configuration is acquired as well, making the whole logic more robust regarding dynamic network configuration.

And in case you wonder what systemd-networkd-wait-online is good for: on systems that boot off the network it makes sense to delay attempts to contact the boot servers until the moment networking is fully established (but no longer), so that no time is wasted on pointless retry cycles unnecessarily.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114658726594933395)
- [Thread continuation](https://mastodon.social/@pid_eins/114658766477192784)
- [Thread continuation](https://mastodon.social/@pid_eins/114663584209221942)
- [Thread continuation](https://mastodon.social/@pid_eins/114782843270822327)
