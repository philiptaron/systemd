# v259 Feature Highlight #12

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins)
**Posted:** 2025-12-05 09:02 UTC
**Original:** [https://mastodon.social/@pid_eins/115666147093865447](https://mastodon.social/@pid_eins/115666147093865447)

---

1️⃣2️⃣ Here's the 12th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

systemd-vmspawn is a small wrapper around qemu that provides various VM integration points with systemd infrastructure, such as ready notification, credential passing, machined integration and so on.

With v259 it gained one additional little feature for integrating VMs better in the host:


---

## Thread Continuation

### [2025-12-05 09:06 UTC](https://mastodon.social/@pid_eins/115666161827220886)

If you attach multiple disks to an vmspawn invocation via --extra-drive= then the "serial" field of the exposed disk will be initialized automatically to the specified filename of the disk on the host. This has the effect that a symlink for the device will appear in /dev/disk/by-id/… that is generated from the host side filename of the disk. And that's just so useful, because it essentially means the identifier for some disk on host and in the VM is the same (well, not literally, …

### [2025-12-05 09:06 UTC](https://mastodon.social/@pid_eins/115666162777933170)

… but closely related).


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115666147093865447)*