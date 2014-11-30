import sys, time
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint
from numpy import array

port = 6633
host = '10.136.122.114'
learning_data_file = './Streaming_Classification_small.txt'
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
    values = [float(x) for x in line.split(',')]
    return LabeledPoint(values[0], values[1:])

# training the model
data = sc.textFile(learning_data_file)
parsedData = data.map(parsePoint)
model = (DecisionTree.trainClassifier(parsedData,
                                      numClasses=2,
                                      categoricalFeaturesInfo={},
                                      impurity='gini',
                                      maxDepth=30,
                                      maxBins=100))

# streaming and parsing text
lines = ssc.socketTextStream(host, port)
vectors = lines.flatMap(lambda x:x.split(',')).map(lambda l:float(l))

def classify(x):
  sample = array(x.take(x.count())) # array is a numpy array
  answer = model.predict(sample)
  print "============================================================"
  print answer

vectors.foreachRDD(classify)

ssc.start()
ssc.awaitTermination()
