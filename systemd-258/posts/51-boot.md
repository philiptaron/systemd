---
layout: post
title: "systemd 258 Feature Highlight #51"
date: 2025-09-03
source: https://mastodon.social/@pid_eins/115139611674941889
author: Lennart Poettering
---

5️⃣1️⃣ Here's the 51st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

For a long time systemd has supported the "ask-password" protocol that allows system components (i.e. non-interactive, low-level stuff) to query passwords and other secrets interactively, during boot and runtime. The original usecase was disk encryption: early during boot, in the initrd, we must query the user for a disk unlock passphrase, and only then can transition into the…

## Thread Continuation

*2025-09-03* ([source](https://mastodon.social/@pid_eins/115139643341683157))

…lifecycled.

With v257 support for this protocol was extended to per-user services too: services that run under the logged-in user's identity can now also query passwords, the same way.

With v258 we take the concept one step further: there's now a Varlink API to request a password: simply call the io.systemd.AskPassword.Ask method on the /run/systemd/io.systemd.AskPassword socket and there you go.

*2025-09-03* ([source](https://mastodon.social/@pid_eins/115139644536400257))

Or in other words: the protocol can be used in a less special way now, it's now a simply IPC call like any other, and we made a bit more progress towards Varlinkifying the world.

*2025-09-03* ([source](https://mastodon.social/@pid_eins/115139776239926015))

[@Mae](https://is.badat.dev/users/Mae) yeah, agents need to implement the old api. clients can use varlink.

*2025-09-03* ([source](https://mastodon.social/@pid_eins/115139924788623842))

[@dazo](https://infosec.exchange/@dazo) [@Mae](https://is.badat.dev/users/Mae) nah, the old stuff remains the protocol underneath all. No need to change anything.

But then again, the varlink service has some benefits, since it is hooked up with polkit, so you could even ask for pws from a state where you already dropped various privs.

*2025-09-04* ([source](https://mastodon.social/@pid_eins/115148038159288275))

[@eichehome](https://social.anoxinon.de/@eichehome) both

*2025-09-05* ([source](https://mastodon.social/@pid_eins/115152246912027532))

[@eichehome](https://social.anoxinon.de/@eichehome) the per-user askpw stuff and the per-system askpw stuff use a different entrypoint socket.

the askpw per-system socket is /run/systemd/io.systemd.AskPassword

the askpw per-user socket is $XDG_RUNTIME_DIR/systemd/io.systemd.AskPassword.

The protocol spoken on both is the same, you just end up with pw prompts direct to different sets of people: if you talk to the system one, any user and the boot time UI will get the request. if you tlak to the user one, only that user.

*2025-09-05* ([source](https://mastodon.social/@pid_eins/115152263565459275))

[@grimmauld](https://mastodon.grimmauld.de/@grimmauld) run0 also starts a tty pw agent during initialization and stops it once the session is fully up, if you specify --pty-late.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115139626628094278):** …encrypted root file system. This protocol never relied on D-Bus, because D-Bus is a late boot thing, and not really usable for early boot stuff. The protocol is documented here, and is basically unmodified since day 1:

<https://systemd.io/PASSWORD_AGENTS/>

As you might see it's quite unlike most APIs: a request is not made via IPC or so, but by dropping a short-lived file into some dir. Implementing this properly requires some care to be taken, as such files need to be created atomically and be properly…

…lifecycled.

With v257 support for this protocol was extended to per-user services too: services that run under the logged-in user's identity can now also query passwords, the same way.

With v258 we take the concept one step further: there's now a Varlink API to request a password: simply call the io.systemd.AskPassword.Ask method on the /run/systemd/io.systemd.AskPassword socket and there you go.

## Sources

- [Original post](https://mastodon.social/@pid_eins/115139611674941889)
- [Thread continuation](https://mastodon.social/@pid_eins/115139643341683157)
- [Thread continuation](https://mastodon.social/@pid_eins/115139644536400257)
- [Thread continuation](https://mastodon.social/@pid_eins/115139776239926015)
- [Thread continuation](https://mastodon.social/@pid_eins/115139924788623842)
- [Thread continuation](https://mastodon.social/@pid_eins/115148038159288275)
- [Thread continuation](https://mastodon.social/@pid_eins/115152246912027532)
- [Thread continuation](https://mastodon.social/@pid_eins/115152263565459275)
