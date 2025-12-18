---
layout: post
title: "systemctl start verbose"
date: 2025-05-21
---

It's that time again!
The systemd v258 release is coming closer.
Let's restart the "what's new" series of posts for this iteration!
Hence:

1. Here's the 1st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

As most of you probably know, `systemctl start` is how you manually start a systemd unit.
Starting a unit can fail, and systemd tracks that for you and tells you this.
When you encounter such a failure, the next thing you'd typically do is check the logs for the unit, i.e. run `journalctl -u …` on the unit.

With v258, there's now a combined way to do this.
If you add the `-v` switch to your `systemctl start` invocation, verbose mode will be invoked, which means the logs will be displayed "live", covering the time span when the start operation is started until the start operation completed.

This has been a much-requested feature – I figure some of you probably even looked for this feature personally already.

Thus you might ask: why did it take so long to actually implement this?
Well, simply because it's really hard to implement, much harder than it might sound on the surface at first.

In order to make the logic work correctly, we need to ensure two things: first, the live log output must be fully established by the time the start operation is enqueued.
That's relatively easy to make sure.
But the other thing is that we must continue the log output until the start operation completed, and all log messages queued at that point are fully processed and shown.
And only once that part is complete, `systemctl start -v` may exit.

And the last part is the nasty bit: ensuring that all log messages enqueued at the moment the start operation completed are fully processed before we stop the log output.
That's because journald takes log streams from a multitude of sources: classic syslog AF_UNIX, modern systemd AF_UNIX, stdout/stderr stream sockets, kernel kmsg and more.

And for each of these inputs, journald needs to track synchronization requests so that we can properly report when all pending log messages up to a certain point are processed, but not more.
And that's a bit messy, since each of these mechanisms have very different properties and functionalities.

For example, for AF_UNIX datagram sockets, we can track the realtime timestamp of incoming messages, and wait until we processed all messages with a timestamp older than the service start completion.

For AF_UNIX stream sockets, on the other hand, we don't have that.
But we can track the number of pending readable bytes in the sockets at the moment that the service start completed, and process that many more bytes before being done with the logging.

But then there's also AF_UNIX stream sockets that have just connected but have not been accepted yet.
Turns out we can get statistics about that too via the obscure "sockdiag" Linux netlink protocol.
For kernel kmsg, we have CLOCK_BOOTTIME timestamps, which we can use similar to the AF_UNIX datagram timestamps.

So yikes, to properly synchronize on log processing, we need 4 completely different mechanisms, and we have a lot of sockets to listen on.
Uff!

But anyway, it's implemented now, and it works.
Enjoy your new `systemctl start -v`!

---

> **[@tfld](https://tyrol.social/@tfld):** That's a nice QOL improvement. Is there an environment variable for it or any other way to make this behaviour the default (without recompiling)?

In the shell: `alias systemctl="systemctl -v"`

---

[systemctl]: https://www.freedesktop.org/software/systemd/man/258/systemctl.html
[journalctl]: https://www.freedesktop.org/software/systemd/man/258/journalctl.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114545892813068498) (2025-05-21)
