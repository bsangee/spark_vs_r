#!/bin/bash
cd 2008 && /usr/bin/time -v spark-submit summary_stats.py > results.txt
#/usr/bin/time -v spark-submit ./00-08/summary_stats.py;
#/usr/bin/time -v spark-submit ./95-08/summary_stats.py;
