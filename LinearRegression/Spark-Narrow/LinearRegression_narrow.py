import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics
from math import sqrt
import urllib
from pyspark.mllib.util import MLUtils
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel
from pyspark.mllib.regression import LabeledPoint

# Load and parse the data
sc = SparkContext("local", "Run1 Linear Regression Data00-08 SingleNode")
def parsePoint(line):

	line_split = line.split(",")
	line_split = [w.replace ('NA', '0') for w in line_split]
	symbolic_indexes = [14,15,18,21,23,13]
	clean_line_split = [item for i,item in enumerate(line_split) if i in symbolic_indexes]
	values = [float(x) for x in clean_line_split]

	return LabeledPoint(values[0], values[1:]) 

data_file = sc.textFile("00-08.csv")
header = data_file.first ()
raw_data = data_file.filter (lambda x:x != header)

#examples = MLUtils.loadLibSVMFile(sc, "2008.csv").collect()
parsedData = raw_data.map(parsePoint)
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])
# Build the model
model = LinearRegressionWithSGD.train(trainingData, iterations=1)

# Evaluating the model on training data
valuesAndPreds = trainingData.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds \
    .map(lambda (v, p): (v - p)**2) \
    .reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))
# Save and load model
model.save(sc, "LinearRegression")
sameModel = LinearRegressionModel.load(sc, "LinearRegression")
