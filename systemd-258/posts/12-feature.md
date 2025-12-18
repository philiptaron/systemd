---
layout: post
title: "systemd 258 Feature Highlight #12"
date: 2025-06-06
source: https://mastodon.social/@pid_eins/114635221853062454
author: Lennart Poettering
---

1️⃣2️⃣ Here's the 12th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

I believe a fundamental aspect of OS security must be a secure way to return the OS into a well-defined, secure state if a compromise has been identified.

Fending of an attacker is one thing, accepting that it might happen anyway and that you can recover from that in a reasonable way is another. And that's the case not only if you think about "cattle" style installs…

## Thread Continuation

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635250959425696))

But only to some point. First of all "reinstalling your Linux" is not precisely a trivial operation, and secondly, in today's world it's actually not really going to suffice in many ways. That's because it's not sufficient to erase your HDD an reinitialize it. There's more state to reset. One of them in particular is the TPM: local key material is derived from or protected by a "seed" key stored on the TPM.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635263631055943))

If you do not invalidate the old seed key and generate a new one, then all secrets associated with the compromised install (and thus tainted) will remain valid. 

And there's more: there are various bits stored in EFI vars NVRAM that need to be reset too (shim keys for example).

systemd for a longer time has had really nice support for resetting your HDD (i.e. securely erase partitions, via the systemd-repart FactoryReset= knob) if a factory reset is requested.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635274347342778))

With v258 we considerably extended this work.There's now a well defined way to extend the factory reset logic so that other subsystems can be reset too. And we do ship one plugin for that (which is enabled by default), that requests a TPM reset from the firmware. 

If your OS is properly set up for that you can now issue "systemctl start factory-reset.target". This will initiate a reboot, but a special one, where first the firmware will reset the TPM, and then the OS will reset its own state.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635293633761868))

And once the system comes back again the system is fully reset.

This currently does not cover EFI var NVRAM reset natively, but there's a clean plugin interface now to do that eventually (two actually: one place where you can plug in such code *before* we reboot, and one place *after* we reboot). [I'd expect that in one of the next releases we'll add another plugin for this, that erases certain EFI vars in NVRAM].

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635302621904693))

There's also now a Varlink based API to query the current factory reset state (i.e. is a factory reset pending for the next reboot, or are we currently executing one for the current boot, or did we already finish one for the current boot, or is none pending nor executing).

If you want to learn more about the factory reset concepts in systemd, there is a new document for this:

<https://github.com/systemd/systemd/blob/main/docs/FACTORY_RESET.md>

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635306779651946))

Oh, and of course: our ParticleOS images have been been updated to expose this kind of thorough factory reset that covers the TPM already. You can simply select "factory reset" in the boot menu, and all non-authenticated data is gone.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635330672967319))

And finally: if you run an OS in production and it has no clear story for factory reset, maybe talk to your vendor, and ask them to get back to the drawing board, and fix their mess.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635356705181936))

[@anselmschueler](https://ieji.de/@anselmschueler) which password?

It's supposed to be a mechanism to get a working systemd back if you forgot your disk encryption passwords, so that the system is not bricked for good, you know.

It's the same as it is for your android phone for example, where you can do a factory reset from the boot menu too – without authentication.

So no, we do not ask for authentication: if you managed to get this kind of access to the boot menu to be able to select it, you are god anyway.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635381540220436))

[@siosm](https://floss.social/@siosm) you definitely need to reboot, to get back into an unbroken chain of trust. Now you have two ways to ensure this works. First of all you physically request the reset early during boot. That's why we have this in the boot menu. Or you ask for the reset from the compromised running system, and then use some form of attestation to validate that the reboot was genuine. The latter is stuff bigger deployments (i.e. companies which actually do attestation) can do, …

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635389893575905))

[@siosm](https://floss.social/@siosm) … but for the local personal device case ("pet") is indeed not really realistic. At least not right now, hence boot loader reset it is for that case, if your factory reset is about trust. (if your factory reset is not about trust, doing factory reset via UI is of course always fine).

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635404199104625))

