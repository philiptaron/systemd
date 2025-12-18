---
layout: post
title: "systemd 258 Feature Highlight #42"
date: 2025-08-20
source: https://mastodon.social/@pid_eins/115061399584325638
author: Lennart Poettering
---

4️⃣2️⃣ Here's the 42nd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Part of the protocol spoken between service processes and the service manager (if it is systemd, that is) are a number of environment variables. Specifically, $MAINPID and $MANAGERPID are two variables that have been part of the protocol for a long time: they contain the PID numbers of the main service process and of the service manager itself.

## Thread Continuation

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115061421956176834))

…of processes, which creates a number of security and robustness issues. (These issues are not just theoretic, the PID space is so small that PID recycling is trivially easy to trigger and even happens by accident quite often). 

New Linux kernels provide a way out: there are now "pidfds", i.e. fds that reference a specific processes. Which is a stable handle to processes, even beyond their lifetime. And their inode numbers are 64bit integers that are never recycled during…

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115061429170818521))

…a boot cycle. (well, that's the theory – as on 32bit archs the inode numbers are 32bit only the 64bit pidfd ids are made available via name_to_handle_at() rather than inode nr).

We have been moving systemd to use pidfds and their inode nrs at more and more places, in particular in the internal codebase.

But interfaces such as $MAINPID/$MANAGERPID of course are *external* interfaces, and expose numeric PIDs, hence we really should improve them too and remove the recycling attacks for them too.

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115061436678458709))

And that's precisely what v258 does: there are now two new env vars: $MAINPIDFDID + $MANAGERPIDFDID, which expose the inode ids of the pidfds of the main process of the service or of the service manager process.

In combination with the old env vars this gives programs a safe, race-free way to operate with the main process and the service manager process: acquire a pidfd from a PID via pidfd_open(), then verify that its inode number matches the new env vars. Done.

Note that there are various…

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115061440770496901))

…other places where systemd currently only exposes a classic PID. In future versions we should fill all those gaps and also expose the pidfd inode ids too at each place.

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115061471833095998))

And I am sorry that there's now an "id for an id" (i.e. the inode *id* for a pidfd of a process *id*). But it's Linux, and thus somewhat organically grown, and choices of the past (i.e. 32bit pid_t, 32bit ino_t) bind us to this day in messy ways…

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115061718060312129))

[@brauner](https://mastodon.social/@brauner) you are of course right.

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115062204323038702))

[@swick](https://hachyderm.io/@swick) for potentially remotable stuff we prefer passing boot id + pid + pidfd inode id.

newest pidfd make exit status retriavable after process died, via the pidfd, hence if that's relevant, passing the fd as fd is preferable.

we typically want most of our apis remotable, hence at this point i'd alwas prefer boot id+pid+pidfd inode id, if there's no reason to pass a pidfd.

*2025-08-20* ([source](https://mastodon.social/@pid_eins/115062208568575085))

[@YaLTeR](https://mastodon.online/@YaLTeR) you can create scope units by pidfd already. systemd-run uses that by default

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065462223348707))

[@aheadofthekrauts](https://social.tchncs.de/@aheadofthekrauts) nope, that's still missing.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115061412102530109):** The former is useful in auxiliary processes associated with a service (for example ExecStartPost=, ExecStop= or so) for interacting with the main process of the service, for example to send a UNIX signal to it. The latter may be useful for service code to auto-detect if it is invoked by a service manager (in which case getppid() must match $MANAGERPID) or from a shell.

But we live in 2025, and POSIX PIDs are quite broken: they are recycled too frequently to be useful as stable identifiers…

…of processes, which creates a number of security and robustness issues. (These issues are not just theoretic, the PID space is so small that PID recycling is trivially easy to trigger and even happens by accident quite often). 

New Linux kernels provide a way out: there are now "pidfds", i.e. fds that reference a specific processes. Which is a stable handle to processes, even beyond their lifetime. And their inode numbers are 64bit integers that are never recycled during…

## Sources

- [Original post](https://mastodon.social/@pid_eins/115061399584325638)
- [Thread continuation](https://mastodon.social/@pid_eins/115061421956176834)
- [Thread continuation](https://mastodon.social/@pid_eins/115061429170818521)
- [Thread continuation](https://mastodon.social/@pid_eins/115061436678458709)
- [Thread continuation](https://mastodon.social/@pid_eins/115061440770496901)
- [Thread continuation](https://mastodon.social/@pid_eins/115061471833095998)
- [Thread continuation](https://mastodon.social/@pid_eins/115061718060312129)
- [Thread continuation](https://mastodon.social/@pid_eins/115062204323038702)
- [Thread continuation](https://mastodon.social/@pid_eins/115062208568575085)
- [Thread continuation](https://mastodon.social/@pid_eins/115065462223348707)
