---
layout: post
title: "systemd-homed areas"
date: 2025-05-22
---

Here's the 2nd post highlighting key new features of the upcoming v258 release of systemd.

On UNIX systems every user registered on a local user owns a private directory: the "home" directory, where the user's configuration and data is saved and stored.
In systemd there's [`systemd-homed`][systemd-homed] which can manage that home directory securely, encrypted with a key that is provided at login time.

In most cases having a single home directory for each user is enough.

But in various scenarios it is handy to have a single login account, but multiple home directories one can switch between, for example to maintain different configuration sets, or build environments, possibly for different hosts.

In v258 [`systemd-homed`][systemd-homed] (and by extension the userdb logic) has a concept for maintaining multiple "areas" for each user account.
Areas in this sense are simply subdirectories of the main home directory, below the `~/Areas/` hierarchy.
A user can have as many of these as they want, and easily switch between them, simply by logging in specifying a user name of `"username%areaname"` at login time, when the system asks for a username.

This will primarily do two things: if you log in as user `"foo"` with area `"bar"` (i.e. specify `"foo%bar"` at login time), you end up with `$HOME` set to `/home/foo/Areas/bar`; it will also do something similar for `$XDG_RUNTIME_DIR`, to give your session a separate runtime directory.

In order to create such an area anew you can simply call `mkdir -p ~/Areas && cp -av /etc/skel ~/Areas/mynewarea`.
To remove it again just do `rm -rf ~/Areas/mynewarea` – you get the idea.

Of course, since all areas are owned by the same underlying UID, and associated with the same user record you can easily move around between the areas and the main home directory, via `cd` and similar.

The simple concept of areas can be used in various quite powerful ways.

My personal usecase for this goes something like this: I regularly build disk images for VMs of different distributions on my host, for building and testing systemd and other stuff.
And I want access to my host user's home dir in each when booting them up, but not necessarily log directly into my host's home directory, but keep a separate area for each such image, so that the build trees in it can be distinct, do not leak context into each other, and can be created anew and flushed out easily.
I also want full access to all my data from each such VM to simplify my work.
And the area concept allows me to do all that.

Note that while this 'virtualizes' `$HOME` and `$XDG_RUNTIME_DIR` nicely, it's not quite enough to run multiple full desktop environments in parallel for each user by giving them each an area of their own.
That's because the per-user service manager only exists once right now, not in one instance per area.

But there's no reason for not supporting that properly besides of "Lennart didn't find the time to make it work yet".
I think we should totally support that too, so that each user can have one per-user service manager for the main area, and then one for each additional area.
With that in place, you could have multiple parallel DE sessions, nicely separated in context (but not in privilege) in parallel, from the same home dir.

And before you ask: all this is a [`systemd-homed`][systemd-homed] feature, it's not implemented for classic UNIX users (as systemd is not involved with management of them, and couldn't do the area management there), and it's unlikely it will ever be.
The user record extensions to make areas a thing are generic though.

---

[systemd-homed]: https://www.freedesktop.org/software/systemd/man/258/systemd-homed.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114550305394053015) (2025-05-22)
