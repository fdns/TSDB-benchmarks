#!/bin/bash
(cd $1 && docker-compose build && docker-compose up -d)
trap "(cd $1 && docker-compose down -v); exit" INT
echo "Waiting 60 seconds for setup"
sleep 60s
pid="$(ps -aux | grep $4 | grep -v grep | grep -v benchmark.sh | grep -v main.py | awk '{ print $2}')"
python loadgenerator/src/main.py --$2 --$3 "$pid" "$5" 1 1000 > $6
(cd $1 && docker-compose down -v)
trap - INT
