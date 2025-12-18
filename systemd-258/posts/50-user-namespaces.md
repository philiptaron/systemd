---
layout: post
title: "User namespaces and cgroups"
date: 2025-09-02
---

50️⃣ Here's the 50th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258) [#systemd](https://mastodon.social/tags/systemd)

User namespaces are weird beasts: on one hand they are supposed to be something that you can acquire without privileges, but on the other hand if you want more than a single UID mapped into them, you need multiple UIDs, and that's a resource you cannot acquire without privs.

To deal with that multiple systems have been devised.

Traditionally there was the `subuid` concept, with the `newuidmap` tool that statically delegates a whole UID range to a user. What can I say, I seriously dislike the idea for a multitude of reasons (urks, suid! urks, persistent assignments! urks, writable `/etc/`! urks, need for propagation via ldap! urks urks urks...). To improve things systemd gained `systemd-nsresourced`, which hands out mappings *transiently* only.

Regardless which mechanism you pick, it does create a weird situation: conceptually unpriv user objects (processes, files, cgroups, ...) are owned by UIDs that are under user control, but without this UID-UID ownership being directly known to the kernel. IOW: the only way to interact with those objects without privs is for the user to go through namespacing similar to how they were originally created. If user code tries to interact with them without going through userns, these objects will appear...

...as foreign UID owned.

(Well, handling of processes is slightly less complex than files/cgroups here, since during their runtime they retain attachment to the userns they where created with, and that userns remains owned by the user's UID, which gives it magic powers. But files and cgroups don't work that way: file system objects "at rest" retain no binding to the userns, and thus no such magic powers from the original user's UID remains)

For systemd this all creates various challenges. One specifically is what this episode is about: there's a per-user service manager for each user, and it manages cgroups. When invoking a userns based container, it makes sense to delegate a cgroup to it, so that the container has all it needs to boot a full blown systemd inside. Delegation means assigning ownership of the cgroup to the UID range used for the userns. But this then means that the per-user service manager...

...will lack the privs to clean up the cgroup delegated to the container, since after all it just runs under the user's UID, but it has no knowledge of the userns or its mappings created by the container manager.

And this is a problem for robustness: it means that the container executor has to carefully clean up after itself, and never leave cgroups around, because unlike almost all other resources, the service manager managing that container executor is unable to clean up after it.

I ran into this problem quite frequently while hacking on nspawn and other userns related code: when my unpriv code died due to some bug I ended up with cgroups in the user's cgroup hierarchy that the per-user service manager couldn't clean up anymore, thus creating something of a DoS scenario.

With systemd v258 this changes a bit. The per-system service manager gained an IPC call that the per-user service manager can call, requesting it to clean up such cgroups for it. The per-system service...

...manager runs privileged after all, and thus can do this.

Of course, the per-system service manager carefully validates the caller's credentials, and verifies that it delegated the cgroup to the caller in the first place. If that checks out, it will remove any subgroup requested, regardless by which UID it owns.

All of this is mostly transparent to services btw: if your code delegates a cgroup to other UIDs, and your service dies it will now be cleaned up no matter what.

That said, the D-Bus method call `RemoveSubgroupFromUnit()` that is behind this is actually available to clients too, which even allows just removing parts of a delegated subtree, instead of the whole thing.

Moreover, there's a related call `KillUnitSubgroup()` will allows killing processes in a delegated cgroup subtree, too, for similar reasons and usecases.

---

## Q&A

> **[@niklauzg](https://indieweb.social/@niklauzg)** Very glad for these changes! May you further describe how the subUIDs are transiently allocated? How could that be enabled/disabled by a system admin and how would it be visible and managed using systemd. For example, I'd imagined this might be a nested and instanced "sub-user@.service", is that off-base?

I need to think about this more before replying.

> **[@cas](https://social.treehouse.systems/@cas)** This is so awesome! i will definitely be adding support for using nsresourced in pmbootstrap when available to avoid all these shenanigans (will need to keep the other stuff around including the ability to set up `/etc/subXid` for those Alpine users heh)

Great to hear!

> **[@alwayscurious](https://infosec.exchange/@alwayscurious)** Would it make sense for the kernel to gain a knowledge of this for files, cgroups, and other things? Something like Windows's DACLs? *gulp*

No response yet from Lennart.

---

[systemd-resolved]: https://www.freedesktop.org/software/systemd/man/258/systemd-resolved.html
[systemd-machined]: https://www.freedesktop.org/software/systemd/man/258/systemd-machined.html
[systemd-networkd]: https://www.freedesktop.org/software/systemd/man/258/systemd-networkd.html
[systemd-nsresourced]: https://www.freedesktop.org/software/systemd/man/258/systemd-nsresourced.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115132962518662116) (2025-09-02)
