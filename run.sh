#!/bin/bash
#sh benchmark.sh dockerfiles/prometheus prometheus domain /bin/prometheus prometheus_prometheus_volume out/prometheus_domain_1.out
#sh benchmark.sh dockerfiles/prometheus prometheus mask /bin/prometheus prometheus_prometheus_volume out/prometheus_mask_1.out
#sh benchmark.sh dockerfiles/prometheus prometheus length /bin/prometheus prometheus_prometheus_volume out/prometheus_length_1.out
#sh benchmark.sh dockerfiles/druid druid domain "io.druid.cli.Main" druid_druid_volume out/druid_domain_1.out
#sh benchmark.sh dockerfiles/druid druid mask "io.druid.cli.Main" druid_druid_volume out/druid_mask_1.out
#sh benchmark.sh dockerfiles/druid druid length "io.druid.cli.Main" druid_druid_volume out/druid_length_1.out
#sh benchmark.sh dockerfiles/clickhouse clickhouse domain clickhouse-server clickhouse_clickhouse_volume out/clickhouse_domain_1.out
#sh benchmark.sh dockerfiles/clickhouse clickhouse mask clickhouse-server clickhouse_clickhouse_volume out/clickhouse_mask_1.out
#sh benchmark.sh dockerfiles/clickhouse clickhouse length clickhouse-server clickhouse_clickhouse_volume out/clickhouse_length_1.out
#sh benchmark.sh dockerfiles/influxdb influxdb domain influxd influxdb_influxdb_volume out/influxdb_domain_1.out
#sh benchmark.sh dockerfiles/influxdb influxdb mask influxd influxdb_influxdb_volume out/influxdb_mask_1.out
#sh benchmark.sh dockerfiles/influxdb influxdb length influxd influxdb_influxdb_volume out/influxdb_length_1.out
#sh benchmark.sh dockerfiles/elasticsearch elasticsearch domain elasticsearch elasticsearch_elasticsearch_volume out/elasticsearch_domain_1.out
#sh benchmark.sh dockerfiles/elasticsearch elasticsearch mask elasticsearch elasticsearch_elasticsearch_volume out/elasticsearch_mask_1.out
#sh benchmark.sh dockerfiles/elasticsearch elasticsearch length elasticsearch elasticsearch_elasticsearch_volume out/elasticsearch_length_1.out
sh benchmark.sh dockerfiles/opentsdb opentsdb domain "net.opentsdb.tools.TSDMain|hbase.master.HMaster" opentsdb_opentsdb_volume out/opentsdb_domain_1.out
