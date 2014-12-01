from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark import SparkContext, SparkConf
import sys
import timeit
appName = "DDE"

# Setup Spark configuration
conf = SparkConf().setAppName(appName).setMaster("local")
sc = SparkContext(conf=conf)

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

#Check if the dataset has been passed as an argument
if(len(sys.argv)==1):
	print("Please pass the filename of the dataset as a commandline argument")
	exit(0);

start = timeit.timeit()
# Read the input data file
data = sc.textFile("../Data/"+sys.argv[1])

# Parse the data to construct a classification dataset
parsedData = data.map(parsePoint)

# Build the classification model
model = NaiveBayes.train(parsedData)

end = timeit.timeit()

print "Training Time = " + str(end-start)

# Evaluating the model on training data

start = timeit.timeit()

labelsAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())

end = timeit.timeit()

print("Training Error = " + str(trainErr))
print "Training Time = " + str(end-start)
