---
layout: post
title: "Terminal context sequences"
date: 2025-06-03
---

Most Linux folks probably spend much of their day in their terminal emulator. Such emulators ultimately reimplement in software what dedicated hardware terminals did in the 1980's and before. While the protocol terminals speak didn't change much in its most basic concepts, various extensions have been added over the years to integrate terminal emulators better with the windowing environment they nowadays run on. For example, early on terminal emulators provided controls to change the window title, and since a long time most shell configurations make use of that to show the user name or hostname in the window title.

More recently added where controls that allow interactive shells that run in terminals (e.g. bash or zsh) to tell terminal emulators when a prompt begins, when it ends and what command it is about to execute.

I think such integration between terminal emulators and the programs, sessions, and infrastructure that runs within them is truly useful, in order to enhance the user experience for an otherwise conceptually quite limited UI concept.

With systemd v258 we added support for a new terminal control (people usually call these "ANSI sequences", though a major part of the ones people actually use are definitely not an ANSI standard) that allows communicating a *lot* more meta information from terminal payload to terminal emulator: we came up with a new ANSI sequence that can be used to define and maintain a stack of *contexts* that tell emulators about what is going on inside the terminal.

What does "context" mean in the above? A context in this sense is basically the runtime of a specific program taking over the terminal's tty device. i.e. typically in a terminal emulator you start out with an interactive shell, that's already your first context.

You then invoke some shell tool, let's say `ls`. That's your second context. The tool then exits, now the second context is closed you are back at the first shell context. Now you `ssh` to some other host. That's a new second context. On that other host you invoke `run0` (or `sudo -s` if you must), that's a third context, from which you then invoke `echo`, that's your fourth, and so on.

Each of these invoked tools might output a thing or two onto the terminal. Or, to turn this around: each character cell on your terminal that has been written to, conceptually can be associated with a context from which it was initialized.

The new ANSI sequence informs the terminal emulator about contexts as they are opened, or closed. And most importantly, the sequence allows attaching various bits of meta information to each context: which host they have been created by, what kind of context they are (i.e. shell, remote shell, privilege upgrade, and so on), which user ID they belong to, which service, which cgroup, which container, etc. Moreover, metadata can be updated for running contexts, and when closing them. For example when a program invoked from a shell starts among the metadata reported to the emulators is the command line invoked, but when the program ends the exit status of the command can be attached too.

What is this all good for? Well, that's ultimately up for the terminal emulator developers to decide. Here are some ideas though:

1. The background of each context could be tinted based on the context type, (or maybe even using a hashed color of the target host or similar), highlighting output from privileged `run0`/`sudo` sessions or from remote sessions, to distinguishing their output visually from unpriv/local commands.

2. Meta information could be made visible via a mouse-over tooltip showing the available metainformation.

3. Failing commands could be specially marked with a red marker where their context ends.

4. A margin could be displayed on the left or right of the screen that shows marks or brackets where a context starts and ends. The margin could also show an emoji or other symbol whenever a failure is seen on some command.

5. A right click on some output line could open a menu that allows starting a log browser that filters for the generating service and hostname.

6. A right click on some output line could open a menu that offers an item to kill the process or a service that generated it.

7. The terminal emulator could offer some kind of bookmarking feature, or table of contents display that visualizes the various contexts in a tree.

Those are just some ideas: I am sure others can come up with a lot more.

v258 will generate these context sequences at almost all places where that makes sense. (There's only omission: ssh remoting is not covered right now, because that's outside of our control).

The specification for the new sequence you can find here: [OSC-CONTEXT.md](https://github.com/systemd/systemd/blob/main/docs/OSC-CONTEXT.md)

And before you ask: no I am not aware of any existing terminal emulator that already makes use of all this information. This is after all an entirely new thing, invented and defined by the systemd project.

My hope is that sooner or later this will find adoption in terminal emulators, given that this is now generated by all systemd systems all over the place, by default.

Oh, and in case you wonder: existing terminal emulators that do no understand this sequence will just ignore it.

It's a feature for those who want to use it, and for all others, it's invisible.

(Oh, and in case you hack on a terminal emulator, and you do decide to make use of this, I would be delighted to learn about this, and what you are doing with it. And I am sure others would be too. Hence, please feel invited to add a comment and link here about your work. Thanks!)

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114618473677694301) (2025-06-03)
