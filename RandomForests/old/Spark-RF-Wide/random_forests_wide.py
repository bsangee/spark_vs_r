import numpy as np
from pyspark import SparkContext
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.regression import LabeledPoint
from datetime import datetime
import sys
sc = SparkContext("local", "Run 1 Random Forests Data2008 Wide SingleNode")
# Load and parse the data file into an RDD of LabeledPoint.
data_file = sc.textFile(sys.argv[1])
#data_file = sc.textFile('2008_small.csv')
header = data_file.first ()
raw_data = data_file.filter (lambda x:x != header)

def parsePoint(line):
       
        line_split = line.split(",")
 	line_split = [w.replace ('NA', '0') for w in line_split]
        symbolic_indexes = [1,2,3,5,7,12,18,21]
        clean_line_split = [item for i,item in enumerate(line_split) if i in symbolic_indexes]
        values = [float(x) for x in clean_line_split]
        if values[7] == '1':
                       values[7]=1;
        else:
                       values[7]=0;
        return LabeledPoint(values[7], values[0:6]) #de

# Split the data into training and test sets (30% held out for testing)
parsedData = raw_data.map(parsePoint)
(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])

# Train a RandomForest model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
#  Note: Use larger numTrees in practice.
#  Setting featureSubsetStrategy="auto" lets the algorithm choose.
startTime = datetime.now()
trainingData.cache()
model = RandomForest.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},
                                     numTrees=3, featureSubsetStrategy="auto",
                                     impurity='gini', maxDepth=1, maxBins=2)
print ('Training Time consumed = '), (datetime.now() - startTime)
startTestTime = datetime.now()
testData.cache()

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
print ('Testing Time consumed = '), (datetime.now() - startTestTime)
print ('Time consumed = '), (datetime.now() - startTime)
print('Test Error = ' + str(testErr))
print('Learned classification forest model:')
print(model.toDebugString())

# Save and load model
#model.save(sc, "RandomForestClassificationModel_2008")
#sameModel = RandomForestModel.load(sc, "RandomForestClassificationModel_2008")
