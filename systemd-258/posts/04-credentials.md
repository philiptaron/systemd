---
layout: post
title: "systemd 258 Feature Highlight #4"
date: 2025-05-26
source: https://mastodon.social/@pid_eins/114573005995694680
author: Lennart Poettering
---

4️⃣ Here's the 4th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

One key Linux technology container runtimes rely on are user namespaces ("userns"). These essentially virtualize the UID/GID range so that each container can have their own set of UIDs/GIDs, that map to individual, distinct subsets of the host's UIDs/GIDs. Given that UIDs/GIDs are the most fundamental of UNIX's security credentials, userns are a pretty essential to security of containers.

## Thread Continuation

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573029973004044))

And frankly, I detest the concept oh so very much. First of all they are a relatively static concept, i.e. assign "subordinate" UID/GID ranges persistently to specific users, i.e. they "stick" forever to the user. And not only that, but container trees need to recursively chown()ed to them, which makes them also "stick" to the container trees. Moreover, they only work for unprivileged container managers because they are implemented via a setuid binary.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573042603518246))

I think the concept of setuid binaries is a terrible concept, and a major weakness of the Linux security model. In the systemd tree for example we'd never accept a suid binary to be added, because we see the concept as effectively a built-in security flaw.

Anyway, tldr: I dislike subuids/subgids very much.

With systemd v257 we already added concepts to that container managers can avoid subuids/subgids and still get the benefits of userns:

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573051904511385))

First of all, there's an IPC API in v257 to get a dynamic, transient UID/GID range for a userns. A container runtime can acquire this, and make processes run under these ranges.

Secondly, there's an IPC API in v257 to mount disk images (i.e. file systems stored in regular files) with their UID/GID range mapped to such a dynamic UID/GID range acquired before.

A container runtime thus can first acquire a UID/GID range via the  first API, and then mount a disk image to match that range, …

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573061073096718))

… and then run the container from this combination.

That's already quite powerful, and I use that all the time for running truly unpriv containers from disk images.

As it turns out though running containers of disk images (as opposed to running them from directory trees that are already mounted) is not the most common thing. With v258 we are doing something about it: we set aside one fixed range of 64K host UIDs/GIDs that can now be used for container trees placed in regular directories.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573075074761394))

A new IPC API is now available to work with that: you pass in an fd to the directory, and an fd to a userns, and it returns you a mount fd of the dir, matching the userns. 

And the twist of it: this is accessible to unpriv clients: access will be granted without any further authentication as long as the dir's parent dir is owned by the client's own UID. 

Or in other words: this allows container runtimes to place unpacked container trees in a user's $HOME.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573086693287119))

They just need to make sure these trees are owned by the that new fixed UID range (which we dubbed the "foreign" UID range). After that, the container runtime can dynamically acquire a runtime UID range, then ask the new IPC API to get a mount of the container tree mapped to the runtime UID range, and voilá: fully unpriv containers. Without any "sticky" UID assignments to users or to inodes on disk. And without any suid binary mess.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573089692720081))

Oh, and there's a new "systemd-dissect --shift foreign …" tool that allows you to fix up existing container trees, so that they are re-chown()-ed to the foreign UID range. (This requires privs of course).

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573142351536041))

[@wrybane](https://wizzards.club/@wrybane) The disk images must come with Verity info and a signature for the verity data, which matches a key either known to the kernel or listed in /etc/verity.d/.

Or in other words: the disk images *files* are under full control of the user, but they are validated as they are mounted, and the *contents* of those files must be authenticated by some key known to the system.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573209176000356))

[@valpackett](https://social.treehouse.systems/@valpackett) Yeah, I think so too, they should have just extended the UID range to 64bit or so (or maybe even 128bit, so you can just consider them uuids, like on other OSes).

But I guess they didn't want to touch existing file systems in this regard, as they generally just store 32bit uids/gids, not more...

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573259612421034))

