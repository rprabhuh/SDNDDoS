#Import for Spark Classification
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint
from numpy import array

#Import for General Python Stuff
import sys
import time

#Declarations
port = 3000
host = 'localhost'
learning_data_file = '../Data/dataset.dat'

# Spark configuration
appName = "DDE"
conf = SparkConf().setAppName(appName).setMaster("local")
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 1)

'''
parsePoint
	This function takes a line and returns a labeled point
Input : String - A line of input
Output: Labeled Point - Labled point consisting of the class
	label and the attributes of the row.
Expects:
	- The attributes in the row should be comma separated
	- The first column should be the class label
'''
def parsePoint(line):
    values = [float(x) for x in line.split(' ')]
    return LabeledPoint(values[0], values[1:])

# Build the model using offline data
data = sc.textFile(learning_data_file)

parsedData = data.map(parsePoint)
model = DecisionTree.trainClassifier(parsedData, numClasses=2, categoricalFeaturesInfo={},
					impurity='gini', maxDepth=30, maxBins=100)

#model = DecisionTree.trainClassifier(parsedData, numClasses=2, categoricalFeaturesInfo={},impurity='gini', maxDepth=30, maxBins=100)
f= open("output.txt", "w")
def pred(x):
  res = model.predict(x)
  f.write("The prediction is:")
  f.write("%s\n"%res.toDebugString())
  return res



# Classify the rows coming in as a stream
lines = ssc.socketTextStream(host, port)

#prediction = model.predict(lines.flatMap(lambda line: line.split(" ")))
'''
words = lines.flatMap(lambda x:x.split()).map(lambda x:(x,1))
	This needs to be paired up with a reduce job
'''
#print prediction

vectors = lines.flatMap(lambda x:x.split()).map(lambda l:map(float, l.split()))

vectors.foreachRDD(pred)

ssc.start()
ssc.awaitTermination()

