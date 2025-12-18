---
layout: post
title: "PID file descriptor `pidfd` identifiers"
date: 2025-08-20
---

Here's the 42nd post highlighting key new features of the upcoming v258 release of systemd.

Part of the protocol spoken between service processes and the service manager (if it is systemd, that is) are a number of environment variables. Specifically, `$MAINPID` and `$MANAGERPID` are two variables that have been part of the protocol for a long time: they contain the PID numbers of the main service process and of the service manager itself.

The former is useful in auxiliary processes associated with a service (for example `ExecStartPost=` or `ExecStop=`) for interacting with the main process of the service, for example to send a UNIX signal to it. The latter may be useful for service code to auto-detect if it is invoked by a service manager (in which case `getppid()` must match `$MANAGERPID`) or from a shell.

But we live in 2025, and POSIX PIDs are quite broken: they are recycled too frequently to be useful as stable identifiers. This recycling of processes creates a number of security and robustness issues. (These issues are not just theoretic; the PID space is so small that PID recycling is trivially easy to trigger and even happens by accident quite often).

New Linux kernels provide a way out: there are now `pidfds`, i.e. file descriptors that reference a specific process. This provides a stable handle to processes, even beyond their lifetime, with inode numbers that are 64-bit integers never recycled during a boot cycle. (Well, that's the theory – on 32-bit architectures, the inode numbers are only 32-bit, so the 64-bit `pidfd` IDs are made available via `name_to_handle_at()` rather than inode number.)

We have been moving systemd to use `pidfds` and their inode numbers at more and more places, in particular in the internal codebase.

But interfaces such as `$MAINPID`/`$MANAGERPID` of course are *external* interfaces, and expose numeric PIDs, hence we really should improve them too and remove the recycling attacks for them too.

And that's precisely what v258 does: there are now two new environment variables: `$MAINPIDFDID` and `$MANAGERPIDFDID`, which expose the inode IDs of the `pidfds` of the main process of the service or of the service manager process.

In combination with the old environment variables, this gives programs a safe, race-free way to operate with the main process and the service manager process: acquire a `pidfd` from a PID via `pidfd_open()`, then verify that its inode number matches the new environment variables. Done.

Note that there are various...

...other places where systemd currently only exposes a classic PID. In future versions, we should fill all those gaps and also expose the `pidfd` inode IDs too at each place.

And I am sorry that there's now an "id for an id" (i.e. the inode *ID* for a `pidfd` of a process *ID*). But it's Linux, and thus somewhat organically grown, and choices of the past (i.e. 32-bit `pid_t`, 32-bit `ino_t`) bind us to this day in messy ways…

---

## Q&A

> **@brauner** You are of course right.

> **@aheadofthekrauts** Nope, that's still missing.

> **@YaLTeR** You can create scope units by `pidfd` already. `systemd-run` uses that by default

> **@swick** For potentially remotable stuff we prefer passing boot ID + PID + `pidfd` inode ID.
>
> Newest `pidfd` makes exit status retrievable after process dies, via the `pidfd`; hence, if that's relevant, passing the file descriptor directly is preferable.
>
> We typically want most of our APIs remotable. Hence, at this point I'd always prefer boot ID + PID + `pidfd` inode ID if there's no reason to pass a `pidfd`.

---

[Original thread](https://mastodon.social/@pid_eins/115061399584325638) (2025-08-20)
