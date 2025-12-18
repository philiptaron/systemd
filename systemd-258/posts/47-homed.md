---
layout: post
title: "systemd 258 Feature Highlight #47"
date: 2025-08-27
source: https://mastodon.social/@pid_eins/115099443130286999
author: Lennart Poettering
---

4️⃣7️⃣ Here's the 47th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In episode 38 of this series we talked about homectl's new commands to manage signing keys for user accounts.

There are two other new commands homectl gained in v258.

First of all there's "homectl adopt". You just pass a path to an existing *.home LUKS disk image, or a *.homedir home directory, and it will make it available locally for login (assuming it carries the…

## Thread Continuation

*2025-08-27* ([source](https://mastodon.social/@pid_eins/115099463759830158))

…it available for local login (again, assuming the record is signed properly). 

The two commands complement each other: one take the home dir itself, the other json record instead, both add an entry to the list of users accessible locally.

Both commands are different from "homectl create" btw, because they do not create any home directory (or user record) anew, they just take what's already there and add it to the local system.

*2025-08-27* ([source](https://mastodon.social/@pid_eins/115099470358901463))

The "adopt" command is useful when migrating a home dir from one laptop to a new one.

The "register" command is useful when doing something like the SMB sharing of a home dir, as described in episode 38. i.e. "homectl inspect -E <user> | ssh <otherhost> homectl register" is a powerful command for propagating a user account from one host to another.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115099454219444163):** …right signatures accepted by the local system). The same could already be achieved by simply linking the .home/.homedir path into /home/, which also causes systemd-homed to pick it up, but "homectl adopt" works without that, the actual home dir remains wherever it is, and /home/ is not modified.

The other is "homectl register". It executes a similar operation, but instead of providing a .home/.homedir path you pass a path to the JSON data of a user record, and it will make…

…it available for local login (again, assuming the record is signed properly). 

The two commands complement each other: one take the home dir itself, the other json record instead, both add an entry to the list of users accessible locally.

Both commands are different from "homectl create" btw, because they do not create any home directory (or user record) anew, they just take what's already there and add it to the local system.

## Sources

- [Original post](https://mastodon.social/@pid_eins/115099443130286999)
- [Thread continuation](https://mastodon.social/@pid_eins/115099463759830158)
- [Thread continuation](https://mastodon.social/@pid_eins/115099470358901463)
