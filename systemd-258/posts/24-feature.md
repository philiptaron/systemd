---
layout: post
title: "systemd 258 Feature Highlight #24"
date: 2025-06-30
source: https://mastodon.social/@pid_eins/114771082006844631
author: Lennart Poettering
---

2️⃣4️⃣ Here's the 24th  post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Terminals are weird beasts. Today's technical UNIX folks probably spend most of their day in them, but they are ultimately tech with roots in the 1950's, with the most relevant specs being from the 2nd half of the 1970s. That's from before most folks in today's IT were even born!

Back in the days, there were many competing terminal protocols, and hence on UNIX systems…

## Thread Continuation

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771111749844661))

…which terminal you have and how the entry in the database is identified. That's what the $TERM environment variable declares. Moreover, as you move between systems (i.e. ssh from one host to the next, from the to another one and so on), $TERM is usually propagated, but it's not guaranteed at all that the database entry referenced by $TERM is actually installed on each target host, so how useful is that even? And then: given that modern terminal emulators nowadays all reimplement…

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771136449067592))

…mostly the same three "standards" (i.e. ANSI x3.64, DEC VTxxx, xterm sequences), what's even the value of termcap/terminfo entries?

Moreover, it's quite hard to get terminfo updated these days, and there is no version negotation, hence whatever it reports, tends to be out of date.

Because of all this, terminal emulators started to lie about their identity (they just set $TERM to some flavour of "xterm"), and apps started to ignore the true meaning of $TERM.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771150391785640))

In particular it's quite common to set $TERM to something old, common and widely supported (e.g. vt100), and still expect various modern features (such as colors) to just work. For example coreutils' "dircolors" tool generates color sequences on vt100, even though vt100 really definitely never had color support.

And then, there's also the problem around serial terminals: unlike with ssh sessions for example, $TERM is not propagated as part of the transport protocol.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771161591442650))

But serial terminals matter, they are widely used to talk to VMs, to embedded devices, or servers. Having them work properly kinda matters.

You could summarize all of the above as: everything kinda sucks around terminal feature negotiation.

So, let's try to make some improvements where we can, right?

With v258 we tried that at various places:

First of all, there are two newer de-facto "standards" these days that terminal tools and emulators support for reporting/controlling color…

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771173691234213))

…support: $COLORTERM and $NO_COLOR. The former "overrides" $TERM to communicate what kind of color support a terminal has. Thus, there's now a way to report "I am a VT100, but I can do color". Which of course is ahistoric, but a pretty common thing for terminals to claim. The latter allows direct control of color output (the latter even has kind of a spec, on <https://no-color.org/>). 

With systemd v258 the whole codebase not only supports these two additional env vars everywhere were we…

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771185357720320))

…generate terminal color sequences, but we also set/propagate them wherever we set/propagate $TERM itself. (And I think ssh would do good if they'd start to propagate the two vars by default too, just like $TERM). 

Moreover, we added support for limited auto-discovery of $TERM: as part of TTY initialization, systemd will now query the terminal for its terminfo database identifier, and then set $TERM to it. This is nowadays relatively widely supported, but not universal, and definitely so far…

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771196203509235))

…underused. We hope that now that systemd issues these sequences as part of its usual terminal reset sequence this will find the universal adoption it deserves. Note that vte-based terminals (i.e. Gnome's various offers in this areas) do not support this right now, but there's work in progress to add that). Also note that systemd is very careful when using the data: before setting $TERM from this, it will check if there actually is a terminfo entry for the identifier installed. (This…

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771205248893430))

…is a quick access(F_OK) check).

Net result: in various scenarios where $TERM hasn't been communicated otherwise, we'll now get a hopefully correct value set up automatically, for any TTY that you ask systemd to initialize (which is the case for system gettys and so on). In particular this means for all serial terminals $TERM should now be set reasonably.

This is not going to single-handedly magically "fix" the situation around terminal feature negotiation, but I think it will…

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771210105872868))

…make things a good step better: there's a good chance now we'll report more useful/correct information in more cases, reducing the chance of mismatches between terminal emulators and the tools running in them.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771238572182216))

