---
layout: post
title: "Factory reset support"
date: 2025-06-06
---

A fundamental aspect of OS security must be a secure way to return the OS into a well-defined, secure state if a compromise has been identified.

Fending off an attacker is one thing, accepting that it might happen anyway and that you can recover from that in a reasonable way is another. And that's the case not only if you think about "cattle" style installs (i.e., lots of similar systems running the same OS image), but equally on "pet" style installs (i.e., your personal device).

Or to turn this around, a system that doesn't come with a clean, well defined mechanism to reset it fully, erase all unauthenticated data and return it to a vendor image without any local modifications, is highly problematic I believe.

Now you might say: "I can always reinstall my Linux" and start from scratch. And to some point you are right even. But only to some point. First of all "reinstalling your Linux" is not precisely a trivial operation, and secondly, in today's world it's actually not really going to suffice in many ways. That's because it's not sufficient to erase your HDD and reinitialize it. There's more state to reset. One of them in particular is the TPM: local key material is derived from or protected by a "seed" key stored on the TPM.

If you do not invalidate the old seed key and generate a new one, then all secrets associated with the compromised install (and thus tainted) will remain valid.

And there's more: there are various bits stored in EFI vars NVRAM that need to be reset too (shim keys, for example).

`systemd` for a longer time has had really nice support for resetting your HDD (i.e., securely erase partitions via the `systemd-repart` `FactoryReset=` knob) if a factory reset is requested.

With v258 we considerably extended this work. There's now a well defined way to extend the factory reset logic so that other subsystems can be reset too. And we do ship one plugin for that (which is enabled by default), that requests a TPM reset from the firmware.

If your OS is properly set up for that you can now issue `systemctl start factory-reset.target`. This will initiate a reboot, but a special one, where first the firmware will reset the TPM, and then the OS will reset its own state.

And once the system comes back again the system is fully reset.

This currently does not cover EFI var NVRAM reset natively, but there's a clean plugin interface now to do that eventually (two actually: one place where you can plug in such code *before* we reboot, and one place *after* we reboot). I'd expect that in one of the next releases we'll add another plugin for this, that erases certain EFI vars in NVRAM.

There's also now a Varlink based API to query the current factory reset state (i.e., is a factory reset pending for the next reboot, or are we currently executing one for the current boot, or did we already finish one for the current boot, or is none pending nor executing).

If you want to learn more about the factory reset concepts in systemd, there is a new document for this: [systemd/docs/FACTORY_RESET.md](https://github.com/systemd/systemd/blob/main/docs/FACTORY_RESET.md)

Oh, and of course: our ParticleOS images have been updated to expose this kind of thorough factory reset that covers the TPM already. You can simply select "factory reset" in the boot menu, and all non-authenticated data is gone.

And finally: if you run an OS in production and it has no clear story for factory reset, maybe talk to your vendor, and ask them to get back to the drawing board, and fix their mess.

---

> **[@anselmschueler](https://ieji.de/@anselmschueler)** [Question about password requirements for factory reset]

Which password?

It's supposed to be a mechanism to get a working systemd back if you forgot your disk encryption passwords, so that the system is not bricked for good, you know.

It's the same as it is for your Android phone for example, where you can do a factory reset from the boot menu too – without authentication.

So no, we do not ask for authentication: if you managed to get this kind of access to the boot menu to be able to select it, you are god anyway.

> **[@agowa338](https://chaos.social/@agowa338)** [Question about EFI variable erasure]

The idea is not to erase all EFI vars, just the OS-owned subset. The way I envision this to work is to primarily rely on the namespace of EFI vars (you know, that UUID that indicates ownership of the EFI var) to filter which ones to keep and which ones to erase.

> **[@agowa338](https://chaos.social/@agowa338)** [Follow-up about EFI variables]

Hmm? The logic is supposed to reset stuff relevant to *our* OS, i.e., the OS we actually want to reset. Some Windows EFI var does *not* belong to that set, and is clearly recognizable as that, precisely because it uses a different namespace UUID.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114635221853062454) (2025-06-06)
