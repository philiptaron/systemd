---
layout: default
title: systemd Release Notes Commentary
---

This site provides annotated release notes for systemd, with additional commentary and explanations from Lennart Poettering's Mastodon posts.

## Releases

### [systemd v259](systemd-259/)

Released December 17, 2025.

Highlights include:
- [New resolve hooks for local DNS interception](systemd-259/posts/01-resolved-hooks.md)
- [dlopen() for shared library dependencies](systemd-259/posts/02-dlopen-dependencies.md)
- [run0 --empower for elevated privileges without root](systemd-259/posts/04-run0-empower.md)
- [TPM2 NvPCRs for verified boot](systemd-259/posts/09-tpm-verified-boot.md)
- [Experimental musl libc support](systemd-259/posts/06-musl-libc.md)

### [systemd v258](systemd-258/)

Released September 17, 2025.

Highlights include:
- [systemctl start -v for verbose output](systemd-258/posts/01-systemctl-verbose.md)
- [cgroup v1 support removed](systemd-258/posts/45-cgroupv1-removal.md)
- [Factory reset support](systemd-258/posts/12-factory-reset.md)
- [systemd-homed areas for multiple home directories](systemd-258/posts/02-homed-areas.md)
- [eBPF delegation to containers](systemd-258/posts/55-ebpf-delegation.md)

## About

The release notes are sourced from the [official systemd GitHub releases](https://github.com/systemd/systemd/releases). Commentary posts are compiled from [Lennart Poettering's Mastodon](https://mastodon.social/@pid_eins).

---

Maintained by [Philip Taron](https://github.com/philiptaron).
