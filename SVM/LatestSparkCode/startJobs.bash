#!/bin/bash
/usr/bin/time -v spark-submit Wide/2008/SVM.py > Wide/2008/results.txt;
/usr/bin/time -v spark-submit Wide/00-08/SVM.py > Wide/2008/results.txt;
/usr/bin/time -v spark-submit Wide/95-08/SVM.py > Wide/2008/results.txt;
/usr/bin/time -v spark-submit Narrow/2008/SVM.py > Narrow/2008/results.txt;
/usr/bin/time -v spark-submit Narrow/00-08/SVM.py > Narrow/2008/results.txt;
/usr/bin/time -v spark-submit Narrow/95-08/SVM.py > Narrow/2008/results.txt;
