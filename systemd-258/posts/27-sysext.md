---
layout: post
title: "systemd 258 Feature Highlight #27"
date: 2025-07-03
source: https://mastodon.social/@pid_eins/114788278114378875
author: Lennart Poettering
---

2️⃣7️⃣ Here's the 27th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

You might have heard of systemd-confext before. It's just like systemd-sysext, but applies its magic to /etc/ rather than /usr/. In case you never heard of systemd-sysext either: it's a mechanism for merging a number of disk images (DDIs specifically) on top of /usr/ via overlayfs so that /usr/ becomes a stack of (immutable) images, that appears as one file system tree.

## Thread Continuation

*2025-07-03* ([source](https://mastodon.social/@pid_eins/114788294396239463))

systemd-confext does all this for /etc/, it's hence a powerful alternative to traditional configuration management: instead of modifying a mutable /etc without chance of undoing things, and without ability to trace back changes to their sources, it manages a strictly immutable /etc/ with some flexibility, but allows whole sets of files to come and go, in a way they can always be traced back to their origin (i.e. to the layer, and thus signed disk image it originates from).

*2025-07-03* ([source](https://mastodon.social/@pid_eins/114788304833026317))

Both concepts (i.e. sysext + confext) exist for the system as a whole *and* per-service, managed automatically via portable services, or more manually by using the ExtensionImages=/ExtensionDirectories= unit file settings.

The latter makes a ton of sense for systemd-confext in particular: the set of configuration files for a service X should be associated with that service X, but still permit management of the code and configuration of X separately. And ExtensionImages=/ExtensionDirectories=…

*2025-07-03* ([source](https://mastodon.social/@pid_eins/114788315148174526))

…allow just that: if used the service will run in its own mount namespace, and get a stack of confext images on /etc/.

Of course, when managing configuration per-service in this novel, immutable, atomic, secure way, then there also needs to be a nice way to update the config.

In v258 we added provisions that the usual "systemctl reload" you can run on a service will also refresh the confext stack for the service, and merge in newer versions of any confext DDIs dropped in, fully atomically.

*2025-07-03* ([source](https://mastodon.social/@pid_eins/114788324833152110))

Or in other words: whenever some orchestrator tooling wants to update the configuration for a specific service, it now just needs to drop-in a new version of the config, nicely wrapped in a confext, then issue a regular service reload, which makes the confext appear in the service's file system view, and then ask the service to reload.

The concept is designed to be used with the .v/ directory functionality, i.e. where you point systemd to a .v/ directory, and systemd…

*2025-07-03* ([source](https://mastodon.social/@pid_eins/114788333020688316))

…automatically picks the newest image file in that directory.

Securely, robustly updating a whole service config consisting of many files by just dropping in a single file, that's awesome, no? At least in PoV that's quite an improvement over traditional configuration management schemes!

Note that the confext stack is refreshed *before* the actual reload of the service happens, i.e. before ExecReload= is run or SIGHUP are sent, to ensure that the service sees the update by then.

*2025-07-03* ([source](https://mastodon.social/@pid_eins/114788349112387553))

One thing I'd like to add in one of the next versions is that systemd implicitly picks up all confext DDIs from /etc/systemd/system/<servicename>.confext.d/* without this requiring any explicit configuration. i.e. similar to how it generates Wants= deps from /etc/systemd/system/<servicename>.wants/*, it would synthesize ExtensionImages= equivalent setting lines for each entry in ….confext.d/*.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114788287134783211):** systemd-sysext is fantastic way to add a bit of flexibility to /usr/ in a world where /usr/ is otherwise immutable. It has various really nice benefits: it's atomic in behaviour (i.e, a sysext image is either merged in or not merged in, but never "half" installed), it can trivially be undone (if you remove an image from the stack it's just gone again), and the security properties are great too (i.e. offline security, signatures checked against kernel keyring).

systemd-confext does all this for /etc/, it's hence a powerful alternative to traditional configuration management: instead of modifying a mutable /etc without chance of undoing things, and without ability to trace back changes to their sources, it manages a strictly immutable /etc/ with some flexibility, but allows whole sets of files to come and go, in a way they can always be traced back to their origin (i.e. to the layer, and thus signed disk image it originates from).

## Sources

- [Original post](https://mastodon.social/@pid_eins/114788278114378875)
- [Thread continuation](https://mastodon.social/@pid_eins/114788294396239463)
- [Thread continuation](https://mastodon.social/@pid_eins/114788304833026317)
- [Thread continuation](https://mastodon.social/@pid_eins/114788315148174526)
- [Thread continuation](https://mastodon.social/@pid_eins/114788324833152110)
- [Thread continuation](https://mastodon.social/@pid_eins/114788333020688316)
- [Thread continuation](https://mastodon.social/@pid_eins/114788349112387553)
