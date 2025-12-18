---
layout: post
title: "SSH over AF_VSOCK"
date: 2025-07-10
---

31️⃣ Here's the 31st post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In v256 we added `systemd-ssh-generator`, which – among other things – would bind sshd to an `AF_VSOCK` socket if that is supported on the system, i.e. if booted inside a VMM that supports `AF_VSOCK` communication.
It greatly simplifies talking to a VM from the host, in environments that support this.

Except, of course, it's not quite as easy as it might appear conceptually:

In order to be able to connect to such a VM via `ssh-over-AF_VSOCK` one needs to know the VM's address, i.e. the `AF_VSOCK` "CID".
That's some 32-bit value that basically plays the role of an IP address, except for `AF_VSOCK` rather than `AF_INET`.

How do you actually figure out the CID of your VM though?
That's a really good question.
The `systemd-ssh-generator` tool actually logs it during early boot, but that typically has long scrolled away once the system is booted up.

It's also part of the `hostnamectl` status output that shows basic information about the host.
But you'll only get to that once you logged in.

Wouldn't it be great if the system would actually show it prominently on the console once it booted up, so that you can immediately see it when the system is ready to take your connections?

Precisely that has been implemented in v258.
The `.socket` units that bind `AF_VSOCK` will now call a tiny new tool `systemd-ssh-issue` that will generate…

…a drop-in file `/run/issue.d/50-ssh-vsock.issue` that contains one brief sentence with the command line to use to connect to the VM, including the `CID`.

The files in `/run/issue.d/*.issue` are shown by the `login` process that is responsible on Linux to show the login prompt.
Or in other words: when you get the console login prompt on a VM system you'll now also get a suggestion how to log into it via `ssh-over-AF_VSOCK` as an alternative means.

Note that this line is only shown if all of the below apply:

* the system runs in a VM
* `AF_VSOCK` is available
* `sshd` is installed
* And `sshd` actually has been successfully bound to an `AF_VSOCK` socket.

In the longer run we intend to make it possible to log into our VMs via `AF_VSOCK` already by VM name (rather than cryptic `CID`), but that's not quite feasible yet, because of various privilege issues.

---

## Q&A

> **[@matttbe](https://fosstodon.org/@matttbe)** Thanks! Talking about SSH and VSOCK: this v258 also adds scp and rsync support by using the % separator instead of /, e.g. `scp /etc/machine-id vsock%2222:.`

This is correct.
v258 extends SSH capabilities to support scp and rsync over VSOCK using a percent separator.
See the pull requests for details.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114827645185448224) (2025-07-10)
- [ssh-proxy: add scp and rsync support](https://github.com/systemd/systemd/pull/37035)
- [Additional related PR](https://github.com/systemd/systemd/pull/37191)
