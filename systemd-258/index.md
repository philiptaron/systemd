---
layout: default
title: systemd v258
---

**Released:** September 17, 2025

systemd v258 brings major changes including the removal of cgroup v1 support, factory reset functionality, enhanced boot debugging, and numerous improvements to containers, credentials, and sandboxing.

## Release Notes

- [Full Release Notes](release-notes.md)

## Commentary

Feature highlights from [Lennart Poettering](https://mastodon.social/@pid_eins):

1. [systemctl start verbose](posts/01-systemctl-verbose.md)
2. [systemd-homed areas](posts/02-homed-areas.md)
3. [systemd-resolved delegate zones](posts/03-resolved-delegate.md)
4. [Unprivileged containers with userns](posts/04-credentials.md)
5. [Hostname pattern matching](posts/05-hostname-pattern.md)
6. [/tmp/ security hardening](posts/06-tmp-security.md)
7. [Service workload management](posts/07-service-workload.md)
8. [ConditionHost matching enhancements](posts/08-condition-host.md)
9. [Terminal context sequences](posts/09-terminal-context.md)
10. [HTTP boot with systemd-boot](posts/10-http-boot.md)
11. [Boot debug breakpoints](posts/11-boot-debug.md)
12. [Factory reset support](posts/12-factory-reset.md)
13. [DNS monitoring and subscriptions](posts/13-dns-monitoring.md)
14. [Stub credentials and boot entries](posts/14-stub-credentials.md)
15. [UKI addons support](posts/15-uki-addons.md)
16. [userdb aliases](posts/16-userdb-aliases.md)
17. [File system integrity checks](posts/17-integrity-checks.md)
18. [TPM policy signing](posts/18-tpm-signing.md)
19. [PAM service prompts](posts/19-pam-prompts.md)
20. [Graceful mount options](posts/20-mount-options.md)
21. [userdb drop-in directories](posts/21-userdb-dropins.md)
22. [systemd-repart image growth](posts/22-repart-grow.md)
23. [Terminal feature negotiation](posts/23-terminal-features.md)
24. [systemd-nspawn notify socket](posts/24-nspawn-notify.md)
25. [systemd-nspawn hotkeys](posts/25-nspawn-hotkeys.md)
26. [ExecStart pipe flag](posts/26-execstart-pipe.md)
27. [systemd-confext immutable config](posts/27-confext-immutable.md)
28. [userdb filtering improvements](posts/28-userdb-filter.md)
29. [Service disk quotas](posts/29-sandboxing-quotas.md)
30. [Service sandbox debugging](posts/30-unit-shell.md)
31. [SSH over AF_VSOCK](posts/31-ssh-vsock.md)
32. [systemd-repart fs-verity](posts/32-repart-fsverity.md)
33. [Socket credentials](posts/33-socket-credentials.md)
34. [systemd-firstboot completion](posts/34-firstboot-complete.md)
35. [Stateless booting via rd.systemd.pull](posts/35-pull-stateless.md)
36. [Kernel module conditions](posts/36-modprobe-conditions.md)
37. [CHID lookup tool](posts/37-chid-lookup.md)
38. [systemd-homed signing keys](posts/38-homed-signing.md)
39. [DDI partition filtering](posts/39-ddi-filter.md)
40. [Android USB debugging](posts/40-android-usb.md)
41. [vmspawn SMBIOS Type 11](posts/41-vmspawn-smbios.md)
42. [PID file descriptor identifiers](posts/42-pidfd-identifiers.md)
43. [RestartMode=debug](posts/43-restart-debug.md)
44. [UKI HTTP boot](posts/44-uki-http-boot.md)
45. [cgroupv1 removal](posts/45-cgroupv1-removal.md)
46. [Protect hostname sandbox](posts/46-protect-hostname.md)
47. [homectl adopt and register](posts/47-homectl-adopt.md)
48. [systemd-machined Varlink APIs](posts/48-machined-varlink.md)
49. [Soft-reboot and sockets](posts/49-soft-reboot-sockets.md)
50. [User namespaces and cgroups](posts/50-user-namespaces.md)
51. [Varlink password agent](posts/51-varlink-passwords.md)
52. [PrivateUsers sandboxing](posts/52-privateusers.md)
53. [User credentials and mount units](posts/53-service-credentials.md)
54. [DDI designators](posts/54-ddi-designators.md)
55. [eBPF delegation](posts/55-ebpf-delegation.md)
