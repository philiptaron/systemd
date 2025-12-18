# v259 Feature Highlight #3

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins)
**Posted:** 2025-11-20 07:38 UTC
**Original:** [https://mastodon.social/@pid_eins/115580882123596509](https://mastodon.social/@pid_eins/115580882123596509)

---

3️⃣ Here's the 3rd post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

This one is quick and closely related to what I discussed in the previous installment:

There's now a new verb "dlopen-metadata" in systemd-analyze that extracts the dlopen() metadata from an ELF file and displays it in tabular form.


---

## Thread Continuation

### [2025-11-20 07:39 UTC](https://mastodon.social/@pid_eins/115580885939157356)

As an example, here's how its output looks like for libsystemd-shared-259.so, i.e. the shared library that contains much of systemd's code that is shared between all its many binaries:

https://paste.centos.org/view/raw/95455033

And that's is already.

### [2025-11-20 12:22 UTC](https://mastodon.social/@pid_eins/115582001009920722)

[@pemensik](https://fosstodon.org/@pemensik) well, it's more complex that that. libsystemd.so itself mostly has deps on compression libs, and those are needed by the journal code. And the journal code only needs the compression libs if you actually have journal files with fields compressed with them. In most cases all your files will only have the same compression alg used, because journald allows you to pick only one when generating them.

### [2025-11-20 12:23 UTC](https://mastodon.social/@pid_eins/115582004623227296)

[@pemensik](https://fosstodon.org/@pemensik) Hence, it doesn't depend so much purely on the tool calling into the lib, but on the files you process with the lib.

It's a bit like with gstreamer or so, where you try to play a video file and don't have the codec around. You get a soft failure too, not a hard one, and this requirement for all codecs is not ever expressed in rpm.


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115580882123596509)*