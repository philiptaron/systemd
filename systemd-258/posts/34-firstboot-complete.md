---
layout: post
title: "`systemd-firstboot` tab completion"
date: 2025-08-07
---

34 Here's the 34th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

When deploying "golden" images (i.e. carefully prepared unified images that are booted on many systems, where they acquire an identity of their own, as well as their own state on first boot), depending on context it makes sense to interactively ask the user for certain basic system settings, such as UI language, hostname, and similar.

For a longer time systemd shipped `systemd-firstboot` as a basic terminal based implementation to provide the interactive UI for this. It may be used in place of something more fancy and graphical in environments where that'd be overkill.

The tool gained some functionality over time, but it always remained very simplistic in its interface. With v258 we make it a bit more comfortable to use: there's now tab completion available in the various prompts it provides. When you are asked for locale settings, keyboard mappings, timezone, root shell choice it now will auto-complete your choices by hitting `TAB`, and show you a list of suitable options on `TAB` `TAB`, in a similar style to how this is done on interactive shells.

---

[systemd-firstboot]: https://www.freedesktop.org/software/systemd/man/258/systemd-firstboot.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114986213475696548) (2025-08-07)
