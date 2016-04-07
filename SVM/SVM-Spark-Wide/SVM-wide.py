import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics
from math import sqrt
import urllib
from pyspark.mllib.util import MLUtils

from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint

from datetime import datetime


# Load and parse the data
sc = SparkContext("local", "Run 1 SVM narrow Data2008 Single Node")
data_file = sc.textFile("../2008.csv")
#raw_data = sc.textFile (data_file).cache ()
#extract header
header = data_file.first()
raw_data = data_file.filter (lambda x:x != header)

def parsePoint(line):
    	#not_included_cols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,22,24,25,27,28]
	line_split = line.split(",")
	line_split = [w.replace ('NA', '0') for w in line_split]
	symbolic_indexes = [21,1, 2, 3, 5, 7, 12, 18]
	clean_line_split = [item for i,item in enumerate(line_split) if i in symbolic_indexes]
	values = [float(x) for x in clean_line_split]
	return LabeledPoint(values[0], values[1:]) #dep_delay, cancelled, diverted, carrierdelay, weather delay, NASdelay, Security delay, LateAircraftdelay

#examples = MLUtils.loadLibSVMFile(sc, "2008.csv").collect()
parsedData = raw_data.map(parsePoint)
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])
# Build the model
model = SVMWithSGD.train(trainingData, iterations=1)

# Evaluating the model on test data
labelsAndPreds = testData.map(lambda p: (p.label, model.predict(p.features)))
testErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(testData.count())
print("Training Error = " + str(testErr))

# Save and load model
