---
layout: post
title: "systemd-nspawn Hotkeys"
date: 2025-07-01
---

When booting up a `systemd-nspawn` container interactively, there's a special key combination `Ctrl-]` you can hit three times within 1s to terminate the container.

This termination is abrupt: all processes in the container are immediately terminated, there's no clean shutdown phase.

That is great for debugging, but it's not ideal for production: there it would be better to let the applications inside the container save their data properly, and let the system shut down cleanly. After all, `systemd-nspawn` is mostly focused on running full-blown containers with init systems as PID1, and that means one better should let the init system inside do its clean shutdown logic.

In v258 there's now an easy way to do just that. In addition to `^]^]^]` there are now two new hotkeys.

First of all there's `^]^]r` for rebooting the container. It's mostly identical to typing `reboot` in such a full-blown container, or to calling `machinectl reboot` on it from the outside.

And then there's `^]^]p` for powering off a container. You guessed, it's equivalent to typing `poweroff` in the container, or calling `machinectl poweroff` from the outside.

(Note that this only works if you actually run an init system inside the container, and it must implement `SIGRTMIN+4`/`SIGRTMIN+5` as a way of powering off or rebooting the container, compatible with how systemd itself has been doing it).

## Keyboard Layout Considerations

On non-US keyboard layouts, `Ctrl-]` is typically accessed via `Ctrl-AltGr-9` or similar combinations. For example, on German keyboards, the `]` character is a separate key.

The hotkeys are designed to be hard to hit by accident, which is why they require this specific sequence.

---

## References

- [`systemd-nspawn`](https://www.freedesktop.org/software/systemd/man/258/systemd-nspawn.html)
- [`machinectl`](https://www.freedesktop.org/software/systemd/man/258/machinectl.html)

## Sources

- [Original post](https://mastodon.social/@pid_eins/114776832571027618) (2025-07-01)
