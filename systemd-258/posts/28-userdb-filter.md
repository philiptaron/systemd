---
layout: post
title: "userdb filtering improvements"
date: 2025-07-07
---

This is the 28th post highlighting key new features of the upcoming v258 release of systemd. [#systemd258](https://mastodon.social/tags/systemd258)

In two earlier episodes of this series about systemd v258 I already talked about `userdb`, the user database subsystem of systemd, that extends the classic POSIX user database (i.e. `getpwnam()` and friends) with more fields and nicer semantics, accessible via IPC.

There's one more thing I'd like to talk about that's new with `userdb` in v258:

## The Limitation

`userdb` inherits from the POSIX user database where the primary keys into the database are the numeric `UID` and the user name. The only operations for lookup you have on POSIX are via these two, or get a full dump (though implementing the full dump is kinda optional actually, various network backends don't implement that).

That's quite limiting however. For various operations it is useful to filter by other properties of the records. For example: query for users in a specific UID range.

Or look for users of certain designations (i.e. regular users only, or system users only, and so on). Or do a "fuzzy" user name search, where we allow users to make typos, and search various user name related fields (such as `GECOS` and so on).

## v257: Client-Side Filtering

Because that's useful, already in v257 we taught `userdbctl` (the command line tool for querying the db) to do just this kind of filtering. Back then it was done *client-side* only: if you ask for a lookup with one of those filters, and without specifying either UID nor user name, then internally this would be a wild dump, of which various entries are then suppressed, all on the client side.

## v258: Server-Side Filtering

With v258 we moved this to the IPC server side: the client can now specify these filter parameters too, in addition to username and UID, and the server can honour them, optimizing its own lookups, in particular when they go over the network. Operations that should be cheap can then be cheap all along the pipeline, instead of blowing up into a wild dump that needs to be transferred to the client before it can be filtered.

Note that compat is maintained: it's optional for a `userdb` provider to implement this kind of filtering: if it does, great! if it doesn't, also OK, as the client-side will then apply the filtering.

This means: the distinction in the place of implementation is abstracted away, and compatibility is retained. Backends that want to optimize this can, backends which don't, will continue to work just fine.

---

## Sources

- [Original thread](https://mastodon.social/@pid_eins/114812166113613377) (2025-07-07)
