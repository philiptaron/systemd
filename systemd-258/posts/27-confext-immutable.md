---
layout: post
title: "systemd-confext immutable configuration"
date: 2025-07-03
---

Here's the 27th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

You might have heard of `systemd-confext` before.
It's just like `systemd-sysext`, but applies to `/etc/` rather than `/usr/`.
In case you never heard of `systemd-sysext` either: it's a mechanism for merging a number of disk images (DDIs specifically) on top of `/usr/` via overlayfs so that `/usr/` becomes a stack of (immutable) images that appears as one file system tree.

## Benefits of `systemd-sysext`

`systemd-sysext` is a fantastic way to add a bit of flexibility to `/usr/` in a world where `/usr/` is otherwise immutable.
It has various really nice benefits: it's atomic in behavior (i.e., a sysext image is either merged in or not merged in, but never "half" installed), it can trivially be undone (if you remove an image from the stack it's just gone again), and the security properties are great too (i.e., offline security, signatures checked against kernel keyring).

## Configuration Management with systemd-confext

`systemd-confext` does all this for `/etc/`, providing a powerful alternative to traditional configuration management: instead of modifying a mutable `/etc/` without chance of undoing things and without the ability to trace back changes to their sources, it manages a strictly immutable `/etc/` with some flexibility but allows whole sets of files to come and go in a way they can always be traced back to their origin (i.e., to the layer and thus the signed disk image it originates from).

## Per-Service Configuration

Both concepts (i.e., `sysext` and `confext`) exist for the system as a whole *and* per-service, managed automatically via portable services or more manually by using the `ExtensionImages=` and `ExtensionDirectories=` unit file settings.

The latter makes a lot of sense for `systemd-confext` in particular: the set of configuration files for a service X should be associated with that service X but still permit management of the code and configuration of X separately.
When used, the service will run in its own mount namespace and get a stack of confext images on `/etc/`.

## Configuration Updates

Of course, when managing configuration per-service in this novel, immutable, atomic, secure way, then there also needs to be a nice way to update the config.

In v258 we added provisions so that the usual `systemctl reload` you can run on a service will also refresh the confext stack for the service and merge in newer versions of any confext DDIs dropped in, fully atomically.

Or in other words: whenever some orchestrator tooling wants to update the configuration for a specific service, it now just needs to drop-in a new version of the config, nicely wrapped in a confext, then issue a regular service reload, which makes the confext appear in the service's file system view, and then ask the service to reload.

The concept is designed to be used with the `.v/` directory functionality, i.e., where you point systemd to a `.v/` directory and systemd automatically picks the newest image file in that directory.

Securely and robustly updating a whole service config consisting of many files by just dropping in a single file is pretty great.
That's quite an improvement over traditional configuration management schemes!

Note that the confext stack is refreshed *before* the actual reload of the service happens, i.e., before `ExecReload=` is run or `SIGHUP` signals are sent, to ensure that the service sees the update by then.

## Future Plans

One thing I'd like to add in one of the next versions is that systemd implicitly picks up all confext DDIs from `/etc/systemd/system/<servicename>.confext.d/*` without this requiring any explicit configuration. I.e., similar to how it generates `Wants=` dependencies from `/etc/systemd/system/<servicename>.wants/`, it would synthesize `ExtensionImages=` equivalent setting lines for each entry in `.confext.d/`.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114788278114378875) (2025-07-03)
