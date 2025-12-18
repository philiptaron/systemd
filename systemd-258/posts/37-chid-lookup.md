---
layout: post
title: "`CHID` lookup tool"
date: 2025-08-13
---

Here's the 37th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Back in v257 we added support to `sd-stub` to automatically load a Devicetree file matching the local system by looking for it in the invoked `UKI` PE binary, using a `CHID` as lookup key.
In v258 we also added support for invoking UEFI firmware update capsules via `UKI` `CHID` matching (see the 15th episode of the current series about that).

`CHID`s are a Microsoft spec that calculates various UUIDs identifying the model of the local system.
It's widely used on Windows (to automatically find drivers matching the local system), and now we use it in our UEFI code too for similar purposes.

But how do you actually figure out the `CHID`s for your local system?
The new v258 `systemd-analyze` command `chid` will help you there: it will calculate all standard `CHID`s of the local system, plus some extended `CHID`s specific to systemd.

(The latter include `EDID` display data hashed together with the `SMBIOS` data `CHID`s are usually hashed from.)

---

## Related Discussions

> **How do you get EDID access in the stub?**

via the `EFI_EDID_DISCOVERED_PROTOCOL` protocol

---

[systemd-analyze]: https://www.freedesktop.org/software/systemd/man/258/systemd-analyze.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115021969729733421) (2025-08-13)
