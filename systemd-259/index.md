---
layout: default
title: systemd v259
---

**Released:** December 17, 2025

systemd v259 brings significant changes including deprecation of System V service scripts, new dlopen()-based weak dependencies, TPM2 NvPCRs for verified boot, and experimental musl libc support.

## Release Notes

- [Full Release Notes](release-notes.md)

## Commentary

Feature highlights from [Lennart Poettering](https://mastodon.social/@pid_eins):

1. [systemd-resolved hook interface](posts/01-resolved-hooks.md)
2. [dlopen() weak dependencies](posts/02-dlopen-dependencies.md)
3. [systemd-analyze dlopen-metadata](posts/03-dlopen-metadata.md)
4. [run0 --empower](posts/04-run0-empower.md)
5. [systemd-vmspawn --bind-user=](posts/05-vmspawn-bind-user.md)
6. [musl libc support](posts/06-musl-libc.md)
7. [systemd-repart size calculation](posts/07-repart-size-calc.md)
8. [modules-load.d parallelization](posts/08-modules-load-parallel.md)
9. [TPM and verified boot](posts/09-tpm-verified-boot.md)
10. [systemd-analyze nvpcrs](posts/10-analyze-nvpcrs.md)
11. [Varlink IPC for systemd-repart](posts/11-repart-varlink.md)
12. [systemd-vmspawn disk integration](posts/12-vmspawn-disk.md)
13. [--defer-partitions switches](posts/13-defer-partitions.md)
