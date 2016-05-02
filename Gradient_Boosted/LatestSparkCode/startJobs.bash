#!/bin/bash
/usr/bin/time -v spark-submit Wide/2008/gradient_boosted_classification.py > Wide/2008/results.txt;
/usr/bin/time -v spark-submit Wide/00-08/gradient_boosted_classification.py > Wide/00-08/results.txt;
/usr/bin/time -v spark-submit Wide/95-08/gradient_boosted_classification.py > Wide/95-08/results.txt;
/usr/bin/time -v spark-submit Narrow/2008/gradient_boosted_classification.py > Narrow/2008/results.txt;
/usr/bin/time -v spark-submit Narrow/00-08/gradient_boosted_classification.py > Narrow/00-08/results.txt;
/usr/bin/time -v spark-submit Narrow/95-08/gradient_boosted_classification.py > Narrow/95-08/results.txt;
