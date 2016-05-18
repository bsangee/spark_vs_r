#!/bin/bash
/usr/bin/time -v spark-submit Wide/2008/summary_stats.py > Wide/2008/results_aws_bd.txt;
/usr/bin/time -v spark-submit Narrow/2008/summary_stats.py > Narrow/2008/results_aws_bd.txt;

