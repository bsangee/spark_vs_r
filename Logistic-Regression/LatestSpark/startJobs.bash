#!/bin/bash
gnome-terminal -e "bash -c \"
/usr/bin/time -v spark-submit Wide/2008/logistic_regression-wide.py > results.txt;
/usr/bin/time -v spark-submit Wide/00-08/logistic_regression-wide.py > results.txt;
/usr/bin/time -v spark-submit Wide/95-08/logistic_regression-wide.py > results.txt;
/usr/bin/time -v spark-submit Narrow/2008/logistic_regression-narrow.py > results.txt;
/usr/bin/time -v spark-submit Narrow/00-08/logistic_regression-narrow.py > results.txt;
/usr/bin/time -v spark-submit Narrow/95-08/logistic_regression-narrow.py > results.txt;
 exec bash\""
