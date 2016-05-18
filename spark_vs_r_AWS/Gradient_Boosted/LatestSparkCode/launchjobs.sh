#!/bin/bash
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/2008/gradient_boosted_classification.py >> Narrow/2008/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/00-08/gradient_boosted_classification.py  >> Narrow/00-08/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Narrow/95-08/gradient_boosted_classification.py  >> Narrow/95-08/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Wide/2008/gradient_boosted_classification.py >> Wide/2008/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Wide/00-08/gradient_boosted_classification.py  >> Wide/00-08/results_aws.txt;
/usr/bin/time -v spark-submit --executor-cores 16 --executor-memory 20G --driver-cores 16 Wide/95-08/gradient_boosted_classification.py  >> Wide/95-08/results_aws.txt;