[@siosm](https://floss.social/@siosm) if you request a factory reset from a running system a single reboot should suffice: we ask firmware to reset tpm on reboot, set a flag to reset disk on reboot, then reboot. done.

if you request a factory reset from boot menu, we'll boot twice: first one will set those flags, second one then does the deed like the other case. or in other words: we need some userspace to be able to run the pre-reboot works, and if we are still in boot menu we first need to go there.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635408665360943))

[@siosm](https://floss.social/@siosm) note that the first boot doesn't transition into rootfs however, it's does its stuff from the initrd, and reboots from there, without transitioning. So from the PoV of the firmware it's two reboots in total. From PoV of rootfs userspace it's one. If you understand what I am trying to say here...

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635418534408244))

[@sstagnaro](https://mastodon.uno/@sstagnaro) [@rfc1036](https://hostux.social/@rfc1036) I love it, of course. It's the exact right thing to do, and if Debian implements that, more power to them!

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635633228055896))

[@agowa338](https://chaos.social/@agowa338) see my comments about this elsewhere in the thread: <https://mastodon.social/@siosm@floss.social/114635361092180697>

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635637900912824))

[@agowa338](https://chaos.social/@agowa338) well, the iea is not erase all efi vars... just the OS-owned subset. the way I envision this is to work is to primarily rely on the namespace of efi vars (you know, that uuid that indicates ownership of the efi var) to filter which ones to keep and which ones to erase.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635650990769540))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) not sure what you are going on about, but the way the trust chain concept works on modern computers is that you boot up in a trusted state, and then chain everything else from there. Hence of course, you reboot to reset the state, to get your trust chain into a clean state again?

Note that all of systemd's factory reset work actually runs from the initrd, i.e. under the assumption of an UKI world in a fully vendor signed part of the OS with only minimal input from elsewhere.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635659995587631))

[@agowa338](https://chaos.social/@agowa338) Hmm? the logic is supposed to reset stuff relevant to *our* OS, i.e. the OS we actually want to reset. Some windows efi var does *not* belong to that set, and is clearly recognizable as that, precisely because it uses a different namespace uuid.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635682533049289))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) sure, if you can afford to dump all hw on the trash and never use them again, if you have the suspicion that they got compromised, knock yourself out. Not cool for the environment, kinda wasteful, but whatever.

I am pretty sure most people outside your bubble probably prefer a reasonable mechanism to maybe not waste all those resources, and get a clear and reasonably secure way to get the systems back to work.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635689619665015))

[@agowa338](https://chaos.social/@agowa338) frankly, to a large degree that's cargo culted paranoia I am sure. At this point various components of the boot set and delete efi vars they own already (shim, sd-boot, systemd otherwise), and the reports that this bricked computers have not really happened.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635702859610652))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) 

also, it's actually mostly fine to boot from a compromised disk as long as every resource involved is properly authenticated. Of course, the less you boot the better, but again when resetting the disks like this we do this from the initrd, i.e. from the signed, vendor-supplied UKI in a short-lived environment, not from the rootfs that might be user (and thus attacker) controlled. 

But I think ultimately we can just agree to disagree on the security model, no?

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635706742936023))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) oh, hey, you are describing exactly what systemd is providing you with now.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635718563271350))

[@agowa338](https://chaos.social/@agowa338) You think I am not sitting at the firehose of systemd + core OS bug reports already? But you are or what?

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635725949636309))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) it's the systemd embedded in the UKI, i.e. fully signed by the OS vendor, immutable, not modifiable by an attacker, without network access and so on.

I mean, sure you can decide not to trust SecureBoot and stuff at all, sure. But if you are at that level of paranoia, then you cannot trust computers at all, and might as well become a sheep farmer?

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635732611323655))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) 

we are dumping the *state* on the trash. But a signed UKI isn't precisely "state". It's firmware-authenticated immutable vendor code.

But dunno, I think we should end this here. You have your security model, I have mine, let's just agree to disagree on it.

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635735017624312))

[@agowa338](https://chaos.social/@agowa338) You think I  haven't been touching this topic since a long time already?

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635772401157406))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) sure if you make your UKI signing keys accessible to an attacker then of course there's no way to recover. Maybe don't do that then...

