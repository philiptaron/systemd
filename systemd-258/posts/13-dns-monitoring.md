---
layout: post
title: "DNS monitoring and configuration subscriptions"
date: 2025-06-10
---

One of `systemd-resolved`'s fundamental jobs is to maintain per-interface and global DNS configuration (as well as per-delegate configuration, as described earlier in this series). We always provided D-Bus APIs to query the current state of this, and `resolvectl` to a large degree is just a wrapper around that.

In v258 we updated this area substantially. There's now a Varlink IPC call to subscribe to all DNS configuration changes: `io.systemd.Resolve.Monitor.SubscribeDNSConfiguration()` on `/run/systemd/resolve/io.systemd.Resolve.Monitor`.

If you issue this you'll get a stream of updates of the DNS configuration as they happen.

Why is this useful? This is used by `systemd-networkd-wait-online`'s new `--dns` switch. If specified it will not only wait until a suitable IP configuration shows up, but also wait until a DNS configuration is acquired as well, making the whole logic more robust regarding dynamic network configuration.

And in case you wonder what `systemd-networkd-wait-online` is good for: on systems that boot off the network it makes sense to delay attempts to contact the boot servers until the moment networking is fully established (but no longer), so that no time is wasted on pointless retry cycles unnecessarily.

---

## Discussion

> **Aaron Sawdey** I thought systemd-resolved's job was to make it impossible for me to control what nameservers were used

My educated guess is that your network config says: pick up DNS config from IPv6 RA advertisements, and your IPv6 network sends those out.

I have no idea about netplan, I don't grok why one would need that, but maybe check what you configured there.

Also try `networkctl status` which shows you the current configuration in effect.

> **amackif** Would this help in a situation where on client PC .mount unit would be used to mount samba/NFS share, but via hostname instead of a fixed IP?

Yeah, that might help in some scenarios like yours.

---

[systemd-resolved]: https://www.freedesktop.org/software/systemd/man/258/systemd-resolved.html
[systemd-networkd]: https://www.freedesktop.org/software/systemd/man/258/systemd-networkd.html
[systemd-networkd-wait-online]: https://www.freedesktop.org/software/systemd/man/258/systemd-networkd-wait-online.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114658726594933395) (2025-06-10)
