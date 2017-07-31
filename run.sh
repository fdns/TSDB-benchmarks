#!/bin/bash
#sh benchmark.sh dockerfiles/prometheus prometheus domain /bin/prometheus prometheus_prometheus_volume out/prometheus_domain_1.out
#sh benchmark.sh dockerfiles/prometheus prometheus mask /bin/prometheus prometheus_prometheus_volume out/prometheus_mask_1.out
#sh benchmark.sh dockerfiles/prometheus prometheus length /bin/prometheus prometheus_prometheus_volume out/prometheus_length_1.out
#sh benchmark.sh dockerfiles/druid druid domain "io.druid.cli.Main" druid_druid_volume out/druid_domain_1.out
#sh benchmark.sh dockerfiles/druid druid mask "io.druid.cli.Main" druid_druid_volume out/druid_mask_1.out
#sh benchmark.sh dockerfiles/druid druid length "io.druid.cli.Main" druid_druid_volume out/druid_length_1.out
sh benchmark.sh dockerfiles/clickhouse clickhouse domain clickhouse-server clickhouse_clickhouse_volume out/clickhouse_domain_1.out
#sh benchmark.sh dockerfiles/clickhouse clickhouse mask clickhouse-server clickhouse_clickhouse_volume out/clickhouse_domain_1.out
#sh benchmark.sh dockerfiles/clickhouse clickhouse length clickhouse-server clickhouse_clickhouse_volume out/clickhouse_domain_1.out
