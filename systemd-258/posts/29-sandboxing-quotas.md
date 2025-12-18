---
layout: post
title: "Service disk quotas"
date: 2025-07-08
---

Among (many) other things systemd's service manager is also a resource manager.
It can assign CPU, IO, memory resources to services, measure their use, and apply live modifications to it.

There's one fundamental type of resource it so far didn't manage per-service however: disk space.
With v258 we are changing that.

As you might know systemd has supported per-unit `StateDirectory=`, `CacheDirectory=` and `LogsDirectory=` settings for a longer time, that define per-service directories that shall be created when the service is invoked and where the service can put its resources.

So far, defining these directories was mostly about three things:

1. About privileges: a service declared to run under an unprivileged user ID needs a place to put its state data – a place to which it has full read + write access.

---

> **@shaman007** so we'll have k8s at home 🙂

> **@alina** i do this with mount namespaces in the systemd nixos wrapper i wrote

> **@balki** I enable CPU/IO/IP accounting. But there does not seem to be a way to read this information programmatically for integration with other tools. Only way seem to be to use `systemctl status | awk ...` which is not very robust.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114816786836736040) (2025-07-08)
