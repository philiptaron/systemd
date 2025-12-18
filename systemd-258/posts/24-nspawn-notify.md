---
layout: post
title: "Terminal feature negotiation improvements"
date: 2025-06-30
---

Here's the 24th post highlighting key new features of the upcoming v258 release of systemd.

Terminals are weird beasts. Today's technical UNIX folks probably spend most of their day in them, but they are ultimately tech with roots in the 1950s, with the most relevant specs being from the 2nd half of the 1970s. That's from before most folks in today's IT were even born!

Back in the days, there were many competing terminal protocols, and hence on UNIX systems there were systems designed to store properties of/differences between hardware terminals, so that libraries could abstract over the differences: `termcap` and `terminfo`. In a way they play the role of declarative "device drivers" for the terminals.

They have some weird semantics though: you traditionally cannot ask a terminal for its terminfo/termcap data, it's stored in a separate database, and there's no way to connect the terminal with its database entry: you need to "know" which terminal you have and how the entry in the database is identified. That's what the `$TERM` environment variable declares. Moreover, as you move between systems (i.e., `ssh` from one host to the next, from the to another one and so on), `$TERM` is usually propagated, but it's not guaranteed at all that the database entry referenced by `$TERM` is actually installed on each target host, so how useful is that even? And then: given that modern terminal emulators nowadays all reimplement mostly the same three "standards" (i.e., ANSI x3.64, DEC VTxxx, xterm sequences), what's even the value of termcap/terminfo entries?

Moreover, it's quite hard to get terminfo updated these days, and there is no version negotiation, hence whatever it reports, tends to be out of date.

Because of all this, terminal emulators started to lie about their identity (they just set `$TERM` to some flavour of "xterm"), and apps started to ignore the true meaning of `$TERM`.

In particular it's quite common to set `$TERM` to something old, common and widely supported (e.g. vt100), and still expect various modern features (such as colors) to just work. For example coreutils' `dircolors` tool generates color sequences on vt100, even though vt100 really definitely never had color support.

And then, there's also the problem around serial terminals: unlike with ssh sessions for example, `$TERM` is not propagated as part of the transport protocol.

But serial terminals matter, they are widely used to talk to VMs, to embedded devices, or servers. Having them work properly kinda matters.

You could summarize all of the above as: everything kinda sucks around terminal feature negotiation.

So, let's try to make some improvements where we can, right?

With v258 we tried that at various places:

First of all, there are two newer de facto "standards" these days that terminal tools and emulators support for reporting/controlling color support: `$COLORTERM` and `$NO_COLOR`. The former "overrides" `$TERM` to communicate what kind of color support a terminal has. Thus, there's now a way to report "I am a VT100, but I can do color". Which of course is ahistoric, but a pretty common thing for terminals to claim. The latter allows direct control of color output (the latter even has kind of a spec, on https://no-color.org/).

With systemd v258 the whole codebase not only supports these two additional env vars everywhere we generate terminal color sequences, but we also set/propagate them wherever we set/propagate `$TERM` itself. (And I think `ssh` would do good if they'd start to propagate the two vars by default too, just like `$TERM`).

Moreover, we added support for limited auto-discovery of `$TERM`: as part of TTY initialization, systemd will now query the terminal for its terminfo database identifier, and then set `$TERM` to it. This is nowadays relatively widely supported, but not universal, and definitely underused. We hope that now that systemd issues these sequences as part of its usual terminal reset sequence this will find the universal adoption it deserves. Note that VTE-based terminals (i.e., GNOME's various terminal offerings) do not support this right now, but there's work in progress to add that. Also note that systemd is very careful when using the data: before setting `$TERM` from this, it will check if there actually is a terminfo entry for the identifier installed. (This is a quick `access(F_OK)` check).

Net result: in various scenarios where `$TERM` hasn't been communicated otherwise, we'll now get a hopefully correct value set up automatically, for any TTY that you ask systemd to initialize (which is the case for system gettys and so on). In particular this means for all serial terminals `$TERM` should now be set reasonably.

This is not going to single-handedly magically "fix" the situation around terminal feature negotiation, but I think it will make things a good step better: there's a good chance now we'll report more useful/correct information in more cases, reducing the chance of mismatches between terminal emulators and the tools running in them.

Note that in v257 we already added support for propagating terminal dimension information when initializing TTYs. The combination of that together with this `$TERM` auto-detection makes working via serial terminals almost as nice as using an SSH connection.

---

## Q&A

Oh, and IIRC if you hit enter 3 times on login prompt login exits and getty restarts. Which as side effect will reinit the tty/refresh `$TERM`, hence there's at least a simple manual way how users can refresh things if they want.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114771082006844631) (2025-06-30)
