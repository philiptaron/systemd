---
layout: post
title: "systemd 258 Feature Highlight #16"
date: 2025-06-13
source: https://mastodon.social/@pid_eins/114674923588128559
author: Lennart Poettering
---

1️⃣6️⃣ Here's the 16th  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Since a while systemd has included the "userdb" subsystem, that extends the classic ~1983 "struct passwd" (as returned by getpwnam()) in a powerful, modernized way. While userdb's user records are a true superset of POSIX'/Linux' struct passwd, the retain the basic concepts: one can query a record by its UID or by its username, and gets a record back.

## Thread Continuation

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114674961878143749))

What'se worse people also sometimes reuse UIDs among multiple user records.

Doing any of this is always a mess, since the lookup key doesn't actually necessarily appear in the record anymore, and forth and back translations are not symmetric anymore. Suffice to say, setups like that will run into problems, sooner rather than later, since applications and deployments typically are not ready for this.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114674970992015469))

In v258 the userdb subsystem is extended to relax rules a bit on this, but in a safer way than this was done with struct passwd. Specifically, there's now an "aliases" field in the userdb user record, that can list additional names a user record shall be discoverable under. When a user name is searched, the lookup will now match both the primary name of the user record, and alternatively any of its alias names.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114674986512614072))

Usecase: my user "lennart" now has an alias "l", so that I save 6 keypresses per login! Yay!

Why is this different from the hacky way people did this previously? Primarily: the alias names are *part* of the user record, and it's always clear which one is the primary name and which ones the aliases.

With this forth/back translations *are* reversible: if you lookup a user record by an alias name, then lookup the user record by its UID, it *will* list the alias name.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114675124957044692))

[@firstyear](https://infosec.exchange/@firstyear) what kind of races are you referring to?

The lookups are always done in parallel to all backends, and the first one replying wins, under the assumptions that user name/UID conflicts have been dealt with already before lookup time, i.e. at definition time.

But not sure I grok what your question is about,

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114675526891348932))

[@firstyear](https://infosec.exchange/@firstyear) userdb *expressely* makes no attempt to resolve conflicts. That can only fail and hide problems. If there are conflicts then they need to be dealt with *before* making the records available, not after.

Hence, it's not userbd's job to fix the security mess that conflicts are, it's the job of whatever owns the record to clean this up.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114676029292635636))

[@firstyear](https://infosec.exchange/@firstyear) Sorry, but this is really to fix for the backends. userdb is really not the place.

If you have conflicting user names or UIDs, then yes, that's problematic. But I am strongly of the opinion that userdb would be the wrong place to deal with it: it's the backends which are responsible for this. If the deed is already done it's *never* going to be reliable to try to polish the burning pile of shit in userdb.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114676036751918737))

[@firstyear](https://infosec.exchange/@firstyear) if you have a setup where user names clash, then that#s your bug, and userdb is *waaaayy* too late in the chain to do anything about it. Fix your setup. It's *always* going to be a total mess if some tools think user record X is right and others think user record Y is right, and userdb is not going to possibly solve that.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114676042991239464))

[@firstyear](https://infosec.exchange/@firstyear) [@erincandescent](https://akko.erincandescent.net/users/erincandescent) sorry, i strongly disagree this is a problem to deal with in systemd. Please contact your ldap clients of choice about this: *they* must deal with such conflicts, and not let them leak onto the final systems.

Hence, please ask your ldap project of choice for its security contact and ping them, not systemd.

Sorry, but I am refusing to make this my problem.

*2025-06-13* ([source](https://mastodon.social/@pid_eins/114676142636318376))

[@erincandescent](https://akko.erincandescent.net/users/erincandescent) [@firstyear](https://infosec.exchange/@firstyear) on nss there's a strict order which is encoded in nsswitch.conf, and the first one wins. But it's a frickin mess, because it also supports "merging" group records, and then it just squashes the stack of modules.

I am very strongly of the opinion that merging records is broken, and that a conflict doesn't stop being a conflict just because you let one side win on the local system.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114674946522038928):** The way the records are usually understood in UNIX is that the username ↔ record ↔ UID relationships are bijective, i.e. there's exactly one user name for a record, and one UID for it and vice versa, but afaics this is never clarified as part of POSIX.

Because of the lax definitions various subsystems that provide user records have departed from the bijective property, and defined records that can be found not just under a single name, but by many.

What'se worse people also sometimes reuse UIDs among multiple user records.

Doing any of this is always a mess, since the lookup key doesn't actually necessarily appear in the record anymore, and forth and back translations are not symmetric anymore. Suffice to say, setups like that will run into problems, sooner rather than later, since applications and deployments typically are not ready for this.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114674923588128559)
- [Thread continuation](https://mastodon.social/@pid_eins/114674961878143749)
- [Thread continuation](https://mastodon.social/@pid_eins/114674970992015469)
- [Thread continuation](https://mastodon.social/@pid_eins/114674986512614072)
- [Thread continuation](https://mastodon.social/@pid_eins/114675124957044692)
- [Thread continuation](https://mastodon.social/@pid_eins/114675526891348932)
- [Thread continuation](https://mastodon.social/@pid_eins/114676029292635636)
- [Thread continuation](https://mastodon.social/@pid_eins/114676036751918737)
- [Thread continuation](https://mastodon.social/@pid_eins/114676042991239464)
- [Thread continuation](https://mastodon.social/@pid_eins/114676142636318376)
