---
layout: post
title: "Service ready notification"
date: 2025-06-27
---

2️⃣3️⃣ Here's the 23rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

One key aspect of service management is ready notification, i.e. a mechanism how a service that has started up can tell the service manager when its initialization is complete and when its functionality is available for other programs to access. The service manager uses this information to know when to start depending services, and similar.

Very early in systemd's development we came up with a very simple protocol for this purpose: the `sd_notify()` protocol. The idea is that the service manager binds an `AF_UNIX/SOCK_DGRAM` to an address of its choice, then invokes the service binary with the `$NOTIFY_SOCKET` environment variable pointing to it and then waits for a datagram containing newline separated, environment-block like strings from the service coming in. It looks for the `READY=1` field in it, and authenticates the thing via `SCM_CREDS` (i.e. checks whether it's the expected process sending this) and that's really already it.

The protocol is simple, and quite extensible: nowadays, in addition to `READY=1` a variety of other things can be sent, for example watchdog keep-alive messages, status strings, configuration reload lifecycle messages, file descriptor store logic, and a lot more.

The [`systemd-notify`][systemd-notify] tool has been part of systemd for as long as the `sd_notify()` protocol has existed.

The tool can be used to send compliant messages from shell scripts, so that services can be implemented natively in shell (not that I would recommend doing that…).

`systemd-notify` so far was strictly the *sender* of these messages, and the service manager was the *receiver*. With v258 `systemd-notify` got extended to optionally switch roles: if you specify `--fork` it can fork off a command, and then wait for the command to send the `READY=1` message, at which point it writes the forked off process' PID to stdout and exits.

You might wonder what this is good for? After all in a way, `systemd-notify` becomes a really dumb service manager of its own that way. So why?

Our own usecase for this is mostly our testsuite for systemd. Many of our tests invoke some operation and at the same time watch via D-Bus, or Varlink, or the Journal or some other message stream the progress of said operation, looking for particular outputs.

Classic shell scripts make it easy to fork off processes in the background, and then controlling their lifetime, that's what shell job control is about after all.

What classic shell scripts don't help you with is doing proper ready notification for such bg jobs: when we expect some message in D-Bus, Varlink or the Journal, we need to make sure that the watch for these event sources is properly installed before we initiate the actual operation we want to watch.

Naively forking off `journalctl`, `busctl`, `varlinkctl` won't give you this kind of synchronization. In many test scripts people work around this race by simply trying a couple of times, applying timeouts and so on.

`systemd-notify --fork` is here to improve things on this front. As it turns out since a while `journalctl`, `busctl`, `varlinkctl` will already send out `sd_notify()` `READY=1` messages once they have established their watches. By invoking these tools via `systemd-notify --fork`, we can easily fork off these tools in the bg, but still get the synchronization right, i.e. delay further execution of the shell script until the watches are properly established.

To illustrate this. Naively, one could watch journal output in the bg via:

```sh
journalctl -f &
PID="$!"
# do something that might log here, for example:
logger "knurz"
kill "$PID"
```

This is subject to the aforementioned race: while `journalctl` is forked off in the bg, it might take too long to start up, so that it might miss the "knurz" message being sent.

With the new `systemd-notify --fork` logic we can do this instead:

```sh
PID=$(systemd-notify --fork -- journalctl -f)
logger "knurz"
kill "$PID"
```

This will also fork off `journalctl`, but it will do this taking the ready notification of `journalctl` into account that it will send once it established its watch. Because of that, the "knurz" message will definitely be seen by `journalctl`.

Summary: this removes a major race *and* it's even one line shorter than the previous code. Yay!

Oh, and yes, it would be great if shells would natively support such ready notifications, it's not rocket science after all, and I'd claim it's a pretty common problem when doing concurrent stuff in shell, in particular in test scripts. And the current hacky ways people use to work around this are sometimes hair raising.

And also, let me emphasize: `sd_notify()` is fantastic for services, but the concept is so simple and powerful, that it is also great for any other tool too. i.e. it's not just `journalctl`, `busctl`, `varlinkctl` that benefit from the concept, it's really any tool that can be somewhat long-running and has an initialization phase about whose completion the caller might want to know.

---

> **[@ablu](https://mastodon.social/@ablu)** well sure, but it also does something very different... One spawns a full fledged service in containment and lifecycle tracking, the other just forks a process into the bg...

That's right. The comparison might have been confusing because both concepts achieve a bit of readiness/syncing. But no doubt, they are different. What `systemd-notify` does is much lighter weight.

---

[systemd-notify]: https://www.freedesktop.org/software/systemd/man/258/systemd-notify.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114754518632012480) (2025-06-27)