*2025-06-06* ([source](https://mastodon.social/@pid_eins/114635823363331310))

[@agowa338](https://chaos.social/@agowa338) [@siosm](https://floss.social/@siosm) if you compile your own kernels you are your own OS vendor. In that case you better take care of your signing keys.

But this is not how most Linux distros or big installs are set up: they run kernels put together and signed on build systems, and those are distinct from the systems they are run on, and the signing keys are not available there.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114635234216495259):** … (i.e. lots of similar systems running the same OS image), but equally on "pet" style installs (i.e. your personal device).

Or to turn this around, a system that doesn't come with a clean, well defined mechanism to reset it fully, erase all unauthenticated data and return it to a vendor image without any local modifications, is highly problematic I believe.

Now you might say: "I can always reinstall my Linux" and start from scratch. And to some point you are right even.

But only to some point. First of all "reinstalling your Linux" is not precisely a trivial operation, and secondly, in today's world it's actually not really going to suffice in many ways. That's because it's not sufficient to erase your HDD an reinitialize it. There's more state to reset. One of them in particular is the TPM: local key material is derived from or protected by a "seed" key stored on the TPM.

> **[@sstagnaro@mastodon.uno](https://mastodon.uno/@sstagnaro/114635369057159493):** [@pid_eins](https://mastodon.social/@pid_eins) Hi Lennart, what do you think about [@rfc1036](https://hostux.social/@rfc1036) factory reset proposal?
<https://hostux.social/@rfc1036/113205554708605481>

[@sstagnaro](https://mastodon.uno/@sstagnaro) [@rfc1036](https://hostux.social/@rfc1036) I love it, of course. It's the exact right thing to do, and if Debian implements that, more power to them!

## Sources

- [Original post](https://mastodon.social/@pid_eins/114635221853062454)
- [Thread continuation](https://mastodon.social/@pid_eins/114635250959425696)
- [Thread continuation](https://mastodon.social/@pid_eins/114635263631055943)
- [Thread continuation](https://mastodon.social/@pid_eins/114635274347342778)
- [Thread continuation](https://mastodon.social/@pid_eins/114635293633761868)
- [Thread continuation](https://mastodon.social/@pid_eins/114635302621904693)
- [Thread continuation](https://mastodon.social/@pid_eins/114635306779651946)
- [Thread continuation](https://mastodon.social/@pid_eins/114635330672967319)
- [Thread continuation](https://mastodon.social/@pid_eins/114635356705181936)
- [Thread continuation](https://mastodon.social/@pid_eins/114635381540220436)
- [Thread continuation](https://mastodon.social/@pid_eins/114635389893575905)
- [Thread continuation](https://mastodon.social/@pid_eins/114635404199104625)
- [Thread continuation](https://mastodon.social/@pid_eins/114635408665360943)
- [Thread continuation](https://mastodon.social/@pid_eins/114635418534408244)
- [Thread continuation](https://mastodon.social/@pid_eins/114635633228055896)
- [Thread continuation](https://mastodon.social/@pid_eins/114635637900912824)
- [Thread continuation](https://mastodon.social/@pid_eins/114635650990769540)
- [Thread continuation](https://mastodon.social/@pid_eins/114635659995587631)
- [Thread continuation](https://mastodon.social/@pid_eins/114635682533049289)
- [Thread continuation](https://mastodon.social/@pid_eins/114635689619665015)
- [Thread continuation](https://mastodon.social/@pid_eins/114635702859610652)
- [Thread continuation](https://mastodon.social/@pid_eins/114635706742936023)
- [Thread continuation](https://mastodon.social/@pid_eins/114635718563271350)
- [Thread continuation](https://mastodon.social/@pid_eins/114635725949636309)
- [Thread continuation](https://mastodon.social/@pid_eins/114635732611323655)
- [Thread continuation](https://mastodon.social/@pid_eins/114635735017624312)
- [Thread continuation](https://mastodon.social/@pid_eins/114635772401157406)
- [Thread continuation](https://mastodon.social/@pid_eins/114635823363331310)
