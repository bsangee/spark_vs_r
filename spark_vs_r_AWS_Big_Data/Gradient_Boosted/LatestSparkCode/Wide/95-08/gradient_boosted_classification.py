from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import GradientBoostedTrees, GradientBoostedTreesModel
from datetime import datetime

sc = SparkContext (appName="Run 1 - Gradient Boosted Classification Wide - Data95-08 - AWS")

data_file = "s3://aws-logs-012060642840-us-west-2/elasticmapreduce/cloud_proj/95-08.csv"
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
	if (line_split[21] == '0'):
		line_split[21] = 0
	else:
		line_split[21] = 1

	#keep just the columns needed
	"""
	1 = Month
	2 = DayOfMonth
	3 = DayOfWeek
	5 = CRSDepTime
	7 = CRSArrTime
	8 = UniqueCarrier = Non numeric
	12 = CRSElapsedTime
	18 = Distance
	21 = Cancelled
	"""
	symbolic_indexes = [1, 2, 3, 5, 7, 12, 18, 21]
	clean_line_split = [item for i, item in enumerate (line_split) if i in symbolic_indexes]
	
	#Cancelled becomes the 8th column now, and total columns in the data = 8
	label = clean_line_split[7]
	nonLable = clean_line_split[0:7]
	return LabeledPoint (label, nonLable)

parsedData = raw_data.map (parsePoint)
#divide training and test data by 70-30 rule
(training, test) = parsedData.randomSplit([0.7, 0.3])
training.cache ()

#start timer at this point
startTime = datetime.now()
#build the model
model = GradientBoostedTrees.trainClassifier(training,
                                             categoricalFeaturesInfo={}, numIterations=3)

#evaluate model on test instances and compute test error
predictions = model.predict (test.map (lambda x: x.features))
labelsAndPredictions = test.map (lambda lp: lp.label).zip (predictions)
testErr = labelsAndPredictions.filter (lambda (v, p): v != p).count() / float(test.count())
print ('Time consumed = '), (datetime.now() - startTime)

print ('Test Error = ' + str (testErr))
print ('Learned classification GBT model:')
print (model.toDebugString())

#save and load model
model.save(sc, "GB-Class-W-95-08")
sameModel = DecisionTreeModel.load(sc, "GB-Class-W-95-08")
sc.stop ()
