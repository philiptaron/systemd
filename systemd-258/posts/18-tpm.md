---
layout: post
title: "systemd 258 Feature Highlight #18"
date: 2025-06-17
source: https://mastodon.social/@pid_eins/114697642092211474
author: Lennart Poettering
---

1️⃣8️⃣ Here's the 18th  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

When building a modern, secure, properly protected OS image, there are a number of cryptographic signatures you need to attach to various resources. A brief list:

1. You want to SecureBoot sign your UKI
2. You want to PKCS#7 sign the TPM policy that matches your UKI so that you can unlock your FDE with only your UKIs

## Thread Continuation

*2025-06-17* ([source](https://mastodon.social/@pid_eins/114697673514808991))

(btw, the fact that "mkosi" can prep and sign all this stuff for you is one of the main reasons why you really should use it)

But once you leave the sunny realms of your local development machine and try to build something deployable, you need to think about signing things properly, i.e. on proper build systems in a reasonably secure way. 

And that usually means hw backed signing, and in particular "offline" signing. i.e. you no longer just run the signing tool from your build script, …

*2025-06-17* ([source](https://mastodon.social/@pid_eins/114697681878353597))

… but you just prep a request, submit it somewhere. Then you wait, typically even terminate your build for now. And then eventually you get the signature for your artifact back, and restart things again, now being able to combine your build artifacts with the freshly acquired signature, and glueing it all together.

With systemd v258 there's now a lot of support for doing all this, in systemd-sbsign (which can do SecureBoot signing), in systemd-measure (which does the PCR signing), …

*2025-06-17* ([source](https://mastodon.social/@pid_eins/114697693907158528))

… and in systemd-repart (which can do the Verity signing).

And of course mkosi already supports all that too (I mean, the features in systemd were put together precisely to make mkosi be able to handle this, mkosi was the driver here).

Net effect: OpenSUSE build system (OBS) natively supports building mkosi images already, and will properly offline sign all these artifacts.

*2025-06-17* ([source](https://mastodon.social/@pid_eins/114697702290914951))

(in case you wonder, OBS supports opengpg signing build artifacts anyway, so number 4 of the list above is already dealt with too. Number 5 in the list is being worked on already).

What's the ultimate goal with all this? The goal is to make it easy to build modern, secure disk images easily: just fork the particleos git repo, build it on OBS and there you go, you have a robust, self-updating, properly signed operating system that checks all the boxes.

*2025-06-17* ([source](https://mastodon.social/@pid_eins/114698591530255485))

[@th](https://social.v.st/@th) interesting. we strive to be bit-wise reproducible, but I am not sure the stuff built on OBS actually is. 

The signing itself is done deeply inside of OBS though, not in our code, so not sure this could be adapted from our side.

(though very confusing that there's also this thing: <https://docs.sigstore.dev/cosign/> by the same name doing something quite different.)

*2025-06-17* ([source](https://mastodon.social/@pid_eins/114699731644520977))

[@darix](https://mastodon.social/@darix) [@bluca](https://fosstodon.org/@bluca) [@johanneskastl](https://digitalcourage.social/@johanneskastl) mkosi can build opensuse images just fine, but so far for particleos noone volunteered to get put things together for that. If you are interested, send a PR, and gte involved.

*2025-07-10* ([source](https://mastodon.social/@pid_eins/114827938384464559))

[@alwayscurious](https://infosec.exchange/@alwayscurious) systemd-pcrlock is robust against downgrade attacks. It generates policies that only cover allowlisted releases and invalidates old policies.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114697657659230872):** 3. You want to PKCS#7 sign the Verity root hash of your file system
4. You want to PKCS#7 sign (or maybe OpenPGP sign) the OS artifacts for download
5. You want to sign your IPE security policy file (if you deploy IPE)

If you build your test images locally, this is all somewhat easy: you can just have those 5 keys locally on disk, and "mkosi" will generally do the right thing for you and sign all this with them, as needed without this being painful.

(btw, the fact that "mkosi" can prep and sign all this stuff for you is one of the main reasons why you really should use it)

But once you leave the sunny realms of your local development machine and try to build something deployable, you need to think about signing things properly, i.e. on proper build systems in a reasonably secure way. 

And that usually means hw backed signing, and in particular "offline" signing. i.e. you no longer just run the signing tool from your build script, …

> **[@alwayscurious@infosec.exchange](https://infosec.exchange/@alwayscurious/114827916412021776):** [@pid_eins](https://mastodon.social/@pid_eins) Can you use the TPM to protect against downgrade attacks, so that if the machine is booted with an older kernel, the keys are inaccessible?

[@alwayscurious](https://infosec.exchange/@alwayscurious) systemd-pcrlock is robust against downgrade attacks. It generates policies that only cover allowlisted releases and invalidates old policies.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114697642092211474)
- [Thread continuation](https://mastodon.social/@pid_eins/114697673514808991)
- [Thread continuation](https://mastodon.social/@pid_eins/114697681878353597)
- [Thread continuation](https://mastodon.social/@pid_eins/114697693907158528)
- [Thread continuation](https://mastodon.social/@pid_eins/114697702290914951)
- [Thread continuation](https://mastodon.social/@pid_eins/114698591530255485)
- [Thread continuation](https://mastodon.social/@pid_eins/114699731644520977)
- [Thread continuation](https://mastodon.social/@pid_eins/114827938384464559)
