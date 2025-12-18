---
layout: post
title: "systemd 258 Feature Highlight #2"
date: 2025-05-22
source: https://mastodon.social/@pid_eins/114550305394053015
author: Lennart Poettering
---

2️⃣ Here's the 2nd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

On UNIX systems every user registered on a local user owns a private directory: the "home" directory, where the user's configuration and data is saved and stored. In systemd there's systemd-homed which can manage that home directory securely, encrypted with a key that is provided at login time.

In most cases having a single home directory for each user is enough.

## Thread Continuation

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550331485403415))

…, as they want, and easily switch between them, simply by logging in specifying a user name of "username%areaname" at login time, when the system asks for a username.

This will primarily do two things: if you log in as user "foo" with area "bar" (i.e. specify "foo%bar" at login time), you end up with $HOME set to /home/foo/Areas/bar; it will also do something similar for $XDG_RUNTIME_DIR, to give your session a separate runtime directory.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550344078634343))

In order to create such an area anew you can simply call "mkdir -p ~/Areas && cp -av /etc/skel ~/Areas/mynewarea". To remove it again just do "rm -rf ~/Areas/mynewarea" – you get the idea.

Of course, since all areas are owned by the same underlying UID, and associated with the same user record you can easily move around between the areas and the main home directory, via "cd" and similar.

The simple concept of areas can be used in various quite powerful ways.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550357232745639))

My personal usecase for this goes something like this: I regularly build disk images for VMs of different distributions on my host, for building and testing systemd and other stuff. And I want access to my host user's home dir in each when booting them up, but not necessarily log directly into my host's home directory, but keep a separate area for each such image, so that the build trees in it can be distinct, do not leak context into each other, and can be created anew and flushed out…

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550365815187692))

… easily. I also want full access to all my data from each such VM to simplify my work. And the area concept allows me to do all that.

Note that while this 'virtualizes' $HOME and $XDG_RUNTIME_DIR nicely, it's not quite enough to run multiple full desktop environments in parallel for each user by giving them each an area of their own. That's because the per-user service manager only exists once right now, not in one instance per area.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550373067181529))

But there's no reason for not supporting that properly besides of "Lennart didn't find the time to make it work yet". I think we should totally support that too, so that each user can have one per-user service manager for the main area, and then one for each additional area. With that in place, you could have multiple parallel DE sessions, nicely separated in context (but not in privilege) in parallel, from the same home dir.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550378175037063))

And before you ask: all this is a systemd-homed feature, it's not implemented for classic UNIX users (as systemd is not involved with managemen of them, and couldn't do the area management there), and it's unlikely it every will be. The user record extensions to make areas a thing are generic though.

And that's all for now.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550396969650709))

[@xbezdick](https://masto.ai/@xbezdick) No, I am talking about systemd-homed managed users, not IPA managed users. If you are looking for IPA features, ask he IPA community for help, I am not the right person for that.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114550437912405150))

[@quite](https://mstdn.social/@quite) It's not a sandboxing feature, it's in fact expressly not about privilege.

If you want privilege separation then just create a separate user?

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114551047691172035))

[@levitte](https://mastodon.nu/@levitte) direnv is just about storing env var info in specific dirs?

that is a very different concept from homed's "areas", which give you additional dirs you can get a somewhat full-blown session in.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114551053058613762))

[@arrieseveneight](https://hachyderm.io/@arrieseveneight) it was lowercase, i changed on request from reviewers to uppercase to match the default naming of the xdg user dirs spec, i.e. "Documents", "Templates", "Pictures" and so on.

*2025-05-22* ([source](https://mastodon.social/@pid_eins/114551064813852510))

[@arrieseveneight](https://hachyderm.io/@arrieseveneight) yeah, we can make this configurable eventually, but do note it's never going to implement the xdg base dir spec, because after all the settings for the xdg base dir spec are stored in the home dir, but areas are about moving home dirs, hence cannot you cannot store the location where to store them in them...

but we could add a field for it in the user record. For now, to me this is more bikeshedding. there's more important stuff in my eyes.

*2025-05-26* ([source](https://mastodon.social/@pid_eins/114573149204838605))

[@S1m](https://infosec.exchange/@S1m) homed does not implement a sandbox.

I mean, it might make sense to one day maybe run each user's sessions inside a sandbox, but that should be independent of homed I'd say.

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/114550318767141575):** But in various scenarios it is handy to have a single login account, but multiple home directories one can switch between, for example to maintain different configuration sets, or build environments, possibly for different hosts.

In v258 systemd-homed (and by extension the userdb logic) has a concept for maintaining multiple "areas" for each user account. Areas in this sense are simply subdirectories of the main home directory, below the ~/Areas/ hierarchy. A user can have as many of these, …

…, as they want, and easily switch between them, simply by logging in specifying a user name of "username%areaname" at login time, when the system asks for a username.

This will primarily do two things: if you log in as user "foo" with area "bar" (i.e. specify "foo%bar" at login time), you end up with $HOME set to /home/foo/Areas/bar; it will also do something similar for $XDG_RUNTIME_DIR, to give your session a separate runtime directory.

> **[@xbezdick@masto.ai](https://masto.ai/@xbezdick/114550334362298321):** [@pid_eins](https://mastodon.social/@pid_eins) Im interested in trying this, does it work well with freeipa?

[@xbezdick](https://masto.ai/@xbezdick) No, I am talking about systemd-homed managed users, not IPA managed users. If you are looking for IPA features, ask he IPA community for help, I am not the right person for that.

## Sources

- [Original post](https://mastodon.social/@pid_eins/114550305394053015)
- [Thread continuation](https://mastodon.social/@pid_eins/114550331485403415)
- [Thread continuation](https://mastodon.social/@pid_eins/114550344078634343)
- [Thread continuation](https://mastodon.social/@pid_eins/114550357232745639)
- [Thread continuation](https://mastodon.social/@pid_eins/114550365815187692)
- [Thread continuation](https://mastodon.social/@pid_eins/114550373067181529)
- [Thread continuation](https://mastodon.social/@pid_eins/114550378175037063)
- [Thread continuation](https://mastodon.social/@pid_eins/114550396969650709)
- [Thread continuation](https://mastodon.social/@pid_eins/114550437912405150)
- [Thread continuation](https://mastodon.social/@pid_eins/114551047691172035)
- [Thread continuation](https://mastodon.social/@pid_eins/114551053058613762)
- [Thread continuation](https://mastodon.social/@pid_eins/114551064813852510)
- [Thread continuation](https://mastodon.social/@pid_eins/114573149204838605)
