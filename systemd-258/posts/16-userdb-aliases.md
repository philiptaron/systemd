---
layout: post
title: "userdb aliases"
date: 2025-06-13
---

Since a while systemd has included the "userdb" subsystem, that extends the classic ~1983 "struct passwd" (as returned by `getpwnam()`) in a powerful, modernized way. While userdb's user records are a true superset of POSIX's/Linux's struct passwd, they retain the basic concepts: one can query a record by its UID or by its username, and gets a record back.

## Understanding User Records

The way the records are usually understood in UNIX is that the username ↔ record ↔ UID relationships are bijective, i.e. there's exactly one user name for a record, and one UID for it and vice versa, but afaics this is never clarified as part of POSIX.

Because of the lax definitions various subsystems that provide user records have departed from the bijective property, and defined records that can be found not just under a single name, but by many.

What's worse people also sometimes reuse UIDs among multiple user records.

Doing any of this is always a mess, since the lookup key doesn't actually necessarily appear in the record anymore, and forth and back translations are not symmetric anymore. Suffice to say, setups like that will run into problems, sooner rather than later, since applications and deployments typically are not ready for this.

## Introducing Aliases

In v258 the userdb subsystem is extended to relax rules a bit on this, but in a safer way than this was done with struct passwd. Specifically, there's now an "aliases" field in the userdb user record, that can list additional names a user record shall be discoverable under. When a user name is searched, the lookup will now match both the primary name of the user record, and alternatively any of its alias names.

## Use Case

Usecase: my user "lennart" now has an alias "l", so that I save 6 keypresses per login! Yay!

Why is this different from the hacky way people did this previously? Primarily: the alias names are *part* of the user record, and it's always clear which one is the primary name and which ones the aliases.

With this forth/back translations *are* reversible: if you lookup a user record by an alias name, then lookup the user record by its UID, it *will* list the alias name.

---

> **What kind of races are you referring to?**
>
> The lookups are always done in parallel to all backends, and the first one replying wins, under the assumptions that user name/UID conflicts have been dealt with already before lookup time, i.e. at definition time.

> **On conflict resolution:**
>
> userdb *expressely* makes no attempt to resolve conflicts. That can only fail and hide problems. If there are conflicts then they need to be dealt with *before* making the records available, not after.
>
> Hence, it's not userdb's job to fix the security mess that conflicts are, it's the job of whatever owns the record to clean this up.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114674923588128559) (2025-06-13)
