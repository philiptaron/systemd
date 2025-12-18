---
layout: post
title: "systemd 258 Feature Highlight #34"
date: 2025-08-07
source: https://mastodon.social/@pid_eins/114986213475696548
author: Lennart Poettering
---

3️⃣4️⃣ Here's the 34th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

When deploying "golden" images (i.e. carefully prepared unified images that are be booted on many systems, where they acquire an identity of their own, as well as their own state on first boot), depending on context it makes sense to interactively ask the user for certain basic system settings, such as UI language, hostname, and similar.

## Thread Continuation

*2025-08-07* ([source](https://mastodon.social/@pid_eins/114986233162190451))

…locale settings, keyboard mappings, timezone, root shell choice it now will auto-complete your choices by hitting TAB, and show you a list of suitable options on TAB TAB, in a similar style to how this is done on interactive shells.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114986222571976849):** For a longer time systemd shipped "systemd-firstboot" as a basic terminal based implementation to provide the interactive UI for this. It may be used in place of something more fancy and graphical in environments where that'd be overkill.

The tool gained some functionality over time, but it always remained very simplistic in its interface. With v258 we make it a bit more comfortable to use: there's now tab completion available in the various prompts it provides. i.e. when you are asked for…

…locale settings, keyboard mappings, timezone, root shell choice it now will auto-complete your choices by hitting TAB, and show you a list of suitable options on TAB TAB, in a similar style to how this is done on interactive shells.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114986213475696548)
- [Thread continuation](https://mastodon.social/@pid_eins/114986233162190451)
