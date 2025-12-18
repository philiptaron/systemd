---
layout: post
title: "systemd 258 Feature Highlight #43"
date: 2025-08-21
source: https://mastodon.social/@pid_eins/115064971230187209
author: Lennart Poettering
---

4️⃣3️⃣ Here's the 43rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Back in v257 we added support for RestartMode=debug: if used and a service is automatically restarted due to Restart= a special environment variable DEBUG_INVOCATION=1 is set for the new invocation. This is then supposed to enable special logic in the service code that generates additional debug logging and other behaviour.

## Thread Continuation

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115064986143951987))

… if started with DEBUG_INVOCATION=1 set, and thus, if you turn on Restart= + RestartMode=debug for any of them, something reasonable will happen: the initial activation is a regular one, but on automatic restart debug logging will be generated.

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065283079112938))

[@ruben](https://social.rocketeer.be/@ruben) just a quick test to verify you all are paying attention ;-)

(Fixed now, thanks!)

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065285590234480))

[@fluchtkapsel](https://nerdculture.de/@fluchtkapsel) only when restarted automatically.

*2025-08-21* ([source](https://mastodon.social/@pid_eins/115065449549174998))

And I forgot to mention GLib's logging infra is already doing this too, and in fact beat us to it:

<https://docs.gtk.org/glib/logging.html#debug-message-output>

I really hope to see similar logic added to the logging infra of the various programs and frameworks sooner or later!

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115064980446752645):** What precisely DEBUG_INVOCATION=1 will trigger in the service code is really up to the programmer of the service itself, and can vary wildly.

In systemd v257 the programmers of systemd's own services decided … to not honour it at all. That of course is quite a missed opportunity, given that we really should showcase our own service/service manager protocol features.

Hence with v258 this is fixed. All of systemd's own services will now automatically enable debug logging …

… if started with DEBUG_INVOCATION=1 set, and thus, if you turn on Restart= + RestartMode=debug for any of them, something reasonable will happen: the initial activation is a regular one, but on automatic restart debug logging will be generated.

## Sources

- [Original post](https://mastodon.social/@pid_eins/115064971230187209)
- [Thread continuation](https://mastodon.social/@pid_eins/115064986143951987)
- [Thread continuation](https://mastodon.social/@pid_eins/115065283079112938)
- [Thread continuation](https://mastodon.social/@pid_eins/115065285590234480)
- [Thread continuation](https://mastodon.social/@pid_eins/115065449549174998)
