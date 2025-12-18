---
layout: post
title: "RestartMode=debug for debug logging"
date: 2025-08-21
---

43: Here's the 43rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Back in v257 we added support for `RestartMode=debug`: if used and a service is automatically restarted due to `Restart=` a special environment variable `DEBUG_INVOCATION=1` is set for the new invocation. This is then supposed to enable special logic in the service code that generates additional debug logging and other behaviour.

What precisely `DEBUG_INVOCATION=1` will trigger in the service code is really up to the programmer of the service itself, and can vary wildly.

In systemd v257 the programmers of systemd's own services decided — to not honour it at all. That of course is quite a missed opportunity, given that we really should showcase our own service/service manager protocol features.

Hence with v258 this is fixed. All of systemd's own services will now automatically enable debug logging — if started with `DEBUG_INVOCATION=1` set, and thus, if you turn on `Restart=` + `RestartMode=debug` for any of them, something reasonable will happen: the initial activation is a regular one, but on automatic restart debug logging will be generated.

And I forgot to mention GLib's logging infra is already doing this too, and in fact beat us to it: https://docs.gtk.org/glib/logging.html#debug-message-output

I really hope to see similar logic added to the logging infra of the various programs and frameworks sooner or later!

---

## Q&A

> **[Fluchtkapsel](https://nerdculture.de/@fluchtkapsel)** Will this be triggered by `systemctl restart …` or when a service gets restarted automatically?

Only when restarted automatically.

> **[Ruben Vermeersch](https://social.rocketeer.be/@ruben)** =restart or =debug?

just a quick test to verify you all are paying attention ;-)

(Fixed now, thanks!)

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115064971230187209) (2025-08-21)
