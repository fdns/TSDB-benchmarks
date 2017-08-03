# OpenTSDB

I found many OpenTSDB docker containers through GitHub, each one with its custom features but none had all I want.
This one bundle OpenTSDB and HBase, with ability to change tsd service configuration from outside the container.
I based my work from 2 container definitions :

- https://github.com/cloudflare/docker-opentsdb (for the outside configuration)
- https://github.com/PeterGrace/opentsdb-docker (for OpenTSDB and HBase installation)

I also added rsyslog to enable advanced logging features (such as shipping to a remote server) and supervisor to "manage" services.

Current image embed OpenTSDB 2.3RC1 and HBase 1.2.2




