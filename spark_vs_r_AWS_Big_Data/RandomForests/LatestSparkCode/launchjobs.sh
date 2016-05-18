#!/bin/bash
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/2008/random_forests.py >> Narrow/2008/results_aws_bd.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Wide/2008/random_forests.py >> Wide/2008/results_aws_bd.txt;

