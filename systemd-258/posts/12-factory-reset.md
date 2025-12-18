---
layout: post
title: "Comprehensive factory reset mechanisms"
date: 2025-06-06
---

I believe a fundamental aspect of OS security must be a secure way to return the OS into a well-defined, secure state if a compromise has been identified.

Fending off an attacker is one thing, accepting that it might happen anyway and that you can recover from that in a reasonable way is another.
And that's the case not only if you think about "cattle" style installs (i.e. lots of similar systems running the same OS image), but equally on "pet" style installs (i.e. your personal device).

Or to turn this around: a system that doesn't come with a clean, well defined mechanism to reset it fully, erase all unauthenticated data and return it to a vendor image without any local modifications, is highly problematic I believe.

Now you might say: "I can always reinstall my Linux" and start from scratch.
And to some point you are right even.
But only to some point.
First of all "reinstalling your Linux" is not precisely a trivial operation, and secondly, in today's world it's actually not really going to suffice in many ways.
That's because it's not sufficient to erase your HDD and reinitialize it.
There's more state to reset.
One of them in particular is the TPM: local key material is derived from or protected by a "seed" key stored on the TPM.

If you do not invalidate the old seed key and generate a new one, then all secrets associated with the compromised install (and thus tainted) will remain valid.

And there's more: there are various bits stored in EFI vars NVRAM that need to be reset too (shim keys for example).

`systemd` for a longer time has had really nice support for resetting your HDD (i.e. securely erase partitions, via the `systemd-repart` `FactoryReset=` knob) if a factory reset is requested.

With v258 we considerably extended this work.
There's now a well defined way to extend the factory reset logic so that other subsystems can be reset too.
And we do ship one plugin for that (which is enabled by default), that requests a TPM reset from the firmware.

If your OS is properly set up for that you can now issue `systemctl start factory-reset.target`.
This will initiate a reboot, but a special one, where first the firmware will reset the TPM, and then the OS will reset its own state.

And once the system comes back again the system is fully reset.

This currently does not cover EFI var NVRAM reset natively, but there's a clean plugin interface now to do that eventually (two actually: one place where you can plug in such code *before* we reboot, and one place *after* we reboot).
[I'd expect that in one of the next releases we'll add another plugin for this, that erases certain EFI vars in NVRAM.]

There's also now a Varlink based API to query the current factory reset state (i.e. is a factory reset pending for the next reboot, or are we currently executing one for the current boot, or did we already finish one for the current boot, or is none pending nor executing).

