import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics 
from math import sqrt 

sc = SparkContext("local", "SUMMARY STATISTICS")

data_file = "2008.csv"
raw_data = sc.textFile(data_file)

"""
For dense vectors, MLlib uses either Python lists or the NumPy array type. 
The later is recommended, so you can simply pass NumPy arrays around.
For sparse vectors, users can construct a SparseVector object from MLlib 
or pass SciPy scipy.sparse column vectors if SciPy is available in their environment. 
The easiest way to create sparse vectors is to use the factory methods imlpemented in Vectors. 
"""

"""
we replaced all NA with 0 => sed -i 's/NA/0/g' file name
we also removed the headers line => sed -i 1d filename
"""

def parse_interaction(line):
	#split lines based on the delimetre, and create a list
    line_split = line.split(",")
    # keep just numeric and logical values
    #symbolic_indexes = [1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,18,20,21,22,24,25,26,27,28,29]
    symbolic_indexes = [8, 10, 13, 16, 17, 19, 20, 22, 24, 25, 26, 27, 28]
    clean_line_split = [item for i,item in enumerate(line_split) if i not in symbolic_indexes]
    return np.array([float(x) for x in clean_line_split])

vector_data = raw_data.map(parse_interaction)

summary = Statistics.colStats(vector_data)

print ('Mean of columns\n'), summary.mean ()
print ('Variances of columns\n'), summary.variance()
print ('Non zero values\n'), summary.numNonzeros()
print ('Max value\n'), summary.max ()
print ('Min value\n'), summary.min ()