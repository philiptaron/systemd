---
layout: post
title: "systemd 258 Feature Highlight #25"
date: 2025-07-01
source: https://mastodon.social/@pid_eins/114776832571027618
author: Lennart Poettering
---

2️⃣5️⃣ Here's the 25th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

When booting up a systemd-nspawn container interactively there's a special key combination Ctrl-] you can hit three times within 1s, to terminate the container. 

This termination is abrupt: all processes in the container are immediately terminated, there's no clean shutdown phase.

## Thread Continuation

*2025-07-01* ([source](https://mastodon.social/@pid_eins/114776865643563371))

First of all there's ^]^]r for rebooting the container. It's mostly identical to typing "reboot" in such a full-blown container, or to calling "machinectl reboot" on it from the outside.

And then there's ^]^]p for powering off a container. You guessed, it's equivalent to typing "poweroff" in the contianer, or calling "machinectl poweroff" from the outside.

(Note that this only works if you actually run an init system inside the container, and it must implement SIGRTMIN+4/SIGRTMIN+5…

*2025-07-01* ([source](https://mastodon.social/@pid_eins/114776868849222897))

…as a way of powering off or rebooting the container, compatible with how systemd itself has been doing it).

*2025-07-01* ([source](https://mastodon.social/@pid_eins/114776905820743481))

[@agowa338](https://chaos.social/@agowa338) I actually use a German layout, and I just hit LStrg+AltGr+9 twice and then r or p.

It's supposed to be something you cannot hit by accident.

*2025-07-01* ([source](https://mastodon.social/@pid_eins/114776973344351380))

[@agowa338](https://chaos.social/@agowa338) it's a separate key on german keyboards

*2025-07-01* ([source](https://mastodon.social/@pid_eins/114780158763499733))

[@amackif](https://mastodon.social/@amackif) fedora, but I disable selinux, the policies are always lagging behind upstream development. Unfortunately selinux policy support is very much lacking in Fedora land.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114776846571848929):** That is great for debugging, but it's not ideal for production: there it would be better to let the applications inside the container save their data properly, and let the system shut down cleanly. After all, systemd-nspawn is mostly focussed on running full blown containers with init systems as PID1, and that means one better should let the init system inside do its clean shutdown logic.

In v258 there's now an easy way to do just that. In addition to ^]^]^] there are now two new hotkeys.

First of all there's ^]^]r for rebooting the container. It's mostly identical to typing "reboot" in such a full-blown container, or to calling "machinectl reboot" on it from the outside.

And then there's ^]^]p for powering off a container. You guessed, it's equivalent to typing "poweroff" in the contianer, or calling "machinectl poweroff" from the outside.

(Note that this only works if you actually run an init system inside the container, and it must implement SIGRTMIN+4/SIGRTMIN+5…

> **[@amackif](https://mastodon.social/@amackif/114779399063231206):** [@pid_eins](https://mastodon.social/@pid_eins) somewhat related, which distro do you use? Just tried to run importctl on fedora host for image either fedora, Ubuntu or opensuse and it fails due to selinux. I know selinux is not your responsibility, but wondering how you deal with this if the answer is fedora (assuming you run fedora because of your past red hat employment)

[@amackif](https://mastodon.social/@amackif) fedora, but I disable selinux, the policies are always lagging behind upstream development. Unfortunately selinux policy support is very much lacking in Fedora land.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114776832571027618)
- [Thread continuation](https://mastodon.social/@pid_eins/114776865643563371)
- [Thread continuation](https://mastodon.social/@pid_eins/114776868849222897)
- [Thread continuation](https://mastodon.social/@pid_eins/114776905820743481)
- [Thread continuation](https://mastodon.social/@pid_eins/114776973344351380)
- [Thread continuation](https://mastodon.social/@pid_eins/114780158763499733)
