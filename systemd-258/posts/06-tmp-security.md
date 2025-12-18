---
layout: post
title: "/tmp/ security hardening"
date: 2025-05-31
---

The concept of `/tmp/` has been a constant source of local security vulnerabilities, mostly in form of a local DoS: `/tmp/` is a shared namespace and less than perfect programs create files under guessable names there, which evil programs can then use to DoS them.

This has been like this since time began and `/tmp/` was invented.

Getting rid of the whole concept is hard though, since `/tmp/` is not just used for temporary files, but also for communication, precisely because it *is* a shared namespace. Most famously X11 puts its sockets there, hence virtualizing `/tmp/` by means of mount namespacing is difficult. (And yes, the X11 question is kinda being solved these days, but there's a lot more like this unfortunately).

There are safe ways to use `/tmp/` though, in fact we have some docs ready explaining how: [Using /tmp/ and /var/tmp/ Safely](https://systemd.io/TEMPORARY_DIRECTORIES/).

Now, if you follow that, all is good, right?

No, you are still vulnerable to a DoS, independently of the guessable filenames issue: because `/tmp/` is generally backed by `tmpfs` and `tmpfs` had no quota concept an unprivileged user can just take as much space in `/tmp/` as it wants, so that no one else can create any inodes there anymore.

Or in other words: yes, you can do everything right in regards with `/tmp/`, but you are *still* vulnerable to a DoS then.

In v258 we are doing something about that. Very recent Linux kernels actually did get support for quota on `tmpfs`. Hence with v258 we'll now configure quota automatically at login time. By default every user gets a quota of 80% of the tmpfs size assigned. If your user provides a modern `userdb` JSON record, it can also configure anything else.

Or in other words: the DoS became much harder: to effectively take away all `/tmp/` space from other users you now need to possess control over at least two UIDs, one won't suffice (unless of course you are unlucky and somebody used `/tmp/` where they actually should have used `/var/tmp/` and put massive amounts of data there, already consuming >20% of space there).

Or in even other words: `/tmp/` is still a mess of a concept, but one facet of it is now a bit less messy.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114600936718520372) (2025-05-31)
