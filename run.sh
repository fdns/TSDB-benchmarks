#!/bin/bash
#set -e
(cd tests/prometheus && docker-compose build && docker-compose up -d)
pid="$(ps -aux | grep prometheus | grep -v grep | grep -v main.py | awk '{ print $2}')"
echo "Waiting 1 minute for setup"
trap 'trap - INT' INT
sleep 10s
python loadgenerator/src/main.py --prometheus --domain "$pid" 'prometheus_prometheus_volume' 60 1000
(cd tests/prometheus && docker-compose down -v)
