---
layout: post
title: "Unprivileged containers with userns"
date: 2025-05-26
---

One key Linux technology container runtimes rely on are user namespaces ("userns").
These essentially virtualize the `UID`/`GID` range so that each container can have their own set of `UID`s/`GID`s, that map to individual, distinct subsets of the host's `UID`s/`GID`s.
Given that `UID`s/`GID`s are the most fundamental of UNIX's security credentials, userns are pretty essential to security of containers.

## The Problem with `subuid`s/`subgid`s

Implementing userns is somewhat painful: a lot of restrictions apply, but from my PoV the messiest part is allocating `UID`/`GID` ranges on the host that can be used for each container, in particular when you intend to make use of userns entirely unprivileged: how do you take control of a `UID` range if you yourself run under an unprivileged `UID` range, and `UID`s are the fundamental form of security isolation on Linux?

The most widely deployed container engines use a concept called `subuid`s/`subgid`s for that.

And frankly, I detest the concept oh so very much.
First of all they are a relatively static concept, i.e. assign "subordinate" `UID`/`GID` ranges persistently to specific users, i.e. they "stick" forever to the user.
And not only that, but container trees need to recursively `chown()` to them, which makes them also "stick" to the container trees.
Moreover, they only work for unprivileged container managers because they are implemented via a `setuid` binary.

I think the concept of `setuid` binaries is a terrible concept, and a major weakness of the Linux security model.
In the systemd tree for example we'd never accept a `suid` binary to be added, because we see the concept as effectively a built-in security flaw.

Anyway, tldr: I dislike `subuid`s/`subgid`s very much.

## The New Solution in v257 and v258

With systemd v257 we already added concepts to that container managers can avoid `subuid`s/`subgid`s and still get the benefits of userns:

First of all, there's an IPC API in v257 to get a dynamic, transient `UID`/`GID` range for a userns.
A container runtime can acquire this, and make processes run under these ranges.

Secondly, there's an IPC API in v257 to mount disk images (i.e. file systems stored in regular files) with their `UID`/`GID` range mapped to such a dynamic `UID`/`GID` range acquired before.

A container runtime thus can first acquire a `UID`/`GID` range via the first API, and then mount a disk image to match that range, and then run the container from this combination.

That's already quite powerful, and I use that all the time for running truly unprivileged containers from disk images.

As it turns out though running containers of disk images (as opposed to running them from directory trees that are already mounted) is not the most common thing.
With v258 we are doing something about it: we set aside one fixed range of 64K host `UID`s/`GID`s that can now be used for container trees placed in regular directories.

## The Foreign UID Range

A new IPC API is now available to work with that: you pass in an `fd` to the directory, and an `fd` to a userns, and it returns you a mount `fd` of the dir, matching the userns.

And the twist of it: this is accessible to unprivileged clients: access will be granted without any further authentication as long as the dir's parent dir is owned by the client's own `UID`.

Or in other words: this allows container runtimes to place unpacked container trees in a user's `$HOME`.

They just need to make sure these trees are owned by that new fixed `UID` range (which we dubbed the "foreign" `UID` range).
After that, the container runtime can dynamically acquire a runtime `UID` range, then ask the new IPC API to get a mount of the container tree mapped to the runtime `UID` range, and voilá: fully unprivileged containers.
Without any "sticky" `UID` assignments to users or to inodes on disk.
And without any `suid` binary mess.

Oh, and there's a new `systemd-dissect --shift foreign` tool that allows you to fix up existing container trees, so that they are re-`chown()`-ed to the foreign `UID` range.
(This requires privs of course).

## Security Considerations

The disk images must come with Verity info and a signature for the verity data, which matches a key either known to the kernel or listed in `/etc/verity.d/`.

Or in other words: the disk images *files* are under full control of the user, but they are validated as they are mounted, and the *contents* of those files must be authenticated by some key known to the system.

---

> **[@valpackett](https://social.treehouse.systems/@valpackett):** the "map to host range" aspect has always been one of the most baffling linux decisions to me. why did they not just introduce a namespace ID as a second key so that (nsid, uid) pairs would become user accounts' actual identifiers, the way freebsd does it?

Yeah, I think so too, they should have just extended the `UID` range to 64bit or so (or maybe even 128bit, so you can just consider them uuids, like on other OSes).
But I guess they didn't want to touch existing file systems in this regard, as they generally just store 32bit `uid`s/`gid`s, not more...

> **[@TheStroyer](https://mastodon.social/@TheStroyer):** Would this system also work for mounting regular directories inside unprivileged containers? I'm always annoyed that the user that created a podman container cannot directly access the contents of a volume mounted in the container

The IPC allows two things to unprivileged clients: you pass in a dir owned by the foreign `UID` range whose parent dir is owned by the client `UID`.
This is what my post here mostly talks about.
In this case the 64K `UID`s/`GID`s of the foreign `UID` range are mapped wholesale to the 64K `UID`s/`GID`s of the provided userns.

But it also accepts a dir owned directly by the client `UID`, in which case a mapping with a single `UID` is created: from the client's `UID` to root of the container.

The latter should be what you are looking for, as I understand it.

---

## References

[systemd-machined]: https://www.freedesktop.org/software/systemd/man/258/systemd-machined.html
[systemd-nspawn]: https://www.freedesktop.org/software/systemd/man/258/systemd-nspawn.html
[systemd-dissect]: https://www.freedesktop.org/software/systemd/man/258/systemd-dissect.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114573005995694680) (2025-05-26)
