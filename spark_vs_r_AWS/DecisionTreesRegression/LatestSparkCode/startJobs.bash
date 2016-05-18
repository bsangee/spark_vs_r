#!/bin/bash
/usr/bin/time -v spark-submit Wide/2008/decision_tree_regression.py > Wide/2008/results.txt;
/usr/bin/time -v spark-submit Wide/00-08/decision_tree_regression.py > Wide/00-08/results.txt;
/usr/bin/time -v spark-submit Wide/95-08/decision_tree_regression.py > Wide/95-08/results.txt;
/usr/bin/time -v spark-submit Narrow/2008/decision_tree_regression.py > Narrow/2008/results.txt;
/usr/bin/time -v spark-submit Narrow/00-08/decision_tree_regression.py > Narrow/00-08/results.txt;
/usr/bin/time -v spark-submit Narrow/95-08/decision_tree_regression.py > Narrow/95-08/results.txt;
