---
layout: post
title: "Android USB debugging support"
date: 2025-08-18
---

Here's the 40th post highlighting key new features of the upcoming v258 release of systemd.

It's a quick one:
Android USB debugging might not be an official standard, but it's implemented by a myriad of devices.
Previously accessing Android USB debugging interfaces from regular, unprivileged programs required installation of manual udev rules.
This should now be a thing of the past, we now match these interfaces out of the box and make them accessible through the "uaccess" logic,
i.e. giving any local user with a session in the foreground access to them.

And that's already the whole post for today.

---

> **[@GrapheneOS](https://grapheneos.social/@GrapheneOS)** Users with physical access should have access to arbitrary USB devices. It's the applications which should need to be explicitly granted access to specific USB devices similarly to how it works for USB access on Android and Chromium WebUSB. Android has a system for USB devices and apps to authorize each other with a generic system for users to grant access to applications. On Android, Chromium's WebUSB prompt is really the Android USB prompt which grants access to the app itself too.

Classic Linux is a multi-user OS with security isolation between users.
This means users should not be able to sniff on other user's keyboard or mouse input, or read raw data off block devices bypassing file access restrictions and so on.
Because of all that we cannot just wildcard allow unprivileged users raw access to USB devices: we must enforce access restrictions.

We can allow raw USB access to devices we can be reasonably sure about that cannot be used to bypass Linux access restrictions, sniff on other user's input or output.

Flatpak folks are working on a portal to authorize raw USB access for devices, by the way, mimicking what Android has there a bit.
But that's not for stuff like USB storage or input devices.

> **[@GrapheneOS](https://grapheneos.social/@GrapheneOS)** Defaulting to not permitting USB access to users with physical access inherently has poor usability. It shouldn't be required for users to set up udev rules to access USB devices which weren't considered by udev or the distribution. Sandboxing apps and requiring users to grant access to specific USB devices is what makes sense from a privacy and security perspective. Physical access already gives access to USB devices. Special cases should require special setup, not the general case.

No, more types of USB devices are being special cased in the standard udev rules.
They're added to the list case-by-case based on their IDs so only ones they're aware of and which are already launched can be added.
Google's devices tend to reuse the same IDs for years but they do sometimes change and then it stops working on frozen release distributions for years without users installing rules manually.

Android, ChromeOS, macOS and Windows don't have this problem.

We don't see why desktop Linux distributions can't be as usable as those.
The approach of requiring users with physical access to use root access to set up being able to access USB devices with udev rules doesn't make sense.
Special casing types of devices is not the right approach.
If a computer vendor or sysadmin doesn't want regular users with physical access being able to access a certain USB device, that should be set up as a special case rather than the opposite.

Even for an internal USB connection such as a laptop touchpad, physical access does provide the ability to access it without much difficulty.
If the goal is treating internal connections differently, that should be done as a special case as part of fully supporting specific hardware platforms using USB internally.
Current approach causes major usability issues with USB to try to provide different behavior for internal USB usage without having proper device support.

The current approach is making a significant sacrifice to general usability in order to enforce a security restriction for non-admin users on actual multi-user systems where there's internal usage of USB within the computer.
Bear in mind someone can simply plug a USB device into another computer they fully control.

Desktop OS apps largely not being sandboxed doesn't justify it.
ADB access is the highly invasive if users enable it and authorize access by the computer.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** The portal still can't get around udev. The device needs to be accessible to the user session before the portal can forward it into the sandbox.

We discussed what to do about this at GUADEC.
An idea that came up was to have a dedicated new upstream of "Flathub hwdb rules", which would be separate from systemd.
We'd ask the distros (even LTS) to always keep these rules updated to the latest snapshot.

Then Flathub could match these rules to the devices ask to access.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** That said, I wonder if we should take a more liberal approach and tag entire USB device classes with uaccess, rather than going through VID:PID by VID:PID

HID devices wouldn't do this of course, but I think it's a demonstrative example.
Microsoft has a list of HID devices that the OS takes ownership over (that's the types with "exclusive").
All other HID devices, even those not listed here, are free for use by apps.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** HID is special of course for $reasons, but USB also gives us broader device class identifiers we can match on. And so we can start making similar generalizations:

HID devices need special treatment.
Block devices are owned only by the kernel.
USB COM ports are fine, unless it's a known modem (to be owned by modem manager) or braille display (to be owned by brltty).
Webcams yes.
Printers no.
Audio yes.
Devices in any "vendor" class yes.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** this should probably be fine even for servers, since we're talking about active seats here. People won't be able to access your webcam over ssh, but they will be able to access the webcam when physically at a terminal. And that's fine!

Maybe that goes wrong if you have some special device on a com port and users shouldn't be able to programmatically talk to it, even with an active local seat.
Right now that's presumably covered by our default-deny policy.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** We don't grant access to generic serial devices though, and USB devices of unknown purpose (i.e. anything marked with a vendor-defined USB or HID class), right?

And for HID devices especially, we just treat all HID devices as privileged at the moment right?
Except for game controllers and a hardcoded list of Stream Deck models and whatnot.
We can take the windows approach of only blocking out keyboard/mouse/touchscreen/pen and then leaving pretty much everything else open.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** I mean, this was the fundamental issue with the android adb rules: there is no cleanly recognizable way detect adb, there is no clear device class, no spec. Existing projects hence maintained large lists of vids/pids. The thing we settled on matches a bit more generically, but it's half ugly, because not dependent on anything specified, but just on what we have seen IRL.

We do tag by device classes wherever possible, but certain kind of hardware doesn't have nice device classes, which is where we go by VID/PID in hwdb.
We try to be as coarse as possible but as precise as necessary.

Well, yeah, it's an allowlist situation right now, not a denylist.

Turning this around is a bit ask...
In the security world denylists are icky.

> **[@AdrianVovk](https://fosstodon.org/@AdrianVovk)** hmm, what would these flathub hwdb rules cover that couldn't go upstream into systemd anyway?

Nothing.
But by being separated from upstream systemd we can update them as fast as possible.
Apparently there's even the possibility of getting LTS distros to update this database to the latest version on LTS releases.

We can add things upstream all the time if they make sense.
I can accept that sometimes upstream might be too slow, given we only release every 6 months, but other than that we should generally be friendly to changes like this.

Ok, if this is about speedier release cycles, I can accept this.

> **[@refi64](https://refi64.social/@refi64)** ...

I guess we could add some API to `logind` to allow opening arbitrary device nodes, even for which we have no revoke protocol, after `polkit` authorization, if there's demand for it.
I mean, as long as the polkit request is detailed enough to make somewhat smart decisions this should be fine.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115047948775277368) (2025-08-18)
