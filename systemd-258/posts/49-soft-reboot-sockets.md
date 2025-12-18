---
layout: post
title: "Soft-reboot and sockets"
date: 2025-09-01
---

49 Here's the 49th post highlighting key new features of the upcoming v258 release of systemd.
[#systemd258](https://mastodon.social/tags/systemd258)

One of the key features of systemd from day 1 on is socket activation, i.e. a mechanism where systemd binds sockets on behalf of services, watches them and only activates the services themselves later, possibly only at the moment they are actively used.

This has various benefits, for example reduces ahead of time cost of running a large number of services (which improves boot times).

But one facet of it is particularly nice: it allows (mostly) getting rid of startup ordering dependencies between services: if all sockets are bound in one early step, then services can just talk to any other service they like at any time, and if that other service is not running yet, this will not cause a failure (as it would on systems without socket activation where ordering is not respected) but instead the will cause activation of the service, and – at worst – the client will wait a bit…

…longer for the request to be fulfilled.

systemd's own services are largely socket activated, in particular since we adopted `Varlink` (since Varlink services are built on listener sockets, unlike D-Bus services where both clients and providers of services connect to the central broker, and never listen on sockets on their own) for many of our services. And all those socket units typically don't carry any ordering deps hence.

Except of course, that things aren't *that* simple.

Socket activation works great of processes that actually are of the kind that binds a socket and listens on it for client requests. But during early boot and late shutdown things are quite different. `systemd-sysusers`, `systemd-tmpfiles`, `systemd-binfmt`, `systemd-sysctl`, `systemd-rfkill`, `fsck`, and so on, are quite different: they do not really stick around, their startup has to be scheduled precisely, after something and before something else. Where those somethings can be other services, or…

…devices popping up or various other things.

Because of that systemd always followed a hybrid approach: for regular daemons socket activation is recommended, but we have dependencies too, to cover in particular the earlier boot phases, and the final shutdown phases.

(Of course, quite unfortunately there are still too many 3rd party services that do not use socket activation and really should, but that's another story...)

With the advent of soft-reboots (remember: this kind of new-style userspace reboot, where systemd shuts down all of userspace again, then reexecs and starts up again, without actually rebooting the kernel) things become a bit more complex on the socket-activation vs. dependencies situation: one thing soft-reboot is supposed to allow is to exclude some select services from shutdown during soft-reboot in order to optimize grey-out times.

But that means that the previously simple logic of saying "use deps for early boot and late shutdown, prefer socket activation for the main runtime" doesn't work anymore, because if select services shall stay up during soft-reboot, then for them the regular runtime and the system's shutdown phase are concurrent. And similar, after the soft-reboot reexec the new boot's startup phase and the regular runtime of the select services is concurrent too.

And that actually creates problems: what if a service tries to talk to some other service while the system is going through the shutdown phase of a soft-reboot cycle, and the target service cannot be activated at that time, because after all stuff is supposed to be stopped, not started?

With v258 there are two new mechanisms to deal with this:

First of all there is a new job mode. (Job modes you can use to tweak how systemd enqueues your unit start/stop/reload/… requests and the deps of it, …

…you can control it via systemctl's `--job-mode=` switch for example). The new job mode is called "lenient". If used and the job you want to enqueue would in any way contradict what is already enqueued, then the operation will fail. It will never reverse any already enqueued job hence.

The other new mechanism is a setting in `.socket` files: `DeferTrigger=` can be used to potentially defer triggering of the associated service if its activation cannot be enqueued immediately due to conflicts.

This makes use of the new "lenient" job mode: the service is always triggered in this job mode, and as long as it fails its activation is deferred to a later point where hopefully it won't fail anymore, because conflicting jobs have been processed and hence don't conflict anymore. Activation is only deferred to some point though, a time-out for that can be configured via `DeferTriggerMaxSec=`.

Long story short: with these two new mechanisms it's now possible to have socket activated services do something somewhat reasonable during the shutdown phase of the system, so that a service that stays around during soft-reboot can just use it without any special handling that deals with the fact that the system goes through this cycle.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115128243121764853) (2025-09-01)
