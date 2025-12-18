---
layout: post
title: "PID file descriptor identifiers"
date: 2025-08-20
---

Here's the 42nd post highlighting key new features of the upcoming v258 release of systemd.

Part of the protocol spoken between service processes and the service manager (if it is systemd, that is) are a number of environment variables. Specifically, `$MAINPID` and `$MANAGERPID` are two variables that have been part of the protocol for a long time: they contain the PID numbers of the main service process and of the service manager itself.

The former is useful in auxiliary processes associated with a service (for example `ExecStartPost=`, `ExecStop=` or so) for interacting with the main process of the service, for example to send a UNIX signal to it. The latter may be useful for service code to auto-detect if it is invoked by a service manager (in which case `getppid()` must match `$MANAGERPID`) or from a shell.

But we live in 2025, and POSIX PIDs are quite broken: they are recycled too frequently to be useful as stable identifiers.

...of processes, which creates a number of security and robustness issues. (These issues are not just theoretic, the PID space is so small that PID recycling is trivially easy to trigger and even happens by accident quite often).

New Linux kernels provide a way out: there are now "pidfds", i.e. fds that reference a specific processes. Which is a stable handle to processes, even beyond their lifetime. And their inode numbers are 64bit integers that are never recycled during...

...a boot cycle. (well, that's the theory – as on 32bit archs the inode numbers are 32bit only the 64bit pidfd ids are made available via `name_to_handle_at()` rather than inode nr).

We have been moving systemd to use pidfds and their inode nrs at more and more places, in particular in the internal codebase.

But interfaces such as `$MAINPID`/`$MANAGERPID` of course are *external* interfaces, and expose numeric PIDs, hence we really should improve them too and remove the recycling attacks for them too.

And that's precisely what v258 does: there are now two new env vars: `$MAINPIDFDID` + `$MANAGERPIDFDID`, which expose the inode ids of the pidfds of the main process of the service or of the service manager process.

In combination with the old env vars this gives programs a safe, race-free way to operate with the main process and the service manager process: acquire a pidfd from a PID via `pidfd_open()`, then verify that its inode number matches the new env vars. Done.

Note that there are various...

...other places where systemd currently only exposes a classic PID. In future versions we should fill all those gaps and also expose the pidfd inode ids too at each place.

And I am sorry that there's now an "id for an id" (i.e. the inode *id* for a pidfd of a process *id*). But it's Linux, and thus somewhat organically grown, and choices of the past (i.e. 32bit `pid_t`, 32bit `ino_t`) bind us to this day in messy ways…

---

## Q&A

> **@brauner** you are of course right.

> **@aheadofthekrauts** nope, that's still missing.

> **@YaLTeR** you can create scope units by pidfd already. systemd-run uses that by default

> **@swick** for potentially remotable stuff we prefer passing boot id + pid + pidfd inode id.
>
> newest pidfd make exit status retrievable after process died, via the pidfd, hence if that's relevant, passing the fd as fd is preferable.
>
> we typically want most of our apis remotable, hence at this point i'd always prefer boot id+pid+pidfd inode id, if there's no reason to pass a pidfd.

---

[Original thread](https://mastodon.social/@pid_eins/115061399584325638) (2025-08-20)
