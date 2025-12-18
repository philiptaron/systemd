---
layout: post
title: "ExecStart pipe flag"
date: 2025-07-02
---

Here's the 26th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

If you ever put together a systemd service, you must be aware of the `ExecStart=` setting, which declares the command line to actually invoke for the service. It's probably *the* most important setting of all.

`ExecStart=` has various features these days. Besides specifier expansion and a limited form of environment variable expansion, there are a couple of flags you can specify to alter how the command line is executed. These are denoted via special characters, such as `@`, `-`, `:`, `+`, `!` as first character of the setting's values. (Yes, this is a bit cryptic, we have to admit that).

With v258 we added one more such flag: `|` (i.e. the pipe symbol). If used, then instead of executing the specified command directly, it's invoked through the shell configured in the user database for the target user (i.e. the user configured in `User=` of the same service). Or in other words: we invoke the shell and pass the specified command via the `-c` parameter to it.

What's this good for? Of course, you could use this for embedding shell scripts into the service file, but we are not sure that would be too wise (since which shell is used is configured in the user record, not in the service, i.e. you might end up writing a zsh script that will be interpreted by bash or similar).

Our primary use case for this is different hence: it's to make sure our `sudo` replacement `run0` is nicer to use: typically people expect that interactive `run0` switches to the target account's configured shell (instead of `/bin/sh`), and that's what this new flag allows us to do.

---

> **[@agowa338](https://chaos.social/@agowa338)** Does that mean there can be another `|` within the command without having to wrap it into `'/bin/sh -c "foo|bar"'` as well?

Sure, but not sure if you actually want to do that, see my comments about that.

> **[@agowa338](https://chaos.social/@agowa338)** Well it for sure is better than fighting with having to nest escape syntax. Especially in regards to quotations... So removing one layer of escaping is definitely preferable. And which shell is used for a service account is also known. Sure it would be desirable if there was a separate switch for it, but it's also kinda not needed as at least at time of packaging it should be known in almost all cases anyway...

You can use the `:` modifier to disable env var expansion. Very useful for manual `` `sh -c` `` lines. (You cannot disable specifier expansion though)

> **[@agowa338](https://chaos.social/@agowa338)** I mainly referred to things like (pseudo code):
>
> ```
> ExecStartPre=/bin/sh -c "cat foo | sed "s/abc'\"/def/" | xargs foo"
> ```
>
> or
>
> ```
> ExecStartPre=/bin/sh -c "cat foo | xargs sh -c 'bar'"
> ```
>
> That is currently highly annoying to write (and there is probably no good way to write this within a service unit either. Sure better would be to create a script file, but why create a script file for a "one-liner" that isn't useful anywhere else...) Mainly applies to sed and awk, but maybe also others.

> **[@heftig](https://mastodon.online/@heftig)** It feels like we might want something like
>
> ```
> ExecStartFlags=no-fail privileged
> ```
>
> or
>
> ```
> ExecStart=[no-fail privileged] /usr/bin/foo
> ```
>
> instead of `ExecStart=-+/usr/bin/foo` to reduce the amount of cryptic prefixes.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114782700539340326) (2025-07-02)
