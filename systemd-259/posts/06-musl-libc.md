---
layout: post
title: "musl libc support"
date: 2025-11-25
---

6️⃣ Here's the 6th post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

Here's a short one: systemd v259 will compile fine with musl libc, out of the box.

Sounds great?
Well, it's not as great as it might sound to some. musl has quite some limitations compared to glibc: the primary one is that there's no Name Service Switch (NSS) support.
That's the subsystem that allows systemd to make domain names, user names, groups names resolvable via `gethostbyname()`, `getaddrinfo()`, `getpwnam()`, `getgrnam()` and similar calls.

And that in turn is used to make a good chunk of systemd's infrastructure work, for example `DynamicUser=1`, [`systemd-resolved`][systemd-resolved], [`systemd-homed`][systemd-homed], [`systemd-userdbd`][systemd-userdbd], [`systemd-nsresourced`][systemd-nsresourced], [`nss-myhostname`][nss-myhostname], and so on.
Hence, if you don't have NSS then all that is gone or half-broken.

And there are other limitations: systemd will react to memory pressure by releasing memory that libc has acquired from the kernel but is no longer using back to the kernel.
It's an essential feature that makes things work on low-memory systems.
But musl has no concept for this, hence the memory pressure operation is a NOP there...

And then of course, musl upstream is what one might describe as hostile towards systemd, and that alone is a good reason to not recommend its use for me.

Hence, make of this what you want.
But my recommendation continues to be: just use glibc, the pain and limitations musl brings are really not worth it. glibc has NSS, glibc has `malloc_trim()`, doesn't need tons of polyfills, and most of all glibc upstream folks are good to work with.

---

> **[@TheDragon](https://hachyderm.io/@TheDragon)** Kinda curious, given the major drawbacks of using these two together + the hostility.. why has this support even been added?

postmarketOS made the fateful decision to adopt musl, and now they are stuck with it.
We like the pmos people.

But a lot of other people asked for it too.

> **[@Atemu](https://darmstadt.social/@Atemu)** Does musl's malloc even have the behaviour that glibc's does where it doesn't actually return `free()`'d memory to the kernel?
> Because if not it'd be quite sensible for that to be a no-op.

Well, that would mean they ask the kernel for memory piecemeal for every single page they need.
And return each page that is empty back to the kernel immediately.
Which is formally correct of course but also prohibitively slow because memory mappings flush TLBs and stuff.
So malloc implementations generally allocate memory in larger chunks to make things fast.
But if you do that you should really have a way to return unused pages of a chunk to the kernel under pressure.
Glibc has that.

> **[@valpackett](https://social.treehouse.systems/@valpackett)** I've heard that `malloc_trim()` only makes sense with glibc's old-fashioned heavily-`sbrk()`-using allocator, and not at all with fully `mmap()` based allocators.
> Is that not true?!
> Does `malloc_trim()` actually do something with `mmap()`ed memory?

glibc calls `madvise` `MADV_DONTNEED` on the space it doesn't need.

---

## References

[systemd-resolved]: https://www.freedesktop.org/software/systemd/man/259/systemd-resolved.html
[systemd-homed]: https://www.freedesktop.org/software/systemd/man/259/systemd-homed.html
[systemd-userdbd]: https://www.freedesktop.org/software/systemd/man/259/systemd-userdbd.html
[systemd-nsresourced]: https://www.freedesktop.org/software/systemd/man/259/systemd-nsresourced.html
[nss-myhostname]: https://www.freedesktop.org/software/systemd/man/259/nss-myhostname.html

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115611051983920298) (2025-11-25)
