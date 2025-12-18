---
layout: post
title: "systemd 258 Feature Highlight #29"
date: 2025-07-08
source: https://mastodon.social/@pid_eins/114816786836736040
author: Lennart Poettering
---

2️⃣9️⃣ Here's the 29th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Among (many) other things systemd's service manager is also a resource manager. It can assign CPU, IO, memory resources to services, measure their use, and apply live modifications to it.

There's one fundamental type of resource it so far didn't manage per-service however: disk space. With v258 we are changing that.

## Thread Continuation

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114816812681603385))

Because it runs unprivileged it can't create the directory itself, hence the service manager can help.
2. About life-cycle: when a service is uninstalled from a system it makes sense to also remove its state resources. "systemctl cleanup" helps you with that, removing the directories configured for a unit with this.
3. Simply for informational purposes, in particular for 3rd party tools: it's very useful if any tool or admin can query systemd about the place a service puts its state.

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114816825898188571))

With v258 we are adding a 4th reason to declare directories like this:
4. There is now StateDirectoryAccounting= and StateDirectoryQuota= for accounting disk usage per-service, and for enforcing limits on it. (similar options for the other two dirs exist too) 

These fields can be set during runtime via "systemctl set-property". They are implemented via new-style "quota project IDs", which are fully automatically managed (i.e. no need to patch around in /etc/projid), …

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114816835917225081))

…and thus compatible with xfs and ext4. Unfortunately, the concept is not compatible with btrfs yet, because quota works completely differently on btrfs, and quite frankly the differing semantics don't make it easy to hook it up the same way (speficially: we enable project quota for arbitrary existing inodes during runtime, we cannot do something equivalent on btrfs, we'd have to create new inodes, but that would be visible to running services).

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114816837188951581))

But we'll see, maybe we find a way to make btrfs work for us too. Who knows.

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114817336159098174))

[@shoragan](https://chaos.social/@shoragan) no. Lack of support on tmpfs is precisely the reason why we didnt expose RuntimeDirectoryQuota= at this time, but only did it for the other dir types.

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114817338507424459))

[@AntonAttano](https://infosec.exchange/@AntonAttano) the latter

*2025-07-08* ([source](https://mastodon.social/@pid_eins/114817967525907613))

[@balki](https://social.balki.me/@balki) there are dbus props.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114816802689497833):** As you might know systemd has supported per-unit StateDirectory=, CacheDirectory= and LogsDirectory= settings for a longer time, that define per-service directories that shall be created when the service is invoked and where the service can put its resources.

So far, defining these directories was mostly about three things:
1. About privileges: a service declared to run under an unprivileged user ID needs a place to put its state data – a place to which it has full read + write access.

Because it runs unprivileged it can't create the directory itself, hence the service manager can help.
2. About life-cycle: when a service is uninstalled from a system it makes sense to also remove its state resources. "systemctl cleanup" helps you with that, removing the directories configured for a unit with this.
3. Simply for informational purposes, in particular for 3rd party tools: it's very useful if any tool or admin can query systemd about the place a service puts its state.

> **[@balki@balki.me](https://social.balki.me/@balki/statuses/01JZN4C42VRPAX90PNDTYQ8CAZ):** [@pid_eins](https://mastodon.social/@pid_eins) I enable CPU/IO/IP accounting. But there does not seem to be a way to read this information programmatically for integration with other tools. Only way seem to be to use systemctl status | awk ... which is not very robust.

[@balki](https://social.balki.me/@balki) there are dbus props.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114816786836736040)
- [Thread continuation](https://mastodon.social/@pid_eins/114816812681603385)
- [Thread continuation](https://mastodon.social/@pid_eins/114816825898188571)
- [Thread continuation](https://mastodon.social/@pid_eins/114816835917225081)
- [Thread continuation](https://mastodon.social/@pid_eins/114816837188951581)
- [Thread continuation](https://mastodon.social/@pid_eins/114817336159098174)
- [Thread continuation](https://mastodon.social/@pid_eins/114817338507424459)
- [Thread continuation](https://mastodon.social/@pid_eins/114817967525907613)
