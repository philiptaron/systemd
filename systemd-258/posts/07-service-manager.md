---
layout: post
title: "systemd 258 Feature Highlight #7"
date: 2025-06-01
source: https://mastodon.social/@pid_eins/114606769582857046
author: Lennart Poettering
---

7️⃣ Here's the 7th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

systemd is at its most basic a service manager, i.e. it runs programs, in a resource managed, security sandboxed way, properly ordered, and starts the system that way and keeps it running.

The focus for this kind of service management is really on services that are started no matter what, regardless of the resources available, because the underlying assumption…

## Thread Continuation

*2025-06-01* ([source](https://mastodon.social/@pid_eins/114606845728987717))

…only if the system is currently idle enough by some definition of "idle". Or in other words: instead of focussing on trying to start all enabled services as soon as possible, the focus is on utilizing the system well, but not putting more workload on it than it could reasonably well deal with for the moment. This kind of workload management assumes there's a lot more work to do than immediate processing time available, while the usual model systemd works with assumes…

*2025-06-01* ([source](https://mastodon.social/@pid_eins/114606847467543453))

…that while there might be temporary resource shortages it's always possible to run all enabled services concurrently sooner or later.

With v258 we are trying to bridge the gap a bit, and are teaching systemd some nice workload management functionality. The fundamental new knobs for this are on the .slice unit: there are two new controls ConcurrencySoftMax= and ConcurrencyHardMax=.

(For those who didn't pay attention, slice units are the fundamental resource management concept in systemd…

*2025-06-01* ([source](https://mastodon.social/@pid_eins/114606848567297224))

… for grouping services and applying combined limits and various scheduling parameters to them).

ConcurrencySoftMax= simply dictates how many units assigned to the slice may be concurrently active at the same time. If more units are queued for a slice, they'll have to wait until an active unit deactivates again (i.e. finishes its work). ConcurrencyHardMax= OTOH puts a hard limit onto how many units can be queued for a slice. If you try to enqueue more then the enqueuing will fail.

*2025-06-01* ([source](https://mastodon.social/@pid_eins/114606849802862188))

Or in other words: if you want to do some workload management, you can now define a slice, assign some resources to it, and then start enqueuing services on it, and they will be started one by one (or more, depending on how you pick the concurrency limits). 

And this is great, because you now have really nice workload job control, but at the same time retain all the nice systemd service mgmt features, such as logging, resource management, sandboxing and so on.

*2025-06-01* ([source](https://mastodon.social/@pid_eins/114606863232825422))

Oh, and yes, before you ask: simply pacing service activation by a per-slice concurrency counter is just one very simple mechanism of determining when a system is "idle". And yeah, we might eventually want to extend on this, for example we could look at CPU/IO/memory PSI information or so, activating more services only as long as the current workload doesn't cause too large latency on resources to acquire. But that's for later.

*2025-06-01* ([source](https://mastodon.social/@pid_eins/114607879927326533))

[@eliasp](https://mastodon.social/@eliasp) yes there's a dbus prop. And systemctl status on the slice even shows you current nr and the limits.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114606844706770803):** …is that they are all roughly equally important and necessary, and until they are all started the system isn't quite up.

In this model, if a system is resource constrained, then things might be a bit slower, but ultimately it will deliver the necessary work too, just maybe take a bit longer. Resource management can help priorizing things.

There's another pretty relevant mode of operation though: where instead of making everything available always workloads should be activated…

…only if the system is currently idle enough by some definition of "idle". Or in other words: instead of focussing on trying to start all enabled services as soon as possible, the focus is on utilizing the system well, but not putting more workload on it than it could reasonably well deal with for the moment. This kind of workload management assumes there's a lot more work to do than immediate processing time available, while the usual model systemd works with assumes…

## Sources

- [Original post](https://mastodon.social/@pid_eins/114606769582857046)
- [Thread continuation](https://mastodon.social/@pid_eins/114606845728987717)
- [Thread continuation](https://mastodon.social/@pid_eins/114606847467543453)
- [Thread continuation](https://mastodon.social/@pid_eins/114606848567297224)
- [Thread continuation](https://mastodon.social/@pid_eins/114606849802862188)
- [Thread continuation](https://mastodon.social/@pid_eins/114606863232825422)
- [Thread continuation](https://mastodon.social/@pid_eins/114607879927326533)
