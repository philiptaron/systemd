---
layout: post
title: "userdb drop-in directories"
date: 2025-06-23
---

Here's the 21st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Earlier in this series I already wrote about `userdb`, systemd's user database logic, that extends the classic UNIX `struct passwd`-based user database in a flexible and powerful way, based on extensible JSON user records.

Besides implementing a Varlink-based IPC API there's also a second way to make user records available: there's a bunch of drop-in directories: `/etc/userdb/`, `/run/userdb/`, `/usr/lib/userdb/` where you can drop in records as regular JSON files, and they will be made available in NSS and userdb like any other.

This sounds easy, and indeed *is* quite easy, but it's not *as* easy as it might look at the surface. That's because user records are typically understood to have a `public` and a `sensitive` part. The former contains data that everyone with access to the system shall be able to see, the latter contains data that only the user themselves (or the admin) shall be able to see (password hashes, etc.). On classic Linux this distinction is reflected in the separation of `/etc/passwd` and `/etc/shadow`.

Moreover, there are *two* primary keys for looking up user records: the user name and the numeric UID.

Because of that using that drop-in directory means not installing a single file there for each user record, but actually two (the public part in a `<username>.user` file, the sensitive part in a `<username>.user-privileged` file) plus two symlinks (one that points from `<uid>.user` to `<username>.user`, and one similar for the privileged file).

On top of that, userdb normalizes the handling of user/group memberships: instead of strictly storing the memberships in user records, or in group records (the latter is what UNIX does), userdb manages them separately, in case of the userdb drop-in files as a fifth type of file: `<username>:<groupname>.membership` files.

Long story short: for each user you want to register via userdb drop-in files you actually need to drop-in 4+n files where n is the number of groups the user shall be in.

Conceptually still quite easy to grok I would say, but of course, not completely trivial anymore.

One usecase for dropping in JSON user record files like this involves invoking VMs or containers which shall be able to access a user home directory mounted in from the host, through a propagated user record.

With v258 we added a concept to make this easier to do. There's now a new mini-service that runs at boot: `systemd-userdb-load-credentials.service`. It only runs if a `userdb.user.*` (or `userdb.group.*`) system credential has been passed in. Such a credential may contain a user record in JSON format. The little service will take it, split the sensitive part from the public part, then write drop-in files for each into `/run/userdb/`, then create the two symlinks, and create the `.membership` files.

Net result: you can pass a simple JSON object for each user you want to be made available in a container/VM via a credential, and it will just be there once the system pops up. And don't forget: both `systemd-vmspawn` and `systemd-nspawn` provide you with a very easy `--load-credential=` switch to pass in such a system credential.

One thing though: the tool does *not* allocate a UID for such user records, it expects one to be already assigned. And before you ask, it has already been requested to change that, and support UID allocation too. This would then allow you to just pass `--set-credential=userdb.user.foo:'{"userName":"foo"}'` to nspawn/vmspawn to get a user by that name auto-registered. We have such allocation code in place already (that's what `sysusers.d/` is about after all), but it's not hooked up to this new mini service yet. (If this interests you, happy to review a PR...)

---

> **[CounterPillow](https://fosstodon.org/@CounterPillow)** hu? we do not use utf16? we use utf8.

Indeed, we use UTF-8.

> **[@tfheen](https://fosstodon.org/@tfheen)** what does "sharing root accounts" mean?

(No response provided)

> **[@tfheen](https://fosstodon.org/@tfheen)** frankly, such a setup is icky and likely to break at numerous places already (because user lookups cannot be roundtripped anymore, i.e. username→uid→username translations will report conflicting info). I am not convinced it's really worth supporting that properly.

(This was a response to a previous question about sharing root accounts)

---

[userdb]: https://www.freedesktop.org/software/systemd/man/258/userdb.html
[systemd-userdb-load-credentials.service]: https://www.freedesktop.org/software/systemd/man/258/systemd-userdb-load-credentials.service.html
[systemd-vmspawn]: https://www.freedesktop.org/software/systemd/man/258/systemd-vmspawn.html
[systemd-nspawn]: https://www.freedesktop.org/software/systemd/man/258/systemd-nspawn.html
[sysusers.d]: https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114731475255410988) (2025-06-23)
