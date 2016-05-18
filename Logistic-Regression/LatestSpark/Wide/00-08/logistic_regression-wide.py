from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.regression import LabeledPoint
from datetime import datetime
from pyspark.mllib.evaluation import MulticlassMetrics

sc = SparkContext ("local", "Run 1 - Logistic Regression Wide - Data00-08 - Single Node")

data_file = "/home/faiz89/Desktop/Eastman/00-08.csv"
raw_data = sc.textFile (data_file).cache ()
#extract the header
header = raw_data.first ()
raw_data = raw_data.filter (lambda x:x != header)

#load and parse the data
def parsePoint (line):
	#split lines based on the delimeter, and create a list
	line_split = line.split (",")

	#substituting NA with zeros
	line_split = [w.replace ('NA', '0') for w in line_split]
	
	#make Cancelled as binary since that's our response
	if (line_split[21] == '0'):
		line_split[21] = 0
	else:
		line_split[21] = 1
	
	#keep just numeric values
	"""
	1 = Month
	2 = DayofMonth
	3 = DayOfWeek
	5 = CRSDepTime
	7 = CRSArrTime
	12 = CRSElapsedTime
	18 = Distance
	21 = Cancelled,
	"""
	symbolic_indexes = [1, 2, 3, 5, 7, 12, 18, 21]
	clean_line_split = [item for i, item in enumerate (line_split) if i in symbolic_indexes]
	
	#Cancelled becomes the 8th column now, and total columns in the data = 8
	label = clean_line_split[7]
	nonLable = clean_line_split[0:7]

	return LabeledPoint (label, nonLable)

parsedData = raw_data.map (parsePoint)
#divide training and test data by 70-30 rule
(training, test) = parsedData.randomSplit ([0.7, 0.3], seed=11L)
training.cache ()

#start timer at this point
startTime = datetime.now()
#build the model
model = LogisticRegressionWithLBFGS.train (training, numClasses=3)

#evaluate the model on training data
labelAndPreds = test.map (lambda x: (x.label, model.predict (x.features)))

#labelAndPreds = testData.map (lambda x: (x.label, model.predict (x.features)))
trainErr = labelAndPreds.filter (lambda (w, x): w != x).count () / float (test.count ())

print ('Time consumed = '), (datetime.now() - startTime)

print ("Training error = " + str (trainErr))

#save and load model
model.save(sc, "LRW-00-08")
sameModel = LogisticRegressionModel.load(sc, "LRW-00-08")
sc.stop ()
"""metrics = MulticlassMetrics(labelAndPreds)
# Overall statistics
precision = metrics.precision()
recall = metrics.recall()
f1Score = metrics.fMeasure()
print("Summary Stats")
print("Precision = %s" % precision)
print("Recall = %s" % recall)
print("F1 Score = %s" % f1Score)"""
