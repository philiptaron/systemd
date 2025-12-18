---
layout: post
title: "Stub credentials and boot entries"
date: 2025-06-11
---

Here's the 14th post highlighting key new features of the upcoming v258 release of systemd. #systemd258

The concept of system credentials has existed since a while in systemd. It allows parameterizing the system (and the services running on it) in a secure and hierarchical way. You can pass them into containers and into VMs, for example via SMBIOS Type #11 vendor strings. While the transport is low-level and firmware compatible, they can reasonably only be consumed in userspace.

Sometimes it is useful to parameterize what comes before however, i.e. `systemd-boot` and `systemd-stub`. Since systemd v254 you could already configure the kernel command line via SMBIOS Type #11 vendor strings: that's what `io.systemd.stub.kernel-cmdline-extra=` and `io.systemd.boot.kernel-cmdline-extra=` are for. With v258 we are adding one more SMBIOS Type #11 vendor string: `io.systemd.boot-entries.extra`. It can carry one or more Boot Loader Spec Type #1 definitions of additional boot menu entries.

Such menu items are added to the boot menu, exactly as if they were placed in the ESP next to `systemd-boot` itself.

What's this good for? So that in VM environments the VMM can insert additional recovery or diagnostic boot menu items, that are then combined with those items already on the disk.

This is in particular useful when thinking about network booting: a boot menu entry defined that way could use the `uki-url` stanza to reference a UKI on some network server.

And of course, because boot menu entries defined by the VMM this way are treated like any other, they are also enumerable via `bootctl list`, and can be selected via `systemctl reboot --boot-loader-entry=`, so that userspace can nicely enumerate and pick such items, if they like.

Oh, and don't forget that `systemd-vmspawn` has a nice and simple `--smbios11=` switch that allows configuring vendor strings for this.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114663599190570395) (2025-06-11)
