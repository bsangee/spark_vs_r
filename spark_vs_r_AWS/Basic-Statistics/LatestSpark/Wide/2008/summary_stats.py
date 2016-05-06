import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics 
from math import sqrt 
from datetime import datetime

sc = SparkContext (appName= "Run 1 - Summary Statistics - Data2008 - AWS")

data_file = "s3://aws-logs-012060642840-us-west-2/elasticmapreduce/cloud_proj/2008.csv"
raw_data = sc.textFile (data_file).cache ()
#extract header
header = raw_data.first () 
raw_data = raw_data.filter (lambda x:x != header)

"""
For dense vectors, MLlib uses either Python lists or the NumPy array type. 
The later is recommended, so you can simply pass NumPy arrays around.
For sparse vectors, users can construct a SparseVector object from MLlib 
or pass SciPy scipy.sparse column vectors if SciPy is available in their environment. 
The easiest way to create sparse vectors is to use the factory methods imlpemented in Vectors. 
"""

def parse_interaction (line):
	#split lines based on the delimeter, and create a list
	line_split = line.split (",")
	#replace NA with zeros
	line_split = [w.replace ('NA', '0') for w in line_split]
	#line_split = [w.replace ('', '0') for w in line_split]
	#keep all except year, and non-numeric values
	symbolic_indexes = [0, 8, 10,16, 17, 22]
	clean_line_split = [item for i,item in enumerate (line_split) if i not in symbolic_indexes]
	return np.array ([float (x) for x in clean_line_split])

vector_data = raw_data.map (parse_interaction)

#start timer at this point
startTime = datetime.now()
summary = Statistics.colStats(vector_data)
print ('Time consumed = '), (datetime.now() - startTime)

print ('Mean of columns\n'), summary.mean ()
print ('Variances of columns\n'), summary.variance()
print ('Non zero values\n'), summary.numNonzeros()
print ('Max value\n'), summary.max ()
print ('Min value\n'), summary.min ()
sc.stop()
