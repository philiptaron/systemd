---
layout: post
title: "musl libc support"
date: 2025-11-25
source: https://mastodon.social/@pid_eins/115611051983920298
---

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins) | **Posted:** 2025-11-25 15:30 UTC

---

6️⃣ Here's the 6th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

Here's a short one: systemd v259 will compile fine with musl libc, out of the box.

Sounds great? Well, it's not as great as it might sound to some. musl has quite some limitations compared to glibc: the primary one is that there's no Name Service Switch (NSS) support. That's the subsystem that allows systemd to make domain names, user names, groups names resolvable via…


---

## Thread Continuation

### [2025-11-25 15:36 UTC](https://mastodon.social/@pid_eins/115611075456548398)

…gethostbyname(), getaddrinfo(), getpwnam(), getgrnam() and similar calls.

And that in turn is used to make a good chunk of systemd's infrastructure work, for example DynamicUser=1, systemd-resolved, systemd-homed, systemd-userdbd, systemd-nsresoured, nss-myhostname, and so on. Hence, if you don't have NSS then all that is gone or half-broken.

And there are other limitations: systemd will react to memory pressure by releasing memory that libc has acquired from the kernel…

### [2025-11-25 15:40 UTC](https://mastodon.social/@pid_eins/115611091164759940)

…but is no longer using back to the kernel. It's an essential feature that makes things work on low-memory systems. But musl has no concept for this, hence the memory pressure operation is a NOP there...

And then of course, musl upstream is what one might describe as hostile towards systemd, and that alone is a good reason to not recommend its use for me.

### [2025-11-25 15:42 UTC](https://mastodon.social/@pid_eins/115611097144507058)

Hence, make of this what you want. But my recommendation continues to be: just use glibc, the pain and limitations musl brings are really not worth it. glibc has NSS, glibc has malloc_trim(), doesn't need tons of polyfills, and most of all glibc upstream folks are good to work with.

### [2025-11-25 19:37 UTC](https://mastodon.social/@pid_eins/115612020100596022)

[@TheDragon](https://hachyderm.io/@TheDragon) postmarketos made the fateful decision to adopt musl, and now they are stuck with it. We like the pmos people.

But a lot of other people asked for it too.

### [2025-11-25 19:45 UTC](https://mastodon.social/@pid_eins/115612051495433467)

[@Atemu](https://darmstadt.social/@Atemu) well, that would mean they ask the kernel for memory piecemeal for every single page they need. And return each page that is empty back to the kernel immediately. Which is formally correct of course but also prohibitively slow because memory mappings flush TLBs and stuff. So malloc implementations generally allocate memory in larger chunks to make things fast. But if you do that you should really have a way to return unused pages of a chunk to the kernel under pressure. Glibc has that.

### [2025-11-27 04:34 UTC](https://mastodon.social/@pid_eins/115619795923312909)

[@valpackett](https://social.treehouse.systems/@valpackett) [@Atemu](https://darmstadt.social/@Atemu) glibc calls madvise MADV_DONTNEED on the space it doesn't need.


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115611051983920298)*