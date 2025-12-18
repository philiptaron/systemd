---
layout: post
title: "systemd 258 Feature Highlight #9"
date: 2025-06-03
source: https://mastodon.social/@pid_eins/114618473677694301
author: Lennart Poettering
---

9️⃣ Here's the 9th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

Most Linux folks probably spend much of their day in their terminal emulator. Such emulators ultimately reimplement in software what dedicated hardware terminals did in the 1980's and before. While the protocol terminals speak didn't change much in its most basic concepts, various extensions have been added over the years to integrate terminal emulators better with the windowing…

## Thread Continuation

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618503381661765))

I think such integration between terminal emulators and the programs, sessions, and infrastructure that runs within them is truly useful, in order to enhance the user experience for an otherwise conceptually quite limited UI concept.

With systemd v258 we added support for a new terminal control (people usually call these "ansi sequences", though a major part of the ones people actually use are definitely not an ANSI standard) that allows communicating a *lot* more meta information…

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618518160867680))

…from terminal payload to terminal emulator: we came up with a new "ansi" sequence that can be used to define and maintain a stack of *contexts* that tell emulators about what is going on inside the terminal.

What does "context" mean in the above? A context in this sense is basically the runtime of a specific program taking over the terminal's tty device. i.e. typically in a terminal emulator you start out with an interactive shell, that's already your first context.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618529538989623))

You then invoke some shell tool, let's say "ls". That's your second context. The tool then exits, now the second context is closed you are back at the first shell context. Now you ssh to some other host. That's a new second context. On that other host you invoke "run0" (or "sudo -s" if you must), that's a third context, from which you then invoke "echo", that's your fourth, and so on.

Each of these invoked tools might output a thing or two onto the terminal. Or, to turn this around:

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618541448333384))

each character cell on your terminal that has been written to, conceptually can be associated with a context from which it was initialized.

The new ansi sequence informs the terminal emulator about contexts as they are opened, or closed. And most importantly, the sequence allows attaching various bits of meta information to each context: which host they have been created by, what kind of context they are (i.e. shell, remote shell, privilege upgrade, and so on), which user ID they belong to, …

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618552088765897))

…, which service, which cgroup, which container, …. Moreover, metadata can be updated for running contexts, and when closing them. For example when a program invoked from a shell starts among the metadata reported to the emulators is the command lone invoked, but when the program ends the exit status of the command can be attached too.

What is this all good for? Well, that's ultimately up for the terminal emulator developers to decide. Here are some ideas though:

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618561684057891))

1. the background of each context could be tinted based on the context type, (or maybe even using a hashed color of the target host or similar), highlighting output from privileged run0/sudo sessions or from remote sessions, to distinguishing their output visually from unpriv/local commands.

2. Meta information could be made visible via a mouse-over tooltip showing the available metainformation.

3. Failing commands could be specially marked with a red marker where their context ends.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618572152794451))

4. A margin could be displayed on the left or right of the screen that shows marks or brackets where a context starts and ends. The margin could also show an emoji or other symbol whenever a failure is seen on some command.

5. A right click on some output line could open a menu that allows starting a log browser that filters for the generating service and hostname.

6. A right click on some output line could open a menu that offers an item to kill the process or a service that generated it.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618584562625987))

7. The terminal emulator could offer some kind of bookmarking feature, or table of contents display that visualizes the various contexts in a tree.

Those are just some ideas: I am sure others can come up with a lot more.

v258 will generate these context sequences at almost all places where that makes sense. (There's only omission: ssh remoting is not covered right now, because that's outside of our control).

The specification for the new sequence you find here:

<https://github.com/systemd/systemd/blob/main/docs/OSC-CONTEXT.md>

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618593855905461))

And before you ask: no I am not aware of any existing terminal emulator that already makes use of all this information. This is after all an entirely new thing, invented and defined by the systemd project.

My hope is that sooner or later this will find adoption in terminal emulators, given that this is now generated by all systemd systems all over the place, by default.

Oh, and in case you wonder: existing terminal emulators that do no understand this sequence will just ignore it.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618595956894469))

It's a feature for those who want to use it, and for all others, it's invisible.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618616141109297))

(Oh, and in case you hack on a terminal emulator, and you do decide to make use of this, would be delighted to learn about this, and what you are doing with it. And I am sure others would be too. Hence, please feel invited to add a comment and link here about your work. Thanks!)

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618635044044171))

