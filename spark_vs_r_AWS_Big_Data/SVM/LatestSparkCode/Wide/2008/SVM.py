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
sc = SparkContext(appName =  "Run 1 SVM wide Data2008 training AWS-80G")
data_file = sc.textFile("In_80")
#raw_data = sc.textFile (data_file).cache ()
#extract header
header = data_file.first()
raw_data = data_file.filter (lambda x:x != header)

def parsePoint(line):
	line_split = line.split(" ")
	line_split = [w.replace ('NA', '0') for w in line_split]
	symbolic_indexes = [1, 2, 3, 5, 7, 12, 18, 21]

	clean_line_split = [item for i,item in enumerate(line_split) if i in symbolic_indexes]
	values = [float(x) for x in clean_line_split]

	return LabeledPoint(values[0], values[1:]) #dep_delay, cancelled, diverted, carrierdelay, weather delay, NASdelay, Security delay, LateAircraftdelay

#examples = MLUtils.loadLibSVMFile(sc, "2008.csv").collect()
parsedData = raw_data.map(parsePoint)
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])
startTime = datetime.now()

# Build the model
trainingData.cache ()
model = SVMWithSGD.train(trainingData, iterations=1)
print ('Training Time consumed = '), (datetime.now() - startTime)
startTestTime = datetime.now()

# Evaluating the model on test data
labelsAndPreds = testData.map(lambda p: (p.label, model.predict(p.features)))
testErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(testData.count())
print ('Testing Time consumed = '), (datetime.now() - startTestTime)
print ('Time consumed = '), (datetime.now() - startTime)

print("Training Error = " + str(testErr))


# Save and load model
model.save(sc, "SVMwide2008train")
sameModel = SVMModel.load(sc, "SVMwide2008train")
sc.stop()

