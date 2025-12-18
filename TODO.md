# Mastodon Posts to Process

Lennart Poettering's v259 feature highlight posts from [@pid_eins@mastodon.social](https://mastodon.social/@pid_eins).

## Posts

- [x] [Post #1](https://mastodon.social/@pid_eins/115570095861864513) - systemd-resolved hook interface
- [x] [Post #2](https://mastodon.social/@pid_eins/115575271970490767) - dlopen() weak dependencies
- [x] [Post #3](https://mastodon.social/@pid_eins/115580882123596509) - systemd-analyze dlopen-metadata
- [x] [Post #4](https://mastodon.social/@pid_eins/115586469819973533) - run0 --empower
- [x] [Post #5](https://mastodon.social/@pid_eins/115605598751722319) - systemd-vmspawn --bind-user=
- [x] [Post #6](https://mastodon.social/@pid_eins/115611051983920298) - musl libc support
- [x] [Post #7](https://mastodon.social/@pid_eins/115614881738923176) - systemd-repart "-" argument
- [x] [Post #8](https://mastodon.social/@pid_eins/115620451885638963) - modules-load.d parallelization
- [x] [Post #9](https://mastodon.social/@pid_eins/115627835871078915) - TPM and verified boot
- [x] [Post #10](https://mastodon.social/@pid_eins/115646310576910417) - systemd-analyze nvpcrs
- [x] [Post #11](https://mastodon.social/@pid_eins/115662198906484836) - Varlink IPC for systemd-repart
- [x] [Post #12](https://mastodon.social/@pid_eins/115666147093865447) - systemd-vmspawn disk integration
- [x] [Post #13](https://mastodon.social/@pid_eins/115740831317295811) - --defer-partitions switches

## API Endpoints

For each post:
- Main post: `https://mastodon.social/api/v1/statuses/{id}`
- Thread context: `https://mastodon.social/api/v1/statuses/{id}/context`

## Notes

- Series may continue with more posts (v258 had 53+ posts)
- Re-run discovery by fetching recent statuses from account ID `109248059314089584`
- To check for new posts: `curl -s "https://mastodon.social/api/v1/accounts/109248059314089584/statuses?limit=40" | jq '.[] | select(.content | contains("v259")) | {id, created_at}'`
