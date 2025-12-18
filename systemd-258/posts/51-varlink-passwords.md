---
layout: post
title: "Varlink password agent interface"
date: 2025-09-03
---

For a long time systemd has supported the "ask-password" protocol that allows system components (i.e. non-interactive, low-level stuff) to query passwords and other secrets interactively, during boot and runtime. The original usecase was disk encryption: early during boot, in the initrd, we must query the user for a disk unlock passphrase, and only then can transition into the encrypted root file system.

This protocol never relied on D-Bus, because D-Bus is a late boot thing, and not really usable for early boot stuff. The protocol is documented at [systemd.io/PASSWORD_AGENTS/](https://systemd.io/PASSWORD_AGENTS/), and is basically unmodified since day 1.

The protocol is quite unlike most APIs: a request is not made via IPC or so, but by dropping a short-lived file into some directory. Implementing this properly requires some care to be taken, as such files need to be created atomically and be properly lifecycled.

With v257 support for this protocol was extended to per-user services too: services that run under the logged-in user's identity can now also query passwords, the same way.

With v258 we take the concept one step further: there's now a Varlink API to request a password. Simply call the `io.systemd.AskPassword.Ask` method on the `/run/systemd/io.systemd.AskPassword` socket and there you go. Or in other words: the protocol can be used in a less special way now, it's now simply an IPC call like any other, and we made a bit more progress towards Varlinkifying the world.

The per-user and per-system password agent services use different entrypoint sockets:

- Per-system socket: `/run/systemd/io.systemd.AskPassword`
- Per-user socket: `$XDG_RUNTIME_DIR/systemd/io.systemd.AskPassword`

The protocol spoken on both is the same, you just end up with password prompts directed to different sets of people: if you talk to the system one, any user and the boot time UI will get the request. If you talk to the user one, only that user.

Note that agents still need to implement the old file-based API, while clients can use varlink. The old protocol remains the underlying infrastructure. The varlink service has some benefits though, since it is hooked up with polkit, so you could even ask for passwords from a state where you already dropped various privileges.

Additionally, `run0` also starts a TTY password agent during initialization and stops it once the session is fully up, if you specify `--pty-late`.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115139611674941889) (2025-09-03)
