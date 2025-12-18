---
layout: post
title: "systemd 258 Feature Highlight #1"
date: 2025-05-21
source: https://mastodon.social/@pid_eins/114545892813068498
author: Lennart Poettering
---

It's that time again! The systemd v258 release is coming closer. Let's restart the "what's new" series of posts for this iteration! Hence:

1️⃣ Here's the 1st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

As most of you probably know "systemctl start" is how you manually start a systemd unit. Starting a unit can fail, and systemd tracks that for you and tells you this. When you encounter such a failure the next thing you'd typically do…

## Thread Continuation

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114545915445888097))

Thus you might ask: why did it take so long to actually implement this? Well, simply because it's really hard to to implement, much harder than it might sound on the surface at first:

in order to make the logic work correctly we need to ensure two things: first, the live log output must be fully established by the time the start operation is enqueued. That's relatively easy to make sure. But the other thing is that we must continue the log output until the the start operation completed…

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114545923974315004))

…and all log messages queued at that point are fully processed and shown. And only once that part is complete, systemctl start -v may exit.

And the last part is the nasty bit: ensuring that all log messages enqueued at the moment the start operation completed are fully processed before we stop the log output. That's because journald takes log stream from a multitude of sources: classic syslog AF_UNIX, modern systemd AF_UNIX, stdout/stderr stream sockets, kernel kmsg and more.

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114545932704361864))

And for each of these inputs journald needs to track synchronization requests so that we can properly report when all pending log messages up to a certain point are processed, but not more. And that's a bit messy, since each of these mechanisms have very different properties and functionalities.

For example for AF_UNIX datagram sockets we can track the realtime timestamp of incoming messages, and wait until we processed all messages with a timestamp older than the service start completion.

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114545940037207373))

For AF_UNIX stream sockets otoh we don't have that. But we can track the number of pending readable bytes in the sockets the moment that the service start completed, and process that many more bytes before being done with the logging.

But then there's also AF_UNIX stream sockets that have just connected but have not been accepted yet. Turns out we can get statistics about that too via the obscure "sockdiag" Linux netlink protocol. 

For kernel kmsg we have CLOCK_BOOTTIME timestamps, …

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114545944769966876))

… which we can use similar to the AF_UNIX datagram timestamps.

So yikes, to properly synchronize on log processing, we need 4 different completel different mechanisms, and we have a lot of sockets to listen on. Uff!

But anyway, it's implemented now, and it works. 

Enjoy your new "systemctl start -v"!

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114546416316448207))

[@mxey](https://hachyderm.io/@mxey) yes, it does.

*2025-05-21* ([source](https://mastodon.social/@pid_eins/114546821175381459))

[@tfld](https://tyrol.social/@tfld) in the shell: alias systemctl="systemctl -v"

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550399080635580))

[@mike](https://social.chinwag.org/@mike) yeah, should just work.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114545904768094738):** …is check the logs for the unit, i.e. run "journalctl -u …" on the unit. 

With v258 there's now a combined way to do this. If you add the -v switch to your "systemctl start" invocation, "verbose" mode will be invoked, which means the logs will displayed "live" covering the time span when the start operation is started until the start operation completed. 

This has been a much requested feature – I figure some of you probably even looked for this feature personally already.

Thus you might ask: why did it take so long to actually implement this? Well, simply because it's really hard to to implement, much harder than it might sound on the surface at first:

in order to make the logic work correctly we need to ensure two things: first, the live log output must be fully established by the time the start operation is enqueued. That's relatively easy to make sure. But the other thing is that we must continue the log output until the the start operation completed…

> **[@tfld@tyrol.social](https://tyrol.social/@tfld/114546722096101653):** [@pid_eins](https://mastodon.social/@pid_eins) That's a nice QOL improvement. Is there an environment variable for it or any other way to make this behaviour the default (without recompiling)?

Also I'm very happy to see this series returning, I really like it!

[@tfld](https://tyrol.social/@tfld) in the shell: alias systemctl="systemctl -v"

## Sources

- [Original post](https://mastodon.social/@pid_eins/114545892813068498)
- [Thread continuation](https://mastodon.social/@pid_eins/114545915445888097)
- [Thread continuation](https://mastodon.social/@pid_eins/114545923974315004)
- [Thread continuation](https://mastodon.social/@pid_eins/114545932704361864)
- [Thread continuation](https://mastodon.social/@pid_eins/114545940037207373)
- [Thread continuation](https://mastodon.social/@pid_eins/114545944769966876)
- [Thread continuation](https://mastodon.social/@pid_eins/114546416316448207)
- [Thread continuation](https://mastodon.social/@pid_eins/114546821175381459)
- [Thread continuation](https://mastodon.social/@pid_eins/114550399080635580)
