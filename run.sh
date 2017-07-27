#!/bin/bash

run_benchmark() {
    (cd $1 && docker-compose build && docker-compose up -d)
    trap "(cd $1 && docker-compose down -v); exit" INT
    echo "Waiting 60 seconds for setup"
    sleep 60s
    pid="$(ps -aux | grep $4 | grep -v grep | grep -v main.py | awk '{ print $2}')"
    python loadgenerator/src/main.py --debug --$2 --$3 "$pid" "$5" 60 1000 > $6
    (cd $1 && docker-compose down -v)
    trap - INT
}

run_benchmark dockerfiles/prometheus prometheus domain /bin/prometheus prometheus_prometheus_volume out/prometheus_domain_1.out
run_benchmark dockerfiles/prometheus prometheus mask /bin/prometheus prometheus_prometheus_volume out/prometheus_mask_1.out
run_benchmark dockerfiles/prometheus prometheus length /bin/prometheus prometheus_prometheus_volume out/prometheus_length_1.out
run_benchmark dockerfiles/druid druid domain "io.druid.cli.Main" druid_druid_volume out/druid_domain_1.out
run_benchmark dockerfiles/druid druid mask "io.druid.cli.Main" druid_druid_volume out/druid_mask_1.out
run_benchmark dockerfiles/druid druid length "io.druid.cli.Main" druid_druid_volume out/druid_length_1.out
