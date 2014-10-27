from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark import SparkContext, SparkConf

appName = "KDDDataset"

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

# Read the input data file
data = sc.textFile("dataset.dat")

# Parse the data to construct a classification dataset
parsedData = data.map(parsePoint)

# Build the classification model
model = LogisticRegressionWithSGD.train(parsedData)

# Evaluating the model on training data
labelsAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(parsedData.count())
print("Training Error = " + str(trainErr))
