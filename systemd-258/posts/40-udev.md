---
layout: post
title: "systemd 258 Feature Highlight #40"
date: 2025-08-18
source: https://mastodon.social/@pid_eins/115047948775277368
author: Lennart Poettering
---

4️⃣0️⃣ Here's the 40th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

It's a quick one: Android USB debugging might not be an official standard, but it's implemented by a myriad of devices. Previously accessing Android USB debugging interfaces from regular, unprivileged programs required installation of manual udev rules.This should now be a thing of the past, we now match these interfaces out of the box and make them accessible through the "uaccess"…

## Thread Continuation

*2025-08-19* ([source](https://mastodon.social/@pid_eins/115054517934270900))

[@GrapheneOS](https://grapheneos.social/@GrapheneOS) Classic Linux is a multi-user OS with security isolation between users. This means users should not be able to sniff on other user's keyboard or mouse input, or read raw data off block devices bypassing file access restrictions and so on. Because of all that we cannot just wildcard allow unpriv users raw access to USB devices: we must enforce access restrictions.

*2025-08-19* ([source](https://mastodon.social/@pid_eins/115054528507863864))

[@GrapheneOS](https://grapheneos.social/@GrapheneOS) We can allow raw USB access to devices we can be reasonably sure about that cannot be used to bypass Linux access restrictions, sniff on other user's input or output.

Flatpak folks are working on a portal to authorize raw USB access for devices, btw, mimicking what android has there a bit. But that's not for stuff like usb storage or input devices.

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065417391466686))

[@AdrianVovk](https://fosstodon.org/@AdrianVovk) [@GrapheneOS](https://grapheneos.social/@GrapheneOS) we do tag by device classes wherever possible, but certain kind of hw doesnt have nice device classes, which is where we go by vid/pid in hwdb. We try to be as coarse as possible but as precise as necessary.

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065473764035055))

[@AdrianVovk](https://fosstodon.org/@AdrianVovk) hmm, what would these flathub hwdb rules cover that couldn't go upstream into systemd anyway? we can add things upstream all the time if they make sense. (i can accept that sometimes upstream might be too slow, given we only release every 6 months, but other than that we should generally be friendly to changes like this)

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065513657988302))

[@AdrianVovk](https://fosstodon.org/@AdrianVovk) [@GrapheneOS](https://grapheneos.social/@GrapheneOS) I mean, this was the fundamental issue with the android adb rules: there is no cleanly recognizable way detect adb, there is no clear device class, no spec. Existing projects hence maintained large lists of vids/pids. The thing we settled on matches a bit more generically, but it's half ugly, because not dependent on anything specified, but just on what we have seen IRL.

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065585930285360))

[@AdrianVovk](https://fosstodon.org/@AdrianVovk) ok, if this is about speedier release cycles, I can accept this.

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065946388147002))

[@AdrianVovk](https://fosstodon.org/@AdrianVovk) [@GrapheneOS](https://grapheneos.social/@GrapheneOS) well, yeah, it's an allowlist situation right now, not a denylist.

Turning this around is a bit ask... in the security world denylists are icky...

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115067248141690513))

[@refi64](https://refi64.social/@refi64) [@AdrianVovk](https://fosstodon.org/@AdrianVovk) [@GrapheneOS](https://grapheneos.social/@GrapheneOS) i guess we could add some API to logind to allow opening arbitrary device nodes, even for which we have no revoke protocol, after polkit authorization, if there's demand for it. I mean, as long as the polkit request is detailed enough to make somewhat smart decisions this should be fine.

## Sources

- [Original post](https://mastodon.social/@pid_eins/115047948775277368)
- [Thread continuation](https://mastodon.social/@pid_eins/115054517934270900)
- [Thread continuation](https://mastodon.social/@pid_eins/115054528507863864)
- [Thread continuation](https://mastodon.social/@pid_eins/115065417391466686)
- [Thread continuation](https://mastodon.social/@pid_eins/115065473764035055)
- [Thread continuation](https://mastodon.social/@pid_eins/115065513657988302)
- [Thread continuation](https://mastodon.social/@pid_eins/115065585930285360)
- [Thread continuation](https://mastodon.social/@pid_eins/115065946388147002)
- [Thread continuation](https://mastodon.social/@pid_eins/115067248141690513)
