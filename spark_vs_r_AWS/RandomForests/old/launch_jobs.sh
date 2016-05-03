cd /home/faiz89/Desktop/Eastman/git/spark_vs_r/RandomForests/Spark-RF-Narrow

/home/faiz89/Desktop/Spark/spark/bin/spark-submit random_forests_narrow.py /home/faiz89/Desktop/Eastman/2008.csv > RF_narrow_run1_singleNode_2008.txt
if [ $? -eq 0 ]; then
	/home/faiz89/Desktop/Spark/spark/bin/spark-submit random_forests_narrow.py /home/faiz89/Desktop/Eastman/00-08.csv > RF_narrow_run1_singleNode_00-08.txt
fi
if [ $? -eq 0 ]; then
	/home/faiz89/Desktop/Spark/spark/bin/spark-submit random_forests_narrow.py /home/faiz89/Desktop/Eastman/95-08.csv > RF_narrow_run1_singleNode_95-08.txt
fi

cd /home/faiz89/Desktop/Eastman/git/spark_vs_r/RandomForests/Spark-RF-Wide
if [ $? -eq 0 ]; then
	/home/faiz89/Desktop/Spark/spark/bin/spark-submit random_forests_wide.py /home/faiz89/Desktop/Eastman/2008.csv > RF_narrow_run1_singleNode_2008.txt
fi
if [ $? -eq 0 ]; then
	/home/faiz89/Desktop/Spark/spark/bin/spark-submit random_forests_wide.py /home/faiz89/Desktop/Eastman/00-08.csv > RF_narrow_run1_singleNode_00-08.txt
fi
if [ $? -eq 0 ]; then
	/home/faiz89/Desktop/Spark/spark/bin/spark-submit random_forests_wide.py /home/faiz89/Desktop/Eastman/95-08.csv > RF_narrow_run1_singleNode_95-08.txt
fi

print "Done with all your jobs"
