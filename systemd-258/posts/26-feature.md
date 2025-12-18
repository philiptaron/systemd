---
layout: post
title: "systemd 258 Feature Highlight #26"
date: 2025-07-02
source: https://mastodon.social/@pid_eins/114782700539340326
author: Lennart Poettering
---

2️⃣6️⃣ Here's the 26th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

If you ever put together a systemd service, you must be aware of the ExecStart= setting, which declares the command line to actually invoke for the service. It's probably *the* most important setting of all.

ExecStart= has various features these days. Besides specifier expansion and a limited form of environment variable expansion, ...

## Thread Continuation

*2025-07-02* ([source](https://mastodon.social/@pid_eins/114782764395358256))

… configured in User= of the same service). Or in other words: we invoke the shell and pass the specified command via the "-c" parameter to it.

What's this good for? Of course, you could use this for embedding shell scripts into the sevice file, but I am not sure that would be too wise (since which shell is used is configured in the user record, not in the service, i.e. you might end up writing a zsh script that will be interpreted by bash or similar).

*2025-07-02* ([source](https://mastodon.social/@pid_eins/114782769992669848))

Our primary usecase for this is different hence: it's to make sure our sudo replacement run0 is nicer to use: typically people expect that interactive run0 switches to the target account's configured shell (instead of /bin/sh), and that's what this new flag allows us to do.

*2025-07-02* ([source](https://mastodon.social/@pid_eins/114782776142504075))

[@agowa338](https://chaos.social/@agowa338) sure, but not sure if you actually want to do that, see my comments about that.

*2025-07-02* ([source](https://mastodon.social/@pid_eins/114782851012012843))

[@agowa338](https://chaos.social/@agowa338) you can use the ":" modifier to disable env var expansion. very useful for manual "sh -c" lines. (you cannot disable specifier expansion though)

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114782747414194506):** …there are a couple of flags you can specify to alter how the command line is executed. These are denoted via special characters, such as "@", "-", ":", "+", "!" as first character of the setting's values. (Yes, this is a bit cryptic, we have to admit that).

With v258 we added one more such flag: "|" (i.e. the pipe symbol). If used, then instead of executing the specified command directly, it's invoked though the shell configured in the user database for the target user (i.e. the user…

… configured in User= of the same service). Or in other words: we invoke the shell and pass the specified command via the "-c" parameter to it.

What's this good for? Of course, you could use this for embedding shell scripts into the sevice file, but I am not sure that would be too wise (since which shell is used is configured in the user record, not in the service, i.e. you might end up writing a zsh script that will be interpreted by bash or similar).

## Sources

- [Original post](https://mastodon.social/@pid_eins/114782700539340326)
- [Thread continuation](https://mastodon.social/@pid_eins/114782764395358256)
- [Thread continuation](https://mastodon.social/@pid_eins/114782769992669848)
- [Thread continuation](https://mastodon.social/@pid_eins/114782776142504075)
- [Thread continuation](https://mastodon.social/@pid_eins/114782851012012843)
