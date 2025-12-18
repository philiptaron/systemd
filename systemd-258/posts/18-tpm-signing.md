---
layout: post
title: "TPM policy signing"
date: 2025-06-17
---

18 Here's the 18th post highlighting key new features of the upcoming v258 release of systemd.

When building a modern, secure, properly protected OS image, there are a number of cryptographic signatures you need to attach to various resources. A brief list:

1. You want to SecureBoot sign your UKI
2. You want to PKCS#7 sign the TPM policy that matches your UKI so that you can unlock your FDE with only your UKIs
3. You want to PKCS#7 sign the Verity root hash of your file system
4. You want to PKCS#7 sign (or maybe OpenPGP sign) the OS artifacts for download
5. You want to sign your IPE security policy file (if you deploy IPE)

If you build your test images locally, this is all somewhat easy: you can just have those 5 keys locally on disk, and `mkosi` will generally do the right thing for you and sign all this with them, as needed without this being painful.

But once you leave the sunny realms of your local development machine and try to build something deployable, you need to think about signing things properly, i.e. on proper build systems in a reasonably secure way.

And that usually means hw backed signing, and in particular "offline" signing—i.e., you no longer just run the signing tool from your build script, but you just prep a request, submit it somewhere. Then you wait, typically even terminate your build for now. And then eventually you get the signature for your artifact back, and restart things again, now being able to combine your build artifacts with the freshly acquired signature, and glueing it all together.

With systemd v258 there's now a lot of support for doing all this in `systemd-sbsign` (which can do SecureBoot signing), `systemd-measure` (which does the PCR signing), and `systemd-repart` (which can do the Verity signing).

And of course `mkosi` already supports all that too (I mean, the features in systemd were put together precisely to make `mkosi` be able to handle this, `mkosi` was the driver here).

Net effect: OpenSUSE build system (OBS) natively supports building `mkosi` images already, and will properly offline sign all these artifacts.

(In case you're wondering, OBS supports opengpg signing build artifacts anyway, so number 4 of the list above is already dealt with too. Number 5 in the list is being worked on already).

What's the ultimate goal with all this? The goal is to make it easy to build modern, secure disk images easily: just fork the particleos git repo, build it on OBS and there you go, you have a robust, self-updating, properly signed operating system that checks all the boxes.

---

## Q&A

> **@alwayscurious** Can you use the TPM to protect against downgrade attacks, so that if the machine is booted with an older kernel, the keys are inaccessible?

`systemd-pcrlock` is robust against downgrade attacks. It generates policies that only cover allowlisted releases and invalidates old ones.

---

[systemd-sbsign]: https://www.freedesktop.org/software/systemd/man/258/systemd-sbsign.html
[systemd-measure]: https://www.freedesktop.org/software/systemd/man/258/systemd-measure.html
[systemd-repart]: https://www.freedesktop.org/software/systemd/man/258/systemd-repart.html
[mkosi]: https://mkosi.systemd.dev/
[systemd-pcrlock]: https://www.freedesktop.org/software/systemd/man/258/systemd-pcrlock.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114697642092211474) (2025-06-17)
