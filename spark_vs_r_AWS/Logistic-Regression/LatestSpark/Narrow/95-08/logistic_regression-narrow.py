from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.regression import LabeledPoint
from datetime import datetime
from numpy import array

sc = SparkContext (appName="Run 1 - Logistic Regression Narrow - Data95-08 - AWS")

data_file = "s3://aws-logs-012060642840-us-west-2/elasticmapreduce/cloud_proj/95-08.csv"
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
	nonLabel = clean_line_split[0:4]

	return LabeledPoint (label, nonLabel)

parsedData = raw_data.map (parsePoint)
#divide training and test data by 70-30 rule
(training, test) = parsedData.randomSplit ([0.7, 0.3], seed=11L)
#start timer at this point
startTime = datetime.now()
#build the model"""
model = LogisticRegressionWithLBFGS.train (training, numClasses=3)
training.cache ()

#evaluate the model on training data
labelAndPreds = test.map (lambda x: (x.label, model.predict (x.features)))
trainErr = labelAndPreds.filter (lambda (w, x): w != x).count () / float (test.count ())
print ('Time consumed = '), (datetime.now() - startTime)

print ("Training error = " + str (trainErr))

#save and load model
model.save (sc, "LRN-95-08")
sameModel = LogisticRegressionModel.load (sc, "LRN-95-08")
sc.stop ()
