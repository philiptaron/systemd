# v259 Feature Highlight #1

**Author:** [Lennart Poettering](https://mastodon.social/@pid_eins)
**Posted:** 2025-11-18 09:55 UTC
**Original:** [https://mastodon.social/@pid_eins/115570095861864513](https://mastodon.social/@pid_eins/115570095861864513)

---

It's that time again! The systemd v259 release is coming closer. Let's restart the "what's new" series of posts for this iteration! Hence:

1️⃣ Here's the 1st post highlighting key new features of the upcoming v259 release of systemd. [#systemd259](https://mastodon.social/tags/systemd259) [#systemd](https://mastodon.social/tags/systemd)

For many usecases it's quite useful if local services can register additional hostnames for local resolution. For example, container and VMMs might want to register the IPs of locally running containers or VMs via a hostname, so that you can…


---

## Thread Continuation

### [2025-11-18 09:57 UTC](https://mastodon.social/@pid_eins/115570106480137615)

…access them by name rather than by address.

With v259 we are making this easy: there's now a "hook" interface in systemd-resolved: any privileged local daemon may bind an AF_UNIX socket in /run/systemd/resolve.hook/, and implement a simple Varlink IPC interface on it. If they do so, systemd-resolved will query it for every single local name resolution request, and they can answer positively, negatively, or let the resolution request be processed by the usual DNS based logic.

### [2025-11-18 10:00 UTC](https://mastodon.social/@pid_eins/115570114780614916)

If multiple hook services are in place, they are always queried in parallel, to reduce latencies (but if multiple return positively the service with the alphabetically first socket path wins). 

In systemd there are now two services which bind sockets there by default:

First of all systemd-machined makes all local containers/VMs that registered their IP addresses with it resolvable.

Secondly, systemd-networkd makes all hosts resolvable for which its internal DHCP server handed out leases.

### [2025-11-18 10:02 UTC](https://mastodon.social/@pid_eins/115570123490469021)

You might wonder: how does this relate to nss-mymachines? That NSS plugin did something very similar to the systemd-machined logic implemented now, however, it has one problem: it operates strictly and exclusively on the NSS level, but many programs nowadays bypass that and talk DNS directly with the configured servers. Since systemd-resolved registers itself as local DNS server in /etc/resolv.conf it means the new hook logic works for all types of lookups, regardless if they come via NSS, …

### [2025-11-18 10:04 UTC](https://mastodon.social/@pid_eins/115570133773288880)

…, D-Bus, Varlink or the local DNS stub. I think in the longer run we should deprecate nss-mymachines.

You might also wonder: sending every single lookup to all hooks might be quite expensive! As it turns out, the Varlink protocol spoken on the hook services is a bit smarter: it allows the hook service to install a filter on the requests it wants: restrict the hook to certain domains, or limits on the number of labels in the lookup.

Note that this API is public, i.e. any service can register…

### [2025-11-18 10:05 UTC](https://mastodon.social/@pid_eins/115570135360256019)

…names this way, not just systemd-machined and systemd-networkd.

And that's it for the first episode.

### [2025-11-18 10:24 UTC](https://mastodon.social/@pid_eins/115570209255259046)

[@arianvp](https://functional.cafe/@arianvp) not following. I never understood your nscd usecase. Given that nscd is obsolete and glibc timeouts for it are extremly short (and followed by local fallback) it seems entirely pointless to ever use nscd.

Note this new hook stuff allows you to plug something *behind* the 4 APIs resolved accepts resolution requests on (NSS, D-Bus, Varlink, DNS_STUB). Not sure what NixOS thinks it needs to plug in there?

### [2025-11-18 10:44 UTC](https://mastodon.social/@pid_eins/115570290314839897)

[@arianvp](https://functional.cafe/@arianvp) well, i don't get it. how do you get your requests from NSS to resolved if you are allergic to use nss-resolve? you can use the DNS stub of course, but I'd not recommend that, since a lot of metadata gets lost along the way, and search domain logic then must be client side.

### [2025-11-18 11:04 UTC](https://mastodon.social/@pid_eins/115570368944800105)

[@arianvp](https://functional.cafe/@arianvp) ah, ok, if you are ok with nss-resolve/nss-systemd then things are good, indeed.

### [2025-11-18 10:41 UTC](https://mastodon.social/@pid_eins/115570277616816846)

[@funkylab](https://mastodon.social/@funkylab) well, there might be conflicting records from different hook services. I wanted to give people a way to define an order of preference for that, simply by picking a different name.

The hook concept is quite powerful, it could not just be used for making additional names resolveable, it also canbe used to make certtain names unresolvable (i.e. something like a name-level firewall). But if you have both kinds in the mix it's essential you can run the firewall-style stuff before the other

### [2025-11-18 10:39 UTC](https://mastodon.social/@pid_eins/115570269723061364)

[@funkylab](https://mastodon.social/@funkylab) yes, we need to wait for the alphabetically first service. we apply a timeout as well though, hence this should be quite robust, if hook services misbehave. And there's a ratelimit: if services fail too often, we don't ping them anymore for  a while.

### [2025-11-18 11:09 UTC](https://mastodon.social/@pid_eins/115570386011429187)

[@pemensik](https://fosstodon.org/@pemensik) we already have a concept of "delegate" domains in resolved since v258, i.e. you can define domains that shall be forwarded to specific DNS servers. But that's a different usecase, as that's a DNS level thing.

Thew new hook stuff sits very early in the pipeline, and allows much more powerful filtering, also covering reasonable resolution of single label names (i.e. have a container called "foobar" actually be resolveable as "foobar") and blocking of names (i.e. inhibit resolution…

### [2025-11-18 11:09 UTC](https://mastodon.social/@pid_eins/115570387262037650)

[@pemensik](https://fosstodon.org/@pemensik) …of certain names before they reach IP networking).


---

*Source: [Mastodon](https://mastodon.social/@pid_eins/115570095861864513)*