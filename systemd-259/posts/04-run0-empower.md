---
layout: post
title: "run0 --empower"
date: 2025-11-21
---

4️⃣ Here's the 4th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

For this one I am simply going to top-post [@daandemeyer](https://mastodon.social/@daandemeyer)'s story about [`run0`][run0]'s new `--empower` switch, which gives your process capability + polkit privileges, without changing your user ID.
Very powerful stuff.

---

**[@daandemeyer](https://mastodon.social/@daandemeyer):**

In systemd 259, I'm making it possible to run commands that need privileges as your current user instead of as root.
With `run0 --empower`, you'll get a session as your current user in which you can do anything that root would be able to do, without actually being root.

This is very useful when you need to run something with privileges but still want all created files and directories to be owned by your current user.

I got inspired to implement this when I was playing around with bpftrace and sysdig and got annoyed that the files written by these tools were owned by root instead of my own user.
Now I can run `run0 --empower bpftrace` and be sure that any written files are owned by my own user instead of root.

---

> **[@funkylab](https://mastodon.social/@funkylab):** How does that work?

Instead of changing to root, we keep the current uid/gid and instead give it full [ambient capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html).
That's sufficient to pass all kernel privilege checks (disregarding LSMs).
To pass polkit checks, we run the `run0 --empower` session with the new `empower` group as an auxiliary group and we ship a polkit rule to allow all actions for users in the `empower` group.

Note that this won't work if a tool checks for uid 0 instead of capabilities.

---

> **[@felixs](https://chaos.social/@felixs):** Is this safe from manipulation by a debugger because the newly spawned process is not a child of run0 but of systemd?

A debugger will be able to attach just fine.
I've opened [a PR](https://github.com/systemd/systemd/pull/39839) to clarify that other processes of the selected user will be able to mess with the empowered session.

So using `run0 --empower` gives malicious processes a vector to infiltrate the system.
But so does `sudo -E PATH` or using sudo to execute anything in your home directory or using `sudo -s`, etc.

---

> **[@pemensik](https://fosstodon.org/@pemensik):** It seems potentially dangerous.
> Does it share configuration with `sudo` somehow?
> What users are allowed to use this in default configuration?

**Lennart:** This leaves auth to polkit, unifying auth at one place hence: polkit.
Regular users by default get to use it only after the usual polkit auth query.

---

[run0]: https://www.freedesktop.org/software/systemd/man/259/run0.html

## Sources

- [Daan's original thread](https://mastodon.social/@daandemeyer/115565105032166177) (2025-11-17)
- [Lennart's thread](https://mastodon.social/@pid_eins/115586469819973533) (2025-11-21)
