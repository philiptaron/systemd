---
layout: post
title: "TPM and verified boot"
date: 2025-11-28
---

9️⃣ Here's the 9th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

Over the past months and years, systemd as acquired a number of features in the verified boot/TPM area.
Verified boot means basically that in cooperation with a TPM a secure log is kept of what happens during runtime and in particular during boot, specifically that every component takes a hash value of the next component it starts (this is called "measuring").

This log is kept secure by means of so called PCRs, which are special registers in the TPM that the CPU can write hash values of components to, but which cannot be reset (unless the system is reset as a whole).
Each time a hash value is written, the current value of the PCR is hashed together with the passed hash value, and the result becomes the new PCR value.

TPMs typically have 24 PCRs, of which 8 are for the OS to use (the rest are "owned" by the firmware or have special semantics).

In theory a single PCR would suffice to protect the whole log, but by using separate PCRs one has the benefit that PCRs become predictable: if you know which components are involved in the boot you can predict what the value of the PCR is after boot.

On Linux, the 8 PCRs are generally used according to the registry maintained in the UAPI.7 document:

https://uapi-group.org/specifications/specs/linux_tpm_pcr_registry/

As you might see on that page various of the PCRs have multiple uses these days, objects of unrelated semantics end up in the same PCRs, and that's simply because there are so few of them.

With systemd v259 we are doing something about that.
As it turns out, the TPM 2.0 spec actually has kinda addressed the scarcity of PCRs, but so far noone bothered to actually make use of that.

One can define additional objects in the TPM nowadays that behave like PCRs, but are implemented by "nvindexes", which is how TPM names little persistent memory registers it offers applications to allocate and store very short data in.

With v259, the [`systemd-tpm2-setup.service`][systemd-tpm2-setup] early boot service can now allocate additional PCRs this way.
We call them "NvPCRs" (which is a very confusing name, because "nv" stands for "non-volatile", but of course PCRs are very much volatile, they reset to zero on each boot; but TPM gods named the backing concepts nvindexes even with these semantics, and this naming spills into our naming).

Setting up NvPCRs is not entirely trivial: nvindexes (unlike classic PCRs) can basically be removed by anyone with sufficient access to the TPM, and be recreated, at which point they can be reset.
But resetting during runtime is precisely what should not be possible with them.
Our way out: we maintain a secret on disk that is measured as first value into the NvPCRs.
The secret itself is locked to the TPM and thus only components with access to the secret can reset the NvPCR.

(The whole story is a bit more complicated than this, and yes I know we could also create "non-deletable" nvindexes, but we don't really want to do that, because ownership of that is kinda problematic in a world where we expect multi-boot scenarios – which means we are just *one* user of the TPM, some other OS might own it too).

With v259 the new NvPCRs are used to measure two new things: we measure the SMBIOS/Devicetree product UUID, and we measure the cryptsetup unlock mechanism used.
We soon want to extend that, and for example measure the root hash + sig of every single DDI activated on the system.
With that we have a pretty complete trail of everything going on on the system.

NvPCR measurements will show up in [`systemd-pcrlock`][systemd-pcrlock] `cel` now, btw.

And that's all for now.

---

> **[@raito](https://nixos.paris/@raito)** Do you know how many nvpcrs can we expect to use on a normal system in addition to those that systemd are going to produce?

Well, the pc profile says there should be 76 nvindexes allocatable.
But it's not entirely clear how many of those shall be accessible in nvextend mode, and if you store very large data in other nvindexes then there might not be enough data for the nvpcrs anymore.
That said, nvpcrs require no data storage, just metadata storage (since they reset to 0 on boot), and thus they should be very space efficient...

But the honest answer is, we need to be frugal still, we'll have to see how this all collides with reality.

> **[@tfld](https://tyrol.social/@tfld)** Oof, that table is unreadable in dark mode.
> I added a PR to fix that

Thank you, already got merged!

---

## References

[systemd-tpm2-setup]: https://www.freedesktop.org/software/systemd/man/259/systemd-tpm2-setup.html
[systemd-pcrlock]: https://www.freedesktop.org/software/systemd/man/259/systemd-pcrlock.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115627835871078915) (2025-11-28)
