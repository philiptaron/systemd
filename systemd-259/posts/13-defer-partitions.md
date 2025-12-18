---
layout: post
title: "--defer-partitions switches"
date: 2025-12-18
source: https://mastodon.social/@pid_eins/115740831317295811
---

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins) | **Posted:** 2025-12-18 13:35 UTC

---

1️⃣3️⃣ Here's the 13th post highlighting key new features of the recently released v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

In episode 7 and 11 of this series we already talked about systemd-repart a bit. Here's another pair of features we added in 259: there are new switches --defer-partitions-empty= and --defer-partitions-factory-reset=. These take a boolean argument, and are closely related to the pre-existing --defer-partitions= switch.

To understand what the new switches do, let's…


---

## Thread Continuation

### [2025-12-18 13:37 UTC](https://mastodon.social/@pid_eins/115740840976597788)

…briefly recap what --defer-partitions= does: it takes a list of partition designators, which allows selecting a subset of partitions of the defined set that shall not be created, but for which space shall be reserved. It's different from --exclude-partitions= which entirely ignores one or more listed partitions, including for the size allocation logic. Example: if you specify --defer-partitions=home you are saying: make sure there's space for a /home partition as per the provided partition…

### [2025-12-18 13:40 UTC](https://mastodon.social/@pid_eins/115740848986287336)

…definitions but don't actually create it nor format it.

What's that useful for? It's good for having a single set of partition definitions, but being able to pick a different subset depending on the context systemd-repart is called in: if it is called as an installer tool (i.e. shall copy an OS from an install medium to a target medium) it makes sense to keep space for local file systems (in particular those which shall be encrypted with a local key), whose creation shall be deferred until…

### [2025-12-18 13:41 UTC](https://mastodon.social/@pid_eins/115740856576798455)

…the first boot. Hence: an installer might want to use --defer-partitions=home,srv with the same partition defs where the boot-time invocation of systemd-repart might want to use no such switch.

I hope this explains a bit what --defer-partitions= is. So what are the new --defer-partitions-empty= and --defer-partitions-factory-reset= about? So here's the thing, the partitions that an installer shall typically not create but leave to the first boot to create are usually partitions also marked…

### [2025-12-18 13:43 UTC](https://mastodon.social/@pid_eins/115740864150948598)

… via Format=empty (which is typically used for the initially unused B partition in an A/B update scheme), or via FactoryReset=yes (which is typically used for the partitions that definitely should be erased on a factory reset because they contain user data as opposed to vendor data).

The two new switches are nothing more than a shortcut to automatically defer partitions marked via these two mechanisms. In 95% of all cases these two switches are what you want to specify for an installer, …

### [2025-12-18 13:44 UTC](https://mastodon.social/@pid_eins/115740866143182201)

… making it unnecessary to manually list all relevant partition types.


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115740831317295811)*