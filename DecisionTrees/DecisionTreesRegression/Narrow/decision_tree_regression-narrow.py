from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from datetime import datetime

sc = SparkContext ("local", "Run 1 - Decision Tree Classification Narrow - Data2008 - Single Node")

data_file = "2008-reduced.csv"
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
	#make Cancelled as binary since that's our response
	if (line_split[21] > 0):
		line_split[21] = 1
	else:
		line_split[21] = 0
	#keep just numeric values
	"""
	5 = CRSDepTime
	7 = CRSArrTime
	12 = CRSElapsedTime
	18 = Distance
	21 = Cancelled,
	"""
	symbolic_indexes = [5, 7, 12, 18, 21]
	clean_line_split = [item for i, item in enumerate (line_split) if i in symbolic_indexes]
	
	#Cancelled becomes the 5th column now, and total columns in the data = 5
	label = clean_line_split[4]
	nonLable = clean_line_split[0:4]
	return LabeledPoint (label, nonLable)

parsedData = raw_data.map (parsePoint)
#divide training and test data by 70-30 rule
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])

#start timer at this point
startTime = datetime.now()
#build the model
model = DecisionTree.trainRegressor (trainingData, categoricalFeaturesInfo={},
                                        impurity='variance', maxDepth=3, maxBins=16)
#evaluate model on test instances and compute test error
predictions = model.predict(testData.map (lambda x: x.features))
labelsAndPredictions = testData.map (lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map (lambda (v, p): (v - p) * (v - p)).sum() / float (testData.count())
print ('Time consumed = '), (datetime.now() - startTime)

print ('Test Mean Squared Error = ' + str (testMSE))
print ('Learned regression tree model:')
print (model.toDebugString())

#save and load model
#model.save (sc, "DTR-Narrow-2008")
#sameModel = DecisionTreeModel.load(sc, "DTR-Narrow-2008")