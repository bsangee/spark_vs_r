from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from datetime import datetime

sc = SparkContext ("local[*]", "Run 1 - Decision Tree Regression Wide - Data2008 - Single Node")

data_file = "/home/faiz89/Desktop/Eastman/2008.csv"
raw_data = sc.textFile (data_file).cache ()
#extract the header
header = raw_data.first ()
raw_data = raw_data.filter (lambda x:x != header)

#load and parse the data
def parsePoint (line):
	#split lines based on the delimeter, and create a list
	line_split = line.split (",")
	#replace NA with zeros
	line_split = [w.replace ('NA', '0') for w in line_split]
	
	#keep only the columns needed
	"""
	1 = Month
	2 = DayofMonth
	3 = DayOfWeek
	4 = DepTime
	5 = CRSDepTime
	6 = ArrTime
	7 = CRSArrTime
	8 = UniqueCarrier - Non numeric
	11 = ActualElapsedTime
	12 = CRSElapsedTime
	13 = ArrTime
	14 = ArrDelay
	15 - DepDelay
	18 = Distance
	19 = TaxiIn
	20 = TaxiOut
	"""

	symbolic_indexes = [1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 18, 19, 20]
	clean_line_split = [item for i, item in enumerate (line_split) if i in symbolic_indexes]
	
	#ArrDelay is our response
	#ArrDelay becomes the 11th column now, and total columns in the data = 11
	label = clean_line_split[10]
	nonLable = clean_line_split[0:10] + clean_line_split[11:]
	return LabeledPoint (label, nonLable)

parsedData = raw_data.map (parsePoint)
#divide training and test data by 70-30 rule
(training, test) = parsedData.randomSplit([0.7, 0.3])

#start timer at this point
startTime = datetime.now()
#build the model
#empty categoricalFeaturesInfo indicates all features are continuous.
model = DecisionTree.trainRegressor (training, categoricalFeaturesInfo={},
                                         impurity='variance', maxDepth=5, maxBins=32)

#evaluate model on test instances and compute test error
predictions = model.predict (test.map (lambda x: x.features))
labelsAndPredictions = test.map (lambda lp: lp.label).zip (predictions)
testMSE = labelsAndPredictions.map (lambda (v, p): (v - p) * (v - p)).sum() /\
    float(testData.count())

print ('Time consumed = '), (datetime.now() - startTime)

print ('Test Mean Squared Error = ' + str (testMSE))
print ('Learned regression tree model:')
print (model.toDebugString())

#save and load model
model.save (sc, "DTR-Wide-2008")
sameModel = DecisionTreeModel.load (sc, "DTR-Wide-2008")
sc.stop ()
