from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.regression import LabeledPoint
from datetime import datetime
from numpy import array

sc = SparkContext ('local', 'Run 1')
raw_data = '2008-reduced.csv'
data = sc.textFile(raw_data).cache ()
#print 'Train size is {}'.format (raw_data.count ())

header = data.first ()
data = data.filter (lambda x:x != header)

def Parsing (line):
	line_split = line.split (',')
	line_split = [w.replace ('NA', '0') for w in line_split]

	"""
	5 = CRSDepTime
	7 = CRSArrTime
	12 = CRSElapsedTime
	18 = Distance
	21 = Cancelled,
	"""
	symbolic_indexes = [21, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 26, 27, 28]
	clean_line_split = [item for i, item in enumerate (line_split) if i in symbolic_indexes]

	label = clean_line_split[0]
	nonLabel = clean_line_split[1:]
	"""if clean_line_split[0] == 0:
		clean_line_split[0] = 0
	else:
		clean_line_split = 1"""
	
	#values = [float (x) for x in clean_line_split]

	return LabeledPoint (label, nonLabel)

parsedData = data.map (Parsing)
(trainingData, testData) = parsedData.randomSplit ([0.7, 0.3], seed=11L)
trainingData.cache ()

model = LogisticRegressionWithLBFGS.train (trainingData, numClasses=3)

labelAndPreds = testData.map(lambda lp: (float(model.predict(lp.features)), lp.label))

trainErr = labelAndPreds.filter (lambda (w, x): w != x).count () / float (testData.count ())


print ("Training error = " + str (trainErr))