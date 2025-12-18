---
layout: post
title: "Kernel module conditions"
date: 2025-08-12
---

systemd tries to bridge the gap between being modular and flexibly supporting a wide range of systems and devices on one hand, and being somewhat quick and efficient to boot up on the other.
These two goals are sometimes opposing forces: on many systems step X has to be done on boot, but each such step X costs dearly on other systems where X is not needed.

In order to find a good balance between these two goals we early on devised a concept of unit "conditions": the various `ConditionXYZ=` setting in unit files can be used to skip activation of it in case some preconditions are not met.
That way, it is safe to always enqueue some unit at boot, but then skip its actual execution if we determine it to be unnecessary for some reason.

With v258 we added one more such condition stanza:

The `ConditionKernelModuleLoaded=` unit file setting takes a kernel module name, and if the specified kernel module is already loaded (or directly built into the kernel already), the unit is skipped in its entirety (as usual the condition can also be inverted for other use cases).

The primary place where this is useful: in the `modprobe@.service` template service.
This service unit is instantiated for each kernel module that needs to be loaded explicitly for some subsystem to operate (i.e. for cases where regular kernel module auto-loading via device nodes, or via udev probing doesn't work).
By using this stanza it's now possible to very efficiently suppress unnecessary modprobe invocations at boot in cases where the relevant modules are already loaded or are built into the kernel already, but at the same time load them in cases where they haven't been.

These cases actually matter more than one might think, since big distributions vary wildly in what they link into the kernel and what they don't.
The `modprobe@.service` dependencies configured in systemd's default units hence typically declare the "worst case scenario", i.e. where the least number of modules are linked in, which traditionally would slow down systems that link more in though.

(This also is more visible than people might think, because the initrd might load a bunch of `kmod`s we might try to load from later userspace again, which of course just wastes resources.)

Oh, and one last note: you might wonder, why this needs to be a stanza of its own, why can't this just implemented via `ConditionPathExists=/sys/module/$module`?
That's because that subdir is created when a `kmod` is begun to be loaded, not when it completed to be loaded.
Thus, if we'd use that in `modprobe@.service`, then the unit could not be used as a synchronization point anymore, as anything ordered `After=` it, might already be started at a time the `kmod` is still in the process of initialization.

---

> **[@stepech](https://fosstodon.org/@stepech)** is it really ConditionKernelModuleLoaded that checks the condition and if the module is indeed loaded, it doesn't execute? It sounds counter intuitive. ModuleLoaded and launches only if unloaded. Or am I understanding it incorrectly?

It's the syntax of `ConditionXYZ=` in general, that when satisfied, the unit doesn't execute.

---

[Original thread](https://mastodon.social/@pid_eins/115016549897778350) (2025-08-12)

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115016549897778350)