Oh, and note that in v257 we already added support for propagating terminal dimension information when initializing TTYs. The combination of that together with this $TERM auto-detection makes working via serial terminals almost as nice as using an SSH connection.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771239380787031))

[@bazzargh](https://hachyderm.io/@bazzargh) fixed.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771250427402134))

[@urosm](https://toot.si/@urosm) Sorry, not buying into a theme of "race to the bottom because of personal distastes".

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771368710714986))

[@urosm](https://toot.si/@urosm) you seem to imply it's a bug in systemd if your terminal emulator cannot display some of the most popular unicode chars, even though it's one in your terminal emulator/distro, if I may say so.

Also you can set SYSTEMD_EMOJI=0 if you like, and they are all gone.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771629203731853))

[@grawity](https://social.treehouse.systems/@grawity) Every time we initialize a TTY. which is once at boot for /dev/console, but then again before and after each getty invocation. We always issue a bunch of sequences anyway, to ensure that no state from a previous getty cycle leaks into the next owner of a tty. As that'd be a security issue.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771629649471753))

[@grawity](https://social.treehouse.systems/@grawity) But yeah, if you are logged in via serial, and then disconnect your terminal emulator without this triggering a carrier reset and then come back with a completely different terminal emulator we'd of course stick with the original $TERM, and things are broken. We cannot really address that… But I don't think that's a common case.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114771641564133767))

[@urosm](https://toot.si/@urosm)

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114773044890291771))

[@grawity](https://social.treehouse.systems/@grawity) of course getty or bash could reissue the detection logic if they want, but conceptually its nicer to do this before first output is generated (i.e. the login prompt), not after, I'd claim.

*2025-06-30* ([source](https://mastodon.social/@pid_eins/114773061443550441))

[@grawity](https://social.treehouse.systems/@grawity) btw if you turn off "clocal" via stty then carrier detection should work if lines have it. Most serial gettys allow you to configure that, for example agetty via --local-line=never

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114771101652590459):** …there were systems designed to store properties of/differences between hardware terminals, so that libraries could abstract over the differences: termcap and terminfo. In a way they play the role of declarative "device drivers" for the terminals.

They have some weird semantics though: you traditionally cannot ask a terminal for its terminfo/termcap data, it's stored in a separate database, and there's no way to connect the terminal with its database entry: you need to "know"…

…which terminal you have and how the entry in the database is identified. That's what the $TERM environment variable declares. Moreover, as you move between systems (i.e. ssh from one host to the next, from the to another one and so on), $TERM is usually propagated, but it's not guaranteed at all that the database entry referenced by $TERM is actually installed on each target host, so how useful is that even? And then: given that modern terminal emulators nowadays all reimplement…

## Sources

- [Original post](https://mastodon.social/@pid_eins/114771082006844631)
- [Thread continuation](https://mastodon.social/@pid_eins/114771111749844661)
- [Thread continuation](https://mastodon.social/@pid_eins/114771136449067592)
- [Thread continuation](https://mastodon.social/@pid_eins/114771150391785640)
- [Thread continuation](https://mastodon.social/@pid_eins/114771161591442650)
- [Thread continuation](https://mastodon.social/@pid_eins/114771173691234213)
- [Thread continuation](https://mastodon.social/@pid_eins/114771185357720320)
- [Thread continuation](https://mastodon.social/@pid_eins/114771196203509235)
- [Thread continuation](https://mastodon.social/@pid_eins/114771205248893430)
- [Thread continuation](https://mastodon.social/@pid_eins/114771210105872868)
- [Thread continuation](https://mastodon.social/@pid_eins/114771238572182216)
- [Thread continuation](https://mastodon.social/@pid_eins/114771239380787031)
- [Thread continuation](https://mastodon.social/@pid_eins/114771250427402134)
- [Thread continuation](https://mastodon.social/@pid_eins/114771368710714986)
- [Thread continuation](https://mastodon.social/@pid_eins/114771629203731853)
- [Thread continuation](https://mastodon.social/@pid_eins/114771629649471753)
- [Thread continuation](https://mastodon.social/@pid_eins/114771641564133767)
- [Thread continuation](https://mastodon.social/@pid_eins/114773044890291771)
- [Thread continuation](https://mastodon.social/@pid_eins/114773061443550441)