[@TheStroyer](https://mastodon.social/@TheStroyer) the IPC allows two things to unpriv clients: you pass in a dir owned by the foreign UID range whose parent dir is owned by the client UID. This is what my post here mostly talks about. In this case the 64K UIDs/GIDs of the foreign UID range are mapped wholesale to the 64K UIDs/GIDs of the provided userns.

But it also accepts a dir owned directly by the client UID, in which case a mapping with a single UID is created: from the client's UID to root of the container.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573260742220892))

[@TheStroyer](https://mastodon.social/@TheStroyer) the latter should be what you are looking for, as I understand it.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573425874485102))

[@jamesh](https://aus.social/@jamesh) Frankly, maintaining polkit is such a thankless job, nobody is going to be thankful if you maintain that. I feel with the current maintainers...  

But I think you are looking for this, no?  <https://github.com/polkit-org/polkit/pull/501>

in other words: polkit is suid-less these days.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573656071160172))

[@pauldoo](https://mastodon.scot/@pauldoo) no, that's about allocating static uids/gids. for running containers one wants dynamic ones.

also, i think the "drift" problem is a made up problem which can be avoided altogether if people just would make better choices.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114574063401743620))

[@heftig](https://mastodon.online/@heftig) You Sir, are asking the right questions.

<https://github.com/systemd/systemd/pull/37616>

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114573017885620302):** Implementing userns is somewhat painful: a lot of restrictions apply, but from my PoV the messiest part is allocating UID/GID ranges on the host that can be used for each container, in particular when you intend to make use of userns entirely unpriv: how do you take control of a UID range if you yourself run under an unpriv UID range, and UIDs are the fundamental form of security isolation on Linux?

The most widely deployed container engines use a concept called "subuids"/"subgids" for that.

And frankly, I detest the concept oh so very much. First of all they are a relatively static concept, i.e. assign "subordinate" UID/GID ranges persistently to specific users, i.e. they "stick" forever to the user. And not only that, but container trees need to recursively chown()ed to them, which makes them also "stick" to the container trees. Moreover, they only work for unprivileged container managers because they are implemented via a setuid binary.

> **[@valpackett@treehouse.systems](https://social.treehouse.systems/@valpackett/114573180895344032):** [@pid_eins](https://mastodon.social/@pid_eins) the "map to host range" aspect has always been one of the most baffling linux decisions to me. why did they not just introduce a namespace ID as a second key so that (nsid, uid) pairs would become user accounts' actual identifiers, the way freebsd does it >_<

[@valpackett](https://social.treehouse.systems/@valpackett) Yeah, I think so too, they should have just extended the UID range to 64bit or so (or maybe even 128bit, so you can just consider them uuids, like on other OSes).

But I guess they didn't want to touch existing file systems in this regard, as they generally just store 32bit uids/gids, not more...

> **[@TheStroyer](https://mastodon.social/@TheStroyer/114573228532837436):** [@pid_eins](https://mastodon.social/@pid_eins) Would this system also work for mounting regular directories inside unpriviliged containers? I'm always annoyed that the user that created a podman container cannot directly access the contents of a volume mounted in the container

[@TheStroyer](https://mastodon.social/@TheStroyer) the IPC allows two things to unpriv clients: you pass in a dir owned by the foreign UID range whose parent dir is owned by the client UID. This is what my post here mostly talks about. In this case the 64K UIDs/GIDs of the foreign UID range are mapped wholesale to the 64K UIDs/GIDs of the provided userns.

But it also accepts a dir owned directly by the client UID, in which case a mapping with a single UID is created: from the client's UID to root of the container.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114573005995694680)
- [Thread continuation](https://mastodon.social/@pid_eins/114573029973004044)
- [Thread continuation](https://mastodon.social/@pid_eins/114573042603518246)
- [Thread continuation](https://mastodon.social/@pid_eins/114573051904511385)
- [Thread continuation](https://mastodon.social/@pid_eins/114573061073096718)
- [Thread continuation](https://mastodon.social/@pid_eins/114573075074761394)
- [Thread continuation](https://mastodon.social/@pid_eins/114573086693287119)
- [Thread continuation](https://mastodon.social/@pid_eins/114573089692720081)
- [Thread continuation](https://mastodon.social/@pid_eins/114573142351536041)
- [Thread continuation](https://mastodon.social/@pid_eins/114573209176000356)
- [Thread continuation](https://mastodon.social/@pid_eins/114573259612421034)
- [Thread continuation](https://mastodon.social/@pid_eins/114573260742220892)
- [Thread continuation](https://mastodon.social/@pid_eins/114573425874485102)
- [Thread continuation](https://mastodon.social/@pid_eins/114573656071160172)
- [Thread continuation](https://mastodon.social/@pid_eins/114574063401743620)
