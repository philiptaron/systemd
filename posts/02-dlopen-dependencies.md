# v259 Feature Highlight #2

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins)
**Posted:** 2025-11-19 07:51 UTC
**Original:** [https://mastodon.social/@pid_eins/115575271970490767](https://mastodon.social/@pid_eins/115575271970490767)

---

No we don't, because years ago we devised a spec for embedded dlopen() based weak dependencies in ELF binaries. systemd binaries use that comprehensively for everything they dlopen(), to the point that libsystemd-shared.so now declares a whopping 26 of them. All relevant package managers have since been updated to read this metadata, hence in this regard we have not regressed.


---

## Thread Continuation

### [2025-11-19 07:55 UTC](https://mastodon.social/@pid_eins/115575286418872935)

Oh, and it's not just about footprint actually, it's also about security: by ensuring that dynamic libraries only get loaded when they are actually used, we make it harder for exploits such as the openssh/xz incident last year to take place, as compile time deps no longer translate to runtime deps 1:1, and thus awful concepts such as gcc constructors lose their negative impact a bit.

### [2025-11-19 08:02 UTC](https://mastodon.social/@pid_eins/115575314386754605)

And one last thing: what about those last two deps? i.e. openssl and libcrypt?

Yes, we have plans to turn those into dlopen() deps too. Hopefully in v260.

And once we achieve that things are going to be fun, because systemd will start to have a smaller minimal dep footprint than certain other "lightweight" init systems. For example, that dependency hog s6 is currently at 3 shared library deps beyond libc. So wasteful! And it doesn't even do a fraction of what systemd does...

### [2025-11-19 08:05 UTC](https://mastodon.social/@pid_eins/115575324853389716)

You might specifically wonder why we haven't turned the libcrypt dep into dlopen() yet, given it only exposes basically a single relevant function (a flavour of crypt()) and hence should be simple.

The only reason is that it's not quite *as* simple, because crypt() used to be part of glibc on Linux, and there are still systems around which do use it like that, hence we need some non-trivial ifdeffery to make that happen and keep things working in both scenarios, and so far we were too…

### [2025-11-19 08:05 UTC](https://mastodon.social/@pid_eins/115575325595738528)

…lazy for that.

And that's all for today.

### [2025-11-19 08:12 UTC](https://mastodon.social/@pid_eins/115575354959743193)

Or maybe let me add one more thing. systemd is of course not only the really fundamental package that makes up an OS image. There are various others you really need too. It would be fantastic of those adopted similar logic, so that container images for example never pull in libselinux anymore (which in turn pulls in libpcre and other stuff), or libaudit and so on, i.e. stuff that doesn't even do anything inside a container.

### [2025-11-19 15:02 UTC](https://mastodon.social/@pid_eins/115576965989010785)

[@ska](https://social.treehouse.systems/@ska) Hey, I am just trolling you…

### [2025-11-19 15:41 UTC](https://mastodon.social/@pid_eins/115577117761089722)

[@pemensik](https://fosstodon.org/@pemensik) it used to be split out a long time ago. it was a fricking nightmare of deps and came with so many restrictions, because ELF cannot distinguish between public APIs to everyone, and public APIs towards a certain set of of libraries. i.e. anything a library exports is *always* public for anyone, thus you can never provide a simple helper for your own higher level libraries only, you must *always* commit to it's ABI stability if you do.

Hence, sorry, fuck no. Never again.

### [2025-11-20 07:43 UTC](https://mastodon.social/@pid_eins/115580900779989425)

[@pemensik](https://fosstodon.org/@pemensik) static libs doesn't work for this. The main reason why systemd's size footprint is actually quite OK for everything it does, is primarily because we do not use static linking, and hence duplication of code in many ELF objects, but are pretty good and minimizing that and placing any shared code in a common object file.

And if you export something to the public you must keep ABI stable, no matter what.

### [2025-11-20 07:43 UTC](https://mastodon.social/@pid_eins/115580901119401195)

[@pemensik](https://fosstodon.org/@pemensik) 

rpm and dpkg extract the dlopen deps when building packages and turn them into Suggests/Recommends packaging deps.

### [2025-11-19 15:35 UTC](https://mastodon.social/@pid_eins/115577095794682751)

[@3v1n0](https://fosstodon.org/@3v1n0) [@pwithnall](https://mastodon.social/@pwithnall) [@ebassi](https://mastodon.social/@ebassi) Ah! it would be lovely if glib would do this too.

[@bluca](https://fosstodon.org/@bluca) wanted to move the spec into the uapi group anyway. maybe at the same time we could provide the relevant C macros as a drop-in .C file too, in some associated repo.

[@bluca](https://fosstodon.org/@bluca) hey, here's one more thing to put on your plate! ;-)


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115575271970490767)*