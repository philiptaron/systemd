---
layout: post
title: "systemd 258 Feature Highlight #53"
date: 2025-09-12
source: https://mastodon.social/@pid_eins/115190035839444683
author: Lennart Poettering
---

5️⃣3️⃣ Here's the 53rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

This is a short one, but a double feature, both about systemd's service credentials concept:

Firstly, encrypted credentials finally work fine now if you use LoadCredentialEncrypted= in a per-user unit. v257 added the concept of user-scoped encrypted credentials, but by mistake I didn't actually hook this up with LoadCredentialEncrypted=. This is addressed now.

## Thread Continuation

*2025-09-12* ([source](https://mastodon.social/@pid_eins/115190067461100585))

And the other one, credentials now are supported for .mount units too. Or in other words, if you have some network mount, that shall be managed by a .mount unit, you can pass the username/password as credentials to them, via the usual LoadCredential=/LoadCredentialEncrypted=/ImportCredential=/SetCredential=/SetCredentialEncrypted= settings. And remember: you can inherit credentials from the host into VMs and containers, and from there into units. Which is really nice to securely pass…

*2025-09-12* ([source](https://mastodon.social/@pid_eins/115190068591259249))

…network share creds down into a system you invoke.

*2025-09-12* ([source](https://mastodon.social/@pid_eins/115190153364423280))

[@IncredibleLaser](https://troet.cafe/@IncredibleLaser) yeah, the secrets are then bound to your uid, your user name, your system and your OS, and can only be unlocked if all that checks out. This should protect you nicely from offline attacks, and yes you can store the secrets in a untrusted place without risking their security.

*2025-09-12* ([source](https://mastodon.social/@pid_eins/115190174673276700))

[@IncredibleLaser](https://troet.cafe/@IncredibleLaser) yes

## Q&A

> **[@pid_eins](https://mastodon.social/@pid_eins/115190057819657025):** So what does that mean? You can now do "systemd-cred encrypt --user myplaintext.txt ~/.config/credstore/mysecret" as regular user, to encrypt some secret with the TPM, bound to your UID. And then you can do "systemd-run --user -p LoadCredentialEncrypted=mysecret mycommand …" to invoke some command as a per-user service, that gets the secret passed unlocked via the usual $CREDENTIALS_DIRECTORY protocol.

And the other one, credentials now are supported for .mount units too. Or in other words, if you have some network mount, that shall be managed by a .mount unit, you can pass the username/password as credentials to them, via the usual LoadCredential=/LoadCredentialEncrypted=/ImportCredential=/SetCredential=/SetCredentialEncrypted= settings. And remember: you can inherit credentials from the host into VMs and containers, and from there into units. Which is really nice to securely pass…

## Sources

- [Original post](https://mastodon.social/@pid_eins/115190035839444683)
- [Thread continuation](https://mastodon.social/@pid_eins/115190067461100585)
- [Thread continuation](https://mastodon.social/@pid_eins/115190068591259249)
- [Thread continuation](https://mastodon.social/@pid_eins/115190153364423280)
- [Thread continuation](https://mastodon.social/@pid_eins/115190174673276700)
