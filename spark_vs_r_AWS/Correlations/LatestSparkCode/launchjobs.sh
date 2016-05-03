#!/bin/bash
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/2008/correlations-narrow.py > Narrow/2008/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/00-08/correlations-narrow.py  > Narrow/00-08/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/95-08/correlations-narrow.py  > Narrow/95-08/results_aws.txt;

