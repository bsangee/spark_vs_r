from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.regression import LabeledPoint
from datetime import datetime
from numpy import array

sc = SparkContext ("local", "Run 1 - Logistic Regression Narrow - Data2008 - Single Node")

data_file = "2008-reduced.csv"
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
	
	#cancelled = line_split[21]
	"""if (line_split[21] > 0):
		line_split[21] = 1
	else:
		line_split[21] = 0"""
	
	#keep just numeric values
	"""
	5 = CRSDepTime
	7 = CRSArrTime
	12 = CRSElapsedTime
	18 = Distance
	21 = Cancelled,
	"""
	symbolic_indexes = [21, 5, 7, 12, 18]
	clean_line_split = [item for i, item in enumerate (line_split) if i in symbolic_indexes]
	
	#Cancelled becomes the 5th column now, and total columns in the data = 5
	#label = clean_line_split[4]
	#nonLable = clean_line_split[0:4]# + clean_line_split[2]
	values = [float (x) for x in clean_line_split]

	if values[0] > 0.5:
		values[0]=1;
	else:
		values[0]=0;

	return LabeledPoint (values[0], values[1:])
	#return LabeledPoint (clean_line_split[0], clean_line_split[1:])

parsedData = raw_data.map (parsePoint)
#divide training and test data by 70-30 rule
(trainingData, testData) = parsedData.randomSplit ([0.7, 0.3], seed=11L)
#print trainingData
#start timer at this point
#startTime = datetime.now()
#build the model"""
model = LogisticRegressionWithLBFGS.train (trainingData, numClasses=3)

#evaluate the model on training data
labelAndPreds = testData.map (lambda x: (x.label, model.predict (x.features)))
trainErr = labelAndPreds.filter (lambda (w, x): w != x).count () / float (testData.count ())
#print ('Time consumed = '), (datetime.now() - startTime)

print ("Training error = " + str (trainErr))

#save and load model
#model.save(sc, "LR-N-2008")
#sameModel = LogisticRegressionModel.load(sc, "LRN-2008")
#sc.stop ()