If you want to learn more about the factory reset concepts in systemd, there is a new document for this:
[Factory Reset Documentation](https://github.com/systemd/systemd/blob/main/docs/FACTORY_RESET.md)

Oh, and of course: our ParticleOS images have been updated to expose this kind of thorough factory reset that covers the TPM already.
You can simply select "factory reset" in the boot menu, and all non-authenticated data is gone.

And finally: if you run an OS in production and it has no clear story for factory reset, maybe talk to your vendor, and ask them to get back to the drawing board, and fix their mess.

---

> **[@anselmschueler](https://ieji.de/@anselmschueler):** [Question about authentication for factory reset]

Which password?

It's supposed to be a mechanism to get a working system back if you forgot your disk encryption passwords, so that the system is not bricked for good, you know.

It's the same as it is for your Android phone for example, where you can do a factory reset from the boot menu too – without authentication.

So no, we do not ask for authentication: if you managed to get this kind of access to the boot menu to be able to select it, you are god anyway.

---

> **[@siosm](https://floss.social/@siosm):** [Questions about trust and rebooting]

You definitely need to reboot, to get back into an unbroken chain of trust.
Now you have two ways to ensure this works.
First of all you physically request the reset early during boot.
That's why we have this in the boot menu.
Or you ask for the reset from the compromised running system, and then use some form of attestation to validate that the reboot was genuine.
The latter is stuff bigger deployments (i.e. companies which actually do attestation) can do, …

…but for the local personal device case ("pet") is indeed not really realistic.
At least not right now, hence boot loader reset it is for that case, if your factory reset is about trust.
(if your factory reset is not about trust, doing factory reset via UI is of course always fine).

If you request a factory reset from a running system a single reboot should suffice: we ask firmware to reset TPM on reboot, set a flag to reset disk on reboot, then reboot.
Done.

If you request a factory reset from boot menu, we'll boot twice: first one will set those flags, second one then does the deed like the other case.
Or in other words: we need some userspace to be able to run the pre-reboot works, and if we are still in boot menu we first need to go there.

Note that the first boot doesn't transition into rootfs however, it does its stuff from the initrd, and reboots from there, without transitioning.
So from the PoV of the firmware it's two reboots in total.
From PoV of rootfs userspace it's one.
If you understand what I am trying to say here...

Not sure what you are going on about, but the way the trust chain concept works on modern computers is that you boot up in a trusted state, and then chain everything else from there.
Hence of course, you reboot to reset the state, to get your trust chain into a clean state again?

Note that all of systemd's factory reset work actually runs from the initrd, i.e. under the assumption of a UKI world in a fully vendor signed part of the OS with only minimal input from elsewhere.

Sure, if you can afford to dump all hardware on the trash and never use them again, if you have the suspicion that they got compromised, knock yourself out.
Not cool for the environment, kinda wasteful, but whatever.

I am pretty sure most people outside your bubble probably prefer a reasonable mechanism to maybe not waste all those resources, and get a clear and reasonably secure way to get the systems back to work.

Oh, hey, you are describing exactly what systemd is providing you with now.

It's the systemd embedded in the UKI, i.e. fully signed by the OS vendor, immutable, not modifiable by an attacker, without network access and so on.

I mean, sure you can decide not to trust SecureBoot and stuff at all, sure.
But if you are at that level of paranoia, then you cannot trust computers at all, and might as well become a sheep farmer?

Also, it's actually mostly fine to boot from a compromised disk as long as every resource involved is properly authenticated.
Of course, the less you boot the better, but again when resetting the disks like this we do this from the initrd, i.e. from the signed, vendor-supplied UKI in a short-lived environment, not from the rootfs that might be user (and thus attacker) controlled.

But I think ultimately we can just agree to disagree on the security model, no?

We are dumping the *state* on the trash.
But a signed UKI isn't precisely "state".
It's firmware-authenticated immutable vendor code.

But dunno, I think we should end this here.
You have your security model, I have mine, let's just agree to disagree on it.

Sure if you make your UKI signing keys accessible to an attacker then of course there's no way to recover.
Maybe don't do that then...

If you compile your own kernels you are your own OS vendor.
In that case you better take care of your signing keys.

But this is not how most Linux distros or big installs are set up: they run kernels put together and signed on build systems, and those are distinct from the systems they are run on, and the signing keys are not available there.

---

> **[@agowa338](https://chaos.social/@agowa338):** [Discussion about EFI vars and security concerns]

Well, the idea is not to erase all EFI vars... just the OS-owned subset.
The way I envision this is to work is to primarily rely on the namespace of EFI vars (you know, that UUID that indicates ownership of the EFI var) to filter which ones to keep and which ones to erase.

Hmm?
The logic is supposed to reset stuff relevant to *our* OS, i.e. the OS we actually want to reset.
Some Windows EFI var does *not* belong to that set, and is clearly recognizable as that, precisely because it uses a different namespace UUID.

Frankly, to a large degree that's cargo culted paranoia I am sure.
At this point various components of the boot set and delete EFI vars they own already (shim, sd-boot, systemd otherwise), and the reports that this bricked computers have not really happened.

You think I am not sitting at the firehose of systemd + core OS bug reports already?
But you are or what?

You think I haven't been touching this topic since a long time already?

---

> **[@sstagnaro](https://mastodon.uno/@sstagnaro):** [Question about factory reset proposal]

I love it, of course.
It's the exact right thing to do, and if Debian implements that, more power to them!

---

[systemd-repart]: https://www.freedesktop.org/software/systemd/man/258/systemd-repart.html
[systemctl]: https://www.freedesktop.org/software/systemd/man/258/systemctl.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114635221853062454) (2025-06-06)
