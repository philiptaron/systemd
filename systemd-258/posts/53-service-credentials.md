---
layout: post
title: "Service credentials double feature"
date: 2025-09-12
---

It's that time again!
The systemd v258 release is coming closer.
Let's continue the "what's new" series of posts for this iteration!
Hence:

53 Here's the 53rd post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

This is a short one, but a double feature, both about systemd's service credentials concept:

Firstly, encrypted credentials finally work fine now if you use `LoadCredentialEncrypted=` in a per-user unit.
v257 added the concept of user-scoped encrypted credentials, but by mistake I didn't actually hook this up with `LoadCredentialEncrypted=`.
This is addressed now.

So what does that mean?
You can now do `systemd-cred encrypt --user myplaintext.txt ~/.config/credstore/mysecret` as regular user, to encrypt some secret with the TPM, bound to your UID.
And then you can do `systemd-run --user -p LoadCredentialEncrypted=mysecret mycommand …` to invoke some command as a per-user service, that gets the secret passed unlocked via the usual `$CREDENTIALS_DIRECTORY` protocol.

And the other one, credentials now are supported for .mount units too.
Or in other words, if you have some network mount, that shall be managed by a .mount unit, you can pass the username/password as credentials to them, via the usual `LoadCredential=`/`LoadCredentialEncrypted=`/`ImportCredential=`/`SetCredential=`/`SetCredentialEncrypted=` settings.
And remember: you can inherit credentials from the host into VMs and containers, and from there into units.
Which is really nice to securely pass network share creds down into a system you invoke.

---

> **[@IncredibleLaser](https://troet.cafe/@IncredibleLaser)** systemd's abilities to manage secrets has been a major boon for me. However I don't exactly understand this particular thing. What is the security you gain from this? Protection against offline attacks? Or is this to put the encrypted credentials somewhere else, like a repository?

Yeah, the secrets are then bound to your uid, your user name, your system and your OS, and can only be unlocked if all that checks out.
This should protect you nicely from offline attacks, and yes you can store the secrets in a untrusted place without risking their security.

> **[@IncredibleLaser](https://troet.cafe/@IncredibleLaser)** [Follow-up question]

Yes

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/115190035839444683) (2025-09-12)
