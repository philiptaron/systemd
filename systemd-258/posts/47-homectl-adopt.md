---
layout: post
title: "`homectl adopt` and `homectl register`"
date: 2025-08-27
---

Here's the 47th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258) [#systemd](https://mastodon.social/tags/systemd)

In episode 38 of this series we talked about `homectl`'s new commands to manage signing keys for user accounts.

There are two other new commands `homectl` gained in v258.

First of all there's `homectl adopt`. You just pass a path to an existing `*.home` LUKS disk image, or a `*.homedir` home directory, and it will make it available locally for login (assuming it carries the right signatures accepted by the local system). The same could already be achieved by simply linking the `.home`/`.homedir` path into `/home/`, which also causes `systemd-homed` to pick it up, but `homectl adopt` works without that, the actual home directory remains wherever it is, and `/home/` is not modified.

The other is `homectl register`. It executes a similar operation, but instead of providing a `.home`/`.homedir` path you pass a path to the JSON data of a user record, and it will make it available for local login (again, assuming the record is signed properly).

The two commands complement each other: one takes the home directory itself, the other `JSON` record instead, both add an entry to the list of users accessible locally.

Both commands are different from `homectl create` btw, because they do not create any home directory (or user record) anew, they just take what's already there and add it to the local system.

---

## Use Cases

The `adopt` command is useful when migrating a home directory from one laptop to a new one.

The `register` command is useful when doing something like `SMB` sharing of a home directory, as described in episode 38. For example: `homectl inspect -E <user> | ssh <otherhost> homectl register` is a powerful command for propagating a user account from one host to another.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115099443130286999) (2025-08-27)
