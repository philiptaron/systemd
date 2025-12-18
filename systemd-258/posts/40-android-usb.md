---
layout: post
title: "Android USB debugging support"
date: 2025-08-18
---

Android USB debugging might not be an official standard, but it's implemented by a myriad of devices.
Previously accessing Android USB debugging interfaces from regular, unprivileged programs required installation of manual `udev` rules.
This should now be a thing of the past: we now match these interfaces out of the box and make them accessible through the `uaccess` logic, i.e. giving any local user with a session in the foreground access to them.

And that's already the whole post for today.

---

> **GrapheneOS** asks about allowing raw USB device access for unprivileged users

Classic Linux is a multi-user OS with security isolation between users.
This means users should not be able to sniff on other user's keyboard or mouse input, or read raw data off block devices bypassing file access restrictions and so on.
Because of all that we cannot just wildcard allow unprivileged users raw access to USB devices: we must enforce access restrictions.

We can allow raw USB access to devices we can be reasonably sure about that cannot be used to bypass Linux access restrictions, sniff on other user's input or output.
Flatpak folks are working on a portal to authorize raw USB access for devices, by the way, mimicking what Android has there a bit.
But that's not for stuff like USB storage or input devices.

> **Questions about device tagging and ADB detection**

We do tag by device classes wherever possible, but certain kinds of hardware don't have nice device classes, which is where we go by VID/PID in `hwdb`.
We try to be as coarse as possible but as precise as necessary.

I mean, this was the fundamental issue with the Android ADB rules: there is no cleanly recognizable way to detect ADB, there is no clear device class, no spec.
Existing projects hence maintained large lists of VID/PIDs.
The thing we settled on matches a bit more generically, but it's half ugly, because it's not dependent on anything specified, but just on what we have seen in real life.

> **Discussion on allowlist vs denylist approach**

Well, yeah, it's an allowlist situation right now, not a denylist.
Turning this around is a bit of an ask... in the security world denylists are icky...

> **Regarding Flatpak hwdb rules**

Hmm, what would these Flatpak hwdb rules cover that couldn't go upstream into systemd anyway?
We can add things upstream all the time if they make sense.
I can accept that sometimes upstream might be too slow, given we only release every 6 months, but other than that we should generally be friendly to changes like this.

OK, if this is about speedier release cycles, I can accept this.

> **Polkit authorization for device access**

I guess we could add some API to `logind` to allow opening arbitrary device nodes, even for which we have no revoke protocol, after `polkit` authorization, if there's demand for it.
I mean, as long as the `polkit` request is detailed enough to make somewhat smart decisions this should be fine.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115047948775277368) (2025-08-18)
