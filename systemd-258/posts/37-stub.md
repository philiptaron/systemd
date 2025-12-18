---
layout: post
title: "systemd 258 Feature Highlight #37"
date: 2025-08-13
source: https://mastodon.social/@pid_eins/115021969729733421
author: Lennart Poettering
---

3️⃣7️⃣ Here's the 37th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258) 

Back in v257 we added support to sd-stub to automatically load a Devicetree file matching the local system by looking for it in the invoked UKI PE binary, using a "CHID" as lookup key. In v258 we also added support for invoking UEFI firmware update capsules via UKI CHID matching (see the 15th episode of the current series about that).

CHIDs are a Microsoft spec that calculates…

## Thread Continuation

*2025-08-13* ([source](https://mastodon.social/@pid_eins/115021994570695929))

(the latter include EDID display data hashed together with the SMBIOS data CHIDs are usually hashed from)

*2025-08-14* ([source](https://mastodon.social/@pid_eins/115025519722001243))

[@valpackett](https://social.treehouse.systems/@valpackett) via EFI_EDID_DISCOVERED_PROTOCOL

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115021980078396928):** …various UUIDs identifying the model of the local system. It's widely used on Windows (to automatically find drivers matching the local system), and now we use it in our UEFI code too for similar purposes.

But how do you actually figure out the CHIDs for your local system? The new v258 systemd-analyze command "chid" will help you there: it will calculate all standard CHIDs of the local system, plus some extended CHIDs specific to systemd.

(the latter include EDID display data hashed together with the SMBIOS data CHIDs are usually hashed from)

## Sources

- [Original post](https://mastodon.social/@pid_eins/115021969729733421)
- [Thread continuation](https://mastodon.social/@pid_eins/115021994570695929)
- [Thread continuation](https://mastodon.social/@pid_eins/115025519722001243)
