import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics 
from math import sqrt 
from datetime import datetime



sc = SparkContext("local", "Correlations-narrow")

data_file = "2008.csv"
raw_data = sc.textFile(data_file)

def parse_interaction(line):
	#split lines based on the delimetre, and create a list
    line_split = line.split(",")
    symbolic_indexes = [14, 15, 19, 20, 24, 25, 26, 27, 28]
    clean_line_split = [item for i,item in enumerate(line_split) if i in symbolic_indexes]
    return np.array([float(x) for x in clean_line_split])

vector_data = raw_data.map(parse_interaction)

startTime = datetime.now()

print (Statistics.corr(vector_data, method="pearson"))

print datetime.now() - startTime