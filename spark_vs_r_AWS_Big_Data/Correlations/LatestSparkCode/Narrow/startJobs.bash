#!/bin/bash
/usr/bin/time -v spark-submit 2008/correlations-wide.py;
/usr/bin/time -v spark-submit 00-08/correlations-wide.py;
/usr/bin/time -v spark-submit 95-08/correlations-wide.py;

