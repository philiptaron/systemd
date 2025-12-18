---
layout: post
title: "run0 --empower"
date: 2025-11-21
---

RE: https://mastodon.social/@daandemeyer/115565105032166177

4️⃣ Here's the 4th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

For this one I am simply going to top-post [@daandemeyer](https://mastodon.social/@daandemeyer)'s story about run0's new --empower switch, which gives your process capability + polkit privileges, without changing your user ID. Very powerful stuff.

---

> **[@pemensik](https://fosstodon.org/@pemensik)** It seems potentially dangerous. Does it share configuration with sudo somehow? What users are allowed to use this in default configuration?

This leaves auth to pk, unifying auth at one place hence: pk. Regular users by default get to use it only after the usual pk auth query.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115586469819973533) (2025-11-21)
