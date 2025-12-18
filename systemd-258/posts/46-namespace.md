---
layout: post
title: "systemd 258 Feature Highlight #46"
date: 2025-08-26
source: https://mastodon.social/@pid_eins/115095836068972901
author: Lennart Poettering
---

4️⃣6️⃣ Here's the 46th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

The various ProtectXYZ= settings for service unit files allow locking services into sandboxes in a relatively fine grained fashion.

The ProtectHostname=yes option is one of these options: it locks the service into a "uts" namespace (which is a Linux kernel construct that disconnects the system hostname the service uses from the hostname the rest of the system sees).

## Thread Continuation

*2025-08-26* ([source](https://mastodon.social/@pid_eins/115095856700903284))

and this should not be misunderstood).

With v258 we are extending the setting in two ways: so far the option was a boolean. Now it takes a third value: "private". If set to that, the hostname is disconnected as before, but hostname changes are not prohibited for the service – however they won't propagate to the system as a whole.

And there's one more trick the setting now has up its sleeve: you may now suffix the setting with a colon, followed by a literal hostname specification, …

*2025-08-26* ([source](https://mastodon.social/@pid_eins/115095862705388869))

… which has the effect of not only disconnecting the hostname from the host (and possibly prohibiting an attempts to change it), but also initializing it to some string of choice.

Example: ProtectHostname=private:foobar

This will disconnect the hostname from the rest of the system, and set the hostname from the service's PoV to "foobar". The service may change the hostname via sethostname() during runtime, which will be in effect for that service, but nothing else on the system.

*2025-08-26* ([source](https://mastodon.social/@pid_eins/115096748445768789))

[@nogweii](https://aethernet.social/@nogweii) ProtectHostname=yes:foobar will do the job.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115095845556819920):** It also enforces some "seccomp" based restrictions on the system calls to change the hostname. Altogether it is a simple way to "freeze" the hostname for a specific service, and ensure it cannot alter it itself (it might still do so indirectly, if it has suitable access to an IPC service doing it for it, for example systemd-hostnamed, hence is only part of the puzzle to lock things down, it's not a one-stop solution blocking hostname changes altogether –

and this should not be misunderstood).

With v258 we are extending the setting in two ways: so far the option was a boolean. Now it takes a third value: "private". If set to that, the hostname is disconnected as before, but hostname changes are not prohibited for the service – however they won't propagate to the system as a whole.

And there's one more trick the setting now has up its sleeve: you may now suffix the setting with a colon, followed by a literal hostname specification, …

## Sources

- [Original post](https://mastodon.social/@pid_eins/115095836068972901)
- [Thread continuation](https://mastodon.social/@pid_eins/115095856700903284)
- [Thread continuation](https://mastodon.social/@pid_eins/115095862705388869)
- [Thread continuation](https://mastodon.social/@pid_eins/115096748445768789)
