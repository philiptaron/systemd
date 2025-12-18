---
layout: post
title: "Service Sandbox Debugging"
date: 2025-07-09
---

systemd's service sandboxing logic builds heavily on Linux `mount` namespacing, as well as other types of process namespacing. It primarily uses this to take away access to certain subhierarchies—marking them read-only, unmounting them, or overmounting them with something else—but it also allows you to rearrange things (for example, `bind mount` one directory onto another, obstructing access to it).

This is all very efficient to secure services, but it's also a bit opaque: since it's the daemon you sandbox, and your admin tools are outside of that sandbox it's sometimes hard to analyze how the daemon sees things.

No more. With v258 there's a new verb `unit-shell` in `systemd-analyze`. You specify a service name, and it opens you a shell inside that specified service's sandbox (which must be running for this). You can look around and check if everything is like you expected it to be.

## How it works

In a way this is somewhat equivalent to `nsenter -a -p $(systemctl show -P MainPID $UNIT)`, but this new tool is a bit more careful and nicely integrated into our tool set. It's lovely, and it has been used quite a few times already since it was merged.

## Questions & Answers

**Q: Does this only work for running services or does it also work with non-running ones to, for example, debug why `MainPID` isn't starting as expected?**

A: This verb only works for running services. A follow-up verb will be added for non-running services.

**Q: Will the shell go away together with my service if it crash loops?**

A: This is expected behavior—the shell session exists within the running service's `namespace`.

## Credits

What's best about all this is that this new addition has been contributed by [@zihco](https://mastodon.social/@zihco) as part of the Outreachy program!

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114823531154384369) (2025-07-09)
