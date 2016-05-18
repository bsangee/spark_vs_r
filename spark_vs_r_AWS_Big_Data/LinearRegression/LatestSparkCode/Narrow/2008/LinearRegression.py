import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics
from math import sqrt
import urllib
from pyspark.mllib.util import MLUtils
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel
from pyspark.mllib.regression import LabeledPoint
from datetime import datetime

# Load and parse the data
sc = SparkContext(appName= "Run1 Linear Regression Data2008 AWS- 80G")
def parsePoint(line):

	line_split = line.split(" ")
	line_split = [w.replace ('NA', '0') for w in line_split]
	symbolic_indexes = [4,5,6,7,11,12,13,14,15,18,19,20]
	
	clean_line_split = [item for i,item in enumerate(line_split) if i in symbolic_indexes]
	values = [float(x) for x in clean_line_split]
	
	label = clean_line_split[0]
	nonlabel = clean_line_split[1:] 
	
	return LabeledPoint(label, nonlabel) 

data_file = sc.textFile("In_80").cache ()
header = data_file.first ()
raw_data = data_file.filter (lambda x:x != header)

parsedData = raw_data.map(parsePoint)
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])
startTime = datetime.now()

# Build the model
trainingData.cache ()
model = LinearRegressionWithSGD.train(trainingData, iterations=1)
print ('Training Time consumed = '), (datetime.now() - startTime)
startTestTime = datetime.now()

# Evaluating the model on training data
valuesAndPreds = testData.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds \
    .map(lambda (v, p): (v - p)**2) \
    .reduce(lambda x, y: x + y) / valuesAndPreds.count()
print ('Testing Time consumed = '), (datetime.now() - startTestTime)
print ('Total Time: '), (datetime.now() - startTime)

print("Mean Squared Error = " + str(MSE))
# Save and load model
model.save(sc, "LinearRegressionNarrow2008_cache_both_train_and_test")
sameModel = LinearRegressionModel.load(sc, "LinearRegressionNarrow2008_cache_both_train_and_test")
sc.stop()
