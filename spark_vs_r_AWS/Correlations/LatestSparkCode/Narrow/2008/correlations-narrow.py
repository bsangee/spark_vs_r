import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics 
from math import sqrt 
from datetime import datetime

sc = SparkContext(appName= "Run 1 - Corr-Wide - Data2008 - AWS")

data_file = "s3://aws-logs-012060642840-us-west-2/elasticmapreduce/cloud_proj/2008.csv"
raw_data = sc.textFile (data_file).cache ()
#extract header
header = raw_data.first () 
raw_data = raw_data.filter (lambda x:x != header)

def parse_interaction(line):
	#split lines based on the delimeter, and create a list
	line_split = line.split (",")
	#replace NA with zeros
	line_split = [w.replace ('NA', '0') for w in line_split]
	#remove year, and other non-numeric data
	"""
	0 = Year
	11 = ActualElapsedTime
	12 = CRSElapsedTime
	13 = AirTime
	16 = Distance 
	"""
	symbolic_indexes = [0, 8, 10, 11, 12, 13, 16, 17, 18, 22]
	clean_line_split = [item for i,item in enumerate (line_split) if i not in symbolic_indexes]
	return np.array ([float (x) for x in clean_line_split])

vector_data = raw_data.map (parse_interaction)

#start timer at this point
startTime = datetime.now()
print (Statistics.corr (vector_data, method="pearson"))
print ('Time consumed = '), (datetime.now() - startTime)
sc.stop()
