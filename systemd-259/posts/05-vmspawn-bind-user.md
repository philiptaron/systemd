---
layout: post
title: "systemd-vmspawn --bind-user="
date: 2025-11-24
source: https://mastodon.social/@pid_eins/115605598751722319
---

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins) | **Posted:** 2025-11-24 16:24 UTC

---

5️⃣ Here's the 5th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

One really fun feature of systemd-nspawn is the --bind-user= switch. If used it will make the specified user from the host (i.e. user record + $HOME) available inside the container. It's a really simple way to quickly get shared access to your home dir from host and container.

With v259 the same option is now available for systemd-vmspawn too. Or in other words, …


---

## Thread Continuation

### [2025-11-24 16:26 UTC](https://mastodon.social/@pid_eins/115605608397801533)

… one simple switch will propagate the user record into the VM (via system credentials), and make the home dir available too (via virtiofs).

This only works if the payload runs a reasonable recent systemd, as it makes use of systemd credentials and userdb.

And that's already it for today.

### [2025-11-24 16:30 UTC](https://mastodon.social/@pid_eins/115605624817762441)

(One more addendum, after all: if an SSH key is part of the host userdb record, then it will be propagated into the VM too, so that you can immediately SSH into the VM)

### [2025-11-25 15:46 UTC](https://mastodon.social/@pid_eins/115611113861579449)

[@jaminsamuel18](https://mastodon.social/@jaminsamuel18) yes there is. and it is being worked on right now.


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115605598751722319)*