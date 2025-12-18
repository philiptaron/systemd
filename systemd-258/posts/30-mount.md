---
layout: post
title: "systemd 258 Feature Highlight #30"
date: 2025-07-09
source: https://mastodon.social/@pid_eins/114823531154384369
author: Lennart Poettering
---

3️⃣0️⃣ Here's the 30th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

systemd's service sandboxing logic builds heavily on Linux mount namespacing, as well as other types of process namespacing. It primarily uses to this to take away access to certain subhierarchies (i.e. marking them read-only, unmounting them or overmounting them with something else), but it also allows to rearrange things (i.e. bind mount one dir onto another, obstructing access to it).

## Thread Continuation

*2025-07-09* ([source](https://mastodon.social/@pid_eins/114823567586140575))

In a way this is somewhat equivalent to `nsenter -a -p $(systemctl show -P MainPID $UNIT)`, but this new tool is a bit more careful as well as nicely integrated in our tool set. It's lovely, and I have been using this myself quite a few times already since we merged it a few days ago.

What's best about all this is that this new addition has been contributed by [@zihco](https://mastodon.social/@zihco) as part of of the Outreachy program!

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114823542015115353):** This is all very efficient to secure services, but it's also a bit opaque: since it's the daemon you sandbox, and your admin tools are outside of that sandbox it's sometimes hard to analyze how the daemon sees things.

No more. With v258 there's a new verb "unit-shell" in systemd-analyze. You specify a service name, and it opens you a shell inside that specified services' sandbox (which must be running for this). You can look around and check if everything is like you expected it to be.

In a way this is somewhat equivalent to `nsenter -a -p $(systemctl show -P MainPID $UNIT)`, but this new tool is a bit more careful as well as nicely integrated in our tool set. It's lovely, and I have been using this myself quite a few times already since we merged it a few days ago.

What's best about all this is that this new addition has been contributed by [@zihco](https://mastodon.social/@zihco) as part of of the Outreachy program!

## Sources

- [Original post](https://mastodon.social/@pid_eins/114823531154384369)
- [Thread continuation](https://mastodon.social/@pid_eins/114823567586140575)
