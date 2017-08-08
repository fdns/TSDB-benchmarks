#!/bin/bash

set -e

export TSD_CONF_tsd__http__cachedir=${TSD_CONF_tsd__http__cachedir:-/var/cache/opentsdb}
export TSD_CONF_tsd__http__staticroot=${TSD_CONF_tsd__http__staticroot:-/usr/share/opentsdb/static}

for VAR in $(env); do
    if [[ $VAR =~ ^TSD_CONF_ ]]; then
        tsd_conf_name=$(echo "$VAR" | sed -r 's/^TSD_CONF_([^=]*)=.*/\1/' | sed 's/__/./g' | tr '[:upper:]' '[:lower:]')
        tsd_conf_value=$(echo "$VAR" | sed -r "s/^[^=]*=(.*)/\1/")

        if grep "$tsd_conf_name" /etc/opentsdb/opentsdb.conf
        then
            # Replace conf value
            replaceString="/$tsd_conf_name/c\\$tsd_conf_name = $tsd_conf_value"
            sed -i "$replaceString" /etc/opentsdb/opentsdb.conf
        else
            # Add conf value
            echo "$tsd_conf_name = $tsd_conf_value" >> /etc/opentsdb/opentsdb.conf
        fi
        
    fi
done


# Feeding opentsdb metrics back to itself
if [ "${TSD_TELEMETRY_INTERVAL:-0}" != "0" ]; then
    TSD_BIND=${TSD_CONF_tsd__network__bind:-127.0.0.1}
    TSD_PORT=${TSD_CONF_tsd__network__port}
    TSD_HOST=${MESOS_TASK_ID:-$(hostname -s)}

    (while true; do
        sleep "${TSD_TELEMETRY_INTERVAL}"
        echo "$(date -u '+%F %T,000') INFO  DockerOwnMetrics: Writing own metrics"
        curl --max-time 2 -s "http://$TSD_BIND:$TSD_PORT/api/stats" | \
          sed -e "s#\"host\":\"[^\"]*\"#\"host\":\"$TSD_HOST\"#g" | \
          curl --max-time 2 -s -X POST -H "Content-type: application/json" "http://$TSD_BIND:$TSD_PORT/api/put" -d @-
    done) &
fi

mkdir -p "${TSD_CONF_tsd__http__cachedir}"

chown opentsdb "${TSD_CONF_tsd__http__cachedir}"
chown opentsdb /data/hbase

echo "Running supervisord"
exec supervisord -n -c /etc/supervisord.conf
