---
layout: post
title: "systemd 258 Feature Highlight #52"
date: 2025-09-10
source: https://mastodon.social/@pid_eins/115179113138417200
author: Lennart Poettering
---

5️⃣2️⃣ Here's the 52nd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

PrivateUsers= is one of the many sandboxing knobs in service unit files. It configures a minimal user namespace for the service code to run in. So far you could set it to "self", which would set up the user namespace mapping for the service to map the root user and the service's user to itself, and leave everything else unmapped.

## Thread Continuation

*2025-09-10* ([source](https://mastodon.social/@pid_eins/115179140857740263))

With v258 a third value has been added: "full". If used the user namespace's UID mapping would map all 2^32 UIDs to themselves.

You might wonder: what's the point of a user namespace if it has a full mapping of the host UID range without altering anything?  Here's the thing: user namespaces are not just about mappings, they also make various operations unnaccessible to processes contained in them, and they can "own" other namespace types.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115179127146633043):** Setting the knob to "self" hence would somewhat disconnect the service from the host user table: all inodes, processes, and other objects it sees will be owned by itself, by root or by the "nobody" user (which is where unmapped users are mapped to). 

In v257 the setting learnt a new value "identity". If used the first 64K users plus the service's own user (if outside the 64K range) would be mapped, nothing else. Or in other words,  the service would be limited to the 16bit UID range.

With v258 a third value has been added: "full". If used the user namespace's UID mapping would map all 2^32 UIDs to themselves.

You might wonder: what's the point of a user namespace if it has a full mapping of the host UID range without altering anything?  Here's the thing: user namespaces are not just about mappings, they also make various operations unnaccessible to processes contained in them, and they can "own" other namespace types.

## Sources

- [Original post](https://mastodon.social/@pid_eins/115179113138417200)
- [Thread continuation](https://mastodon.social/@pid_eins/115179140857740263)
