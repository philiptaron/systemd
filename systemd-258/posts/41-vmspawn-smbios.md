---
layout: post
title: "vmspawn SMBIOS Type 11"
date: 2025-08-19
---

41️⃣ Here's the 41st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

`systemd-vmspawn` is a wrapper around qemu, which makes it work more like `systemd-nspawn`, and provides various bits of integration with systemd (for example, to make really nice unpriv networking work thanks to `systemd-nsresourced` + `systemd-networkd`).

With v258 vmspawn gained a new `--smbios11=` switch. It's an easy way to add SMBIOS Type 11 vendor objects to the VM, or in other words:

You can use it to parameterize the VM in a nice way.

For example, `systemd-boot` now takes the `io.systemd.boot.entries-extra` (see episode 14 of this series) SMBIOS Type 11 object for defining additional boot menu items. You can set these really nicely with the `--smbios11=` switch like so:

```
--smbios11=io.systemd.boot.entries-extra:particleos-current.conf=$'title ParticleOS Current\nuki-url http://example.com/somedir/uki.efi'
```

This adds a new boot entry, defining it to download the specified UKI via UEFI…HTTP boot and booting into it. An orchestrator could use this to generically install a boot menu item in all its VMs that help with recovery, reset or backup of its VMs or similar logic.

Note that you can also pass system credentials via SMBIOS Type 11 to a VM, hence you could set those via `--smbios11=` too. But it's kinda pointless given that we have explicit `--set-credential=/--load-credential=` knobs for that, which are more powerful.

We maintain a list of SMBIOS Type 11 objects systemd cares for in a man page:

---

## Questions & Answers

> **Q: Does the unpriv networking handle providing IPv6 to guests better than a standard qemu-system-x86_64 invocation with `-netdev user` does?**

I have no idea what "better" constitutes, but it just lets networkd configure the device, and this is the default config:
https://github.com/systemd/systemd/blob/main/network/80-namespace-ns-tun.network

i.e. it does ipv6 masquerading.

---

## Reference Links

- [smbios-type-11 man page](https://www.freedesktop.org/software/systemd/man/devel/smbios-type-11.html)
- [systemd-vmspawn](https://www.freedesktop.org/software/systemd/man/259/systemd-vmspawn.html)
- [systemd-boot](https://www.freedesktop.org/software/systemd/man/259/systemd-boot.html)
- [80-namespace-ns-tun.network config](https://github.com/systemd/systemd/blob/main/network/80-namespace-ns-tun.network)

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115054570728027141) (2025-08-19)
