import numpy as np
from pyspark import SparkContext
from pyspark.mllib.stat import Statistics 
from math import sqrt 
from datetime import datetime

sc = SparkContext("local", "Run 1 - Corr-Wide - Data95-08 - Single Node")

data_file = "95-08.csv"
raw_data = sc.textFile (data_file).cache ()
#extract header
header = raw_data.first () 
raw_data = raw_data.filter (lambda x:x != header)

def parse_interaction(line):
	#split lines based on the delimeter, and create a list
	line_split = line.split (",")
	#replace NA with zeros
	line_split = [w.replace ('NA', '0') for w in line_split]
	#keep just numeric values
	"""
	1 = Month
	2 = DayofMonth
	3 = DayOfWeek
	4 = DepTime
	5 = CRSDepTime
	6 = ArrTime
	7 = CRSArrTime
	9 = FlightNum
	11 = ActualElapsedTime
	12 = CRSElapsedTime
	13 = AirTime
	14 = ArrDelay
	15 = DepDelay
	18 = Distance
	19 = TaxiIn
	20 = TaxiOut
	21 = Cancelled
	23 = Diverted
	24 = CarrierDelay
	25 = WeatherDelay
	26 = NASDelay
	27 = SecurityDelay
	28 = LateAircraftDelay
	"""
	symbolic_indexes = [1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28]
	clean_line_split = [item for i,item in enumerate (line_split) if i in symbolic_indexes]
	return np.array ([float (x) for x in clean_line_split])

vector_data = raw_data.map (parse_interaction)

#start timer at this point
startTime = datetime.now()
print (Statistics.corr (vector_data, method="pearson"))
print ('Time consumed = '), (datetime.now() - startTime)
