---
layout: post
title: "systemd-homed signing keys"
date: 2025-08-14
---

Here's the 38th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

`systemd-homed` managed users/home directories are supposed to be self-contained and portable between systems: it's sufficient to move the home dir from one system to another to make the user available there, with all its data and metadata, ready for login.

Except of course this is not quite true: there's an extra step involved for security reasons:

Every user record is cryptographically signed (asymmetrically), and if the target system does not recognize the (public) key it is signed with, it will ignore the home directory. This is done so that simply placing a foreign home dir on some target system doesn't magically give you access to the target system.

Previously, while this signing logic was documented, there were no tools to help you with managing them. You'd have to copy the signing keys between systems fully manually.

With v258 that has changed. There are a bunch of commands available now that help you manage the keys.

`homectl list-signing-keys` lists the signing keys (well, the public parts of the keypairs) accepted locally, by their name (which is just a freely choosable filename each key is stored under; only one name is a bit special: the key pair called "local" is the one implicitly created locally if you create a user and don't have any signature key yet).

`homectl get-signing-key` allows you to get the public part of a specific signing key, `homectl add-signing-key` allows you to install a signing key locally (the public part of it), `homectl remove-signing-key` allows you to remove one again.

These commands are designed to be used in shell pipelines, i.e. getting a signing key will write the key data to stdout, and adding one will read it from stdin.

**Example use:**

```
homectl get-signing-key local.public | ssh targetsystem homectl add-signing-key --key-name=foobar.public
```

This gets the public part of the local key pair, and installs it on a remote system, renaming it to "foobar" on the fly (because that target system of course already has a local key, which is distinct, and we don't want to override).

And with that and user/home dir created locally will also be accepted on the specified target system for login.

**A more complex example:**

```
homectl update lennart --ssh-authorized-keys=... -N --storage=cifs --cifs-service="//$HOSTNAME/lennart"
homectl get-signing-key | ssh targetsystem homectl add-signing-key --key-name="$HOSTNAME".public
homectl inspect -E lennart | ssh targetsystem homectl register -
ssh lennart@targetsystem
```

What does this do? The first line updates the local user "lennart" to carry an SSH public key. It also declares that if the account is accessed from any system but the local one, it should use "cifs" storage instead of the usual one (which is likely "luks"). CIFS of course is the Linux name of the windows-style file sharing protocol (usually called SMB). And the CIFS share to access for the home directory should be the one of the local system. (The -N switch enforces the "any but local" rule btw, see man page).

With this first line we thus have done two things: first of all, the account becomes remotely accessible via SSH, secondly if the account is used on other systems, the original home directory shall be accessed via CIFS on the currently local system.

The second line then copies the local signing key to some target system, as in the first example.

The third line then propagates the user record from the local system to the same target system (but only the record, not the home dir!).

The fourth line then uses SSH to log into our account, on the target system, which will then automatically mount the specified CIFS share as home dir there, from our source system.

Or in other words: you can take your account/home dir "with you" onto a target system this way, all through high-level commands.

(This of course only works if you have samba installed locally, so that the local home dirs are actually accessible through CIFS from other systems)

Let me emphasize one thing: even though this uses SMB/CIFS, it uses it in file sharing mode only, i.e. the source and the target system don't have to be in the same windows domain or anything like that, they don't have to share user records otherwise, and the only daemon that needs to run for this (beyond `homed`) is the samba service on the system that carries the original home dir.

And yeah, I wished there was something simpler than CIFS/SMB for just sharing some directory across the network safely in a somewhat posixy kind of way, alas there really isn't anything I was aware of that wasn't awful.

(NFS is not a candidate, because it's requirements on syncing UIDs, which we really don't want here, we want to decide the UID to use for the fs share on the target system, not on the source)

---

> **Note from Lennart on NFS alternatives:** Never played with that, but last time I looked NFS always needs some per-system uid translation daemon, which rules this out for this usecase. Also, NFS is not simpler than CIFS, quite the opposite, it's a monster.

---

[homectl]: https://www.freedesktop.org/software/systemd/man/258/homectl.html
[systemd-homed]: https://www.freedesktop.org/software/systemd/man/258/systemd-homed.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115025535193319606) (2025-08-14)
