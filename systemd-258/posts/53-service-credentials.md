---
layout: post
title: "User credentials and mount units"
date: 2025-09-12
---

This is a short one, but a double feature, both about systemd's service credentials concept:

Firstly, encrypted credentials finally work fine now if you use `LoadCredentialEncrypted=` in a per-user unit. v257 added the concept of user-scoped encrypted credentials, but by mistake this wasn't actually hooked up with `LoadCredentialEncrypted=`. This is addressed now.

You can now do `systemd-cred encrypt --user myplaintext.txt ~/.config/credstore/mysecret` as a regular user to encrypt some secret with the TPM, bound to your UID. Then you can do `systemd-run --user -p LoadCredentialEncrypted=mysecret mycommand` to invoke some command as a per-user service, that gets the secret passed unlocked via the usual `$CREDENTIALS_DIRECTORY` protocol.

The secrets are then bound to your UID, your user name, your system and your OS, and can only be unlocked if all that checks out. This protects you nicely from offline attacks, and you can store the secrets in an untrusted place without risking their security.

Secondly, credentials are now supported for `.mount` units too. If you have some network mount that shall be managed by a `.mount` unit, you can pass the username/password as credentials to them via the usual `LoadCredential=`, `LoadCredentialEncrypted=`, `ImportCredential=`, `SetCredential=`, and `SetCredentialEncrypted=` settings. Remember that you can inherit credentials from the host into VMs and containers, and from there into units, which is really nice to securely pass network share credentials down into a system you invoke.

---

## Q&A

> **@IncredibleLaser** Are the credentials only for protecting at-rest secrets or also for in-transit usage?

Yeah, the secrets are then bound to your UID, your user name, your system and your OS, and can only be unlocked if all that checks out. This should protect you nicely from offline attacks, and yes you can store the secrets in an untrusted place without risking their security.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115190035839444683) (2025-09-12)
