---
layout: post
title: "systemd 258 Feature Highlight #8"
date: 2025-06-02
source: https://mastodon.social/@pid_eins/114611768708184175
author: Lennart Poettering
---

8️⃣ Here's the 8th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Since a long time systemd has had the ConditionHost= unit file setting, which allows limiting execution of a unit to a specific host. As argument it takes either a hostname (with shell-style globbing, nicely aligning with the question mark logic in /etc/hostname, as in the 5th episode of this season of this series), or a machine ID (i.e. /etc/machine-id) specification.

## Thread Continuation

*2025-06-02* ([source](https://mastodon.social/@pid_eins/114611806579767938))

… the setting may now also match against the boot ID (i.e /proc/sys/kernel/random/boot_id) and the product ID of the hardware (i.e. `run0 varlinkctl call /run/systemd/io.systemd.Hostname io.systemd.Hostname.Describe '' | jq -r .ProductUUID`).

The former is useful as it means you can deploy configuration that will only apply to a certain *state* of the system, while the latter might be useful if your inventory tracks hardware instead of OS installations.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114611786373552753):** This is useful as you can ship a single configuration for a fleet of devices, but still have some of it be specific to a subset (or exclude a subset) of the whole fleet. (In fact, by combining the question mark stuff with the glob matching you can even execute services on a randomized subset of your fleet this way…)

With v258 we are slightly extending ConditionHost= a bit. In addition to matching against the two aforementioned host identifiers, …

… the setting may now also match against the boot ID (i.e /proc/sys/kernel/random/boot_id) and the product ID of the hardware (i.e. `run0 varlinkctl call /run/systemd/io.systemd.Hostname io.systemd.Hostname.Describe '' | jq -r .ProductUUID`).

The former is useful as it means you can deploy configuration that will only apply to a certain *state* of the system, while the latter might be useful if your inventory tracks hardware instead of OS installations.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114611768708184175)
- [Thread continuation](https://mastodon.social/@pid_eins/114611806579767938)
