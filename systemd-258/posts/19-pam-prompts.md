---
layout: post
title: "PAM service prompts"
date: 2025-06-19
---

19. Here's the 19th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Service units for systemd can optionally register a `PAM` session, and run its processes inside.
This is used for a number of use cases, including `run0` (so that the target shell runs within a proper `PAM` session with all `PAM` modules in effect), and `user@*.service` (the system service that contains the per-user service manager).

This logic has been in place for a longer time, but there was a major limitation: `PAM` modules are supposed to be able to query the user for questions, such as passwords and similar.
So far, any such requests issued by the `PAM` session modules for such services were refused immediately, thus typically causing any relevant `PAM` modules to fail.

This has worked great for a long time, since thankfully `PAM` session modules even though they can – typically don't prompt for anything.

Except of course, that that's not quite true anymore: `systemd-homed` manages per-user encrypted file systems that are unlocked at login time.
This is systematically different from the weak security model of traditional UNIX home directories where encryption does not take place per-user, and the data of the user is protected by system-wide encryption at best (which is unlocked at boot time and that's it), and thus privileged code (incl. the admin) has free access to the user's data anytime.

To be able to access a user's home directory (when managed with `systemd-homed`) it is thus strictly necessary to acquire the decryption key for it, and that must come from somewhere – typically a `PAM` question for the user's password.

Thus, when using `run0` or `user@.service` on some user that hasn't already been unlocked strictly requires interactive answers to password prompts, except that as mentioned before we'd deny those.
Or in other words, so far, using `user@.service` in lingering mode or accessing a user account via `run0` (if the account uses `systemd-homed` and wasn't logged in already) would always fail.

In v258 we are doing something about it: if a `PAM` session ends up requesting the user to answer a question this will no longer just be refused, but instead be forwarded to the usual "ask-password" subsystem of systemd, that is also used to handle LUKS FDE password prompts, and which can ask for passwords via `Plymouth` (i.e. via the boot-time splash) or locally in a TTY.

The effect of this is really nice, it means you can now use `systemd-homed` home directories even in lingering mode – however, if you do you'll be prompted for the user's password at boot as part of the boot process.
Moreover you can now nicely log into a `systemd-homed` account via `run0 -u …`, and simply provide the unlock password from there.

---

## Q&A

> **Werhaus** Is this also supporting other `PAM` modules? I'm thinking about 2FA and IAM solutions here

Yeah, it's generic, if a `PAM` module asks a question via `pam_conv` stuff, it will be processed via the askpw logic.

> **JigenDaisukeJr** I said it before and I'll say it again - `systemd-homed` is one of the best ways to manage user's home in modern systems. And what is the "lingering mode", btw?

See [loginctl - enable-linger](https://www.freedesktop.org/software/systemd/man/latest/loginctl.html#enable-linger%20USER%E2%80%A6)

It basically allows you to run per-user services headless already at boot and until shutdown, independently of having an interactive login session.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114710109344141459) (2025-06-19)