[@anthropy](https://mastodon.derg.nz/@anthropy) well, the security model of terminals is quite flawed anyway. This isn't make things worse. It could make things better (for example, we could in theory overload each context that indicates a security transition with some actual security functionality, i.e. that queued keypress cannot be delivered across security context boundaries or so). But frankly, this sounds too complicated, and probably would frustrate people a lot too.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618671812712672))

[@arrjay](https://tacobelllabs.net/@arrjay) you can disable this sequences (and all others) via TERM=dumb.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618691023890206))

[@alg0w](https://social.vivaldi.net/@alg0w) the concept assumes theres's only one fg context. That matches the tty logic which only knows one foreground process group. 

The context stuff is not supposed to be a security feature. That said, systemd actually makes sure the context ids (which are used to relate open/close sequences with each other) are reasonably long and from a safe source (i.e. randomized using getrandom() or hashed with a cryptographic hash func from some other data), so that they are not guessable.

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618700846235693))

[@alg0w](https://social.vivaldi.net/@alg0w) that means it should be quite hard to interfere with the context stack in a bad way (i.e. close contexts further up the tree). 

But again, this is explicitly not supposed to be a security concept, exactly because we cannot expect everyone to generate them in "secure" ways, even if systemd itself is carefully written in that regard.

Not that if some tool doesn't close the contexts it creates the failure mode should be nice: the calling tool will eventually and implicity close all…

*2025-06-03* ([source](https://mastodon.social/@pid_eins/114618701741270673))

[@alg0w](https://social.vivaldi.net/@alg0w) …nested contexts once it takes over again.

*2025-09-05* ([source](https://mastodon.social/@pid_eins/115152222125773208))

[@dolmen](https://mamot.fr/@dolmen) [@alg0w](https://social.vivaldi.net/@alg0w) might simply be an ordering issue, i.e. /etc/profile.d/80-systemd-osc-context.sh is what systemd adds. Depending how you want your extra output attributed to a context, you might want to name your package's drop-in for that dir before or after that, i.e. with a prefix < "80-" or > "80-"

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114618489331467675):** …environment they nowadays run on. For example, early on terminal emulators provided controls to change the window title, and since a long time most shell configurations make use of that to show the user name or hostname in the window title.

More recently added where controls that allow interactive shells that run in terminals (e.g. bash or zsh) to tell terminal emulators when a prompt begins, when it ends and what command it is about to execute.

I think such integration between terminal emulators and the programs, sessions, and infrastructure that runs within them is truly useful, in order to enhance the user experience for an otherwise conceptually quite limited UI concept.

With systemd v258 we added support for a new terminal control (people usually call these "ansi sequences", though a major part of the ones people actually use are definitely not an ANSI standard) that allows communicating a *lot* more meta information…

## Sources

- [Original post](https://mastodon.social/@pid_eins/114618473677694301)
- [Thread continuation](https://mastodon.social/@pid_eins/114618503381661765)
- [Thread continuation](https://mastodon.social/@pid_eins/114618518160867680)
- [Thread continuation](https://mastodon.social/@pid_eins/114618529538989623)
- [Thread continuation](https://mastodon.social/@pid_eins/114618541448333384)
- [Thread continuation](https://mastodon.social/@pid_eins/114618552088765897)
- [Thread continuation](https://mastodon.social/@pid_eins/114618561684057891)
- [Thread continuation](https://mastodon.social/@pid_eins/114618572152794451)
- [Thread continuation](https://mastodon.social/@pid_eins/114618584562625987)
- [Thread continuation](https://mastodon.social/@pid_eins/114618593855905461)
- [Thread continuation](https://mastodon.social/@pid_eins/114618595956894469)
- [Thread continuation](https://mastodon.social/@pid_eins/114618616141109297)
- [Thread continuation](https://mastodon.social/@pid_eins/114618635044044171)
- [Thread continuation](https://mastodon.social/@pid_eins/114618671812712672)
- [Thread continuation](https://mastodon.social/@pid_eins/114618691023890206)
- [Thread continuation](https://mastodon.social/@pid_eins/114618700846235693)
- [Thread continuation](https://mastodon.social/@pid_eins/114618701741270673)
- [Thread continuation](https://mastodon.social/@pid_eins/115152222125773208)
