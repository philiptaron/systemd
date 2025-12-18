---
layout: post
title: "Hostname pattern matching"
date: 2025-05-28
---

5th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258) [#systemd](https://mastodon.social/tags/systemd)

On modern Linux systems the persistent hostname is configured in `/etc/hostname`.
Linux people treating their devices like pets tend to come up with nice, imaginative names for their hosts.

But this doesn't scale: if you have a large number of devices to manage (i.e. "cattle") then you typically want something more automatic: the hostnames used should follow some specific pattern, but also have some more dynamic part in it.
Often deployments use tech like DHCP leases or cloud provisioning tools to set hostnames like this.

With v258 we are adding a simple way to do this locally, in a deterministic fashion, without requiring any further infrastructure:
if the `/etc/hostname` file contains question mark characters, those are implicitly and automatically replaced by hex digits hashed from `/etc/machine-id` when processed.

Or in other words, you can set `/etc/hostname` to something like `mycorp-????-????-devel` and it will result in hostnames such as `mycorp-ae78-f1c5-devel` being set on the system, or something similar, depending on your `/etc/machine-id`.

Or in even other words: you can relatively freely choose the basic pattern to use for naming, but also make the names distinct for each system, in a somewhat deterministic way.
(well, deterministic in the sense that you accept `/etc/machine-id` is an input to your system, not an output)

Note that you can use as many question marks as you like (well, you probably shouldn't use more than 63 chars for the whole hostname, since that's the maximum length of a DNS label, and also the limit the Linux kernel enforces on the local hostname).
But of course, keep the birthday paradox in mind when picking the number of question marks, since you probably want to avoid accidental hostname clashes in your fleet.
There's a reason why UUIDs are 128bit long (i.e. 32 hex chars)...

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114584855720355892) (2025-05-28)
