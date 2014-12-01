from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark import SparkContext, SparkConf
import sys
import timeit
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

#Check if the dataset has been passed as an argument
if(len(sys.argv)==1):
	print("Please pass the filename of the Train and Test datasets as commandline arguments")
	exit(0);

# Read the input data file
Traindata = sc.textFile("../Data/"+sys.argv[1])
Testdata = sc.textFile("../Data/"+sys.argv[2])
# Parse the data to construct a classification dataset

parsedData = Traindata.map(parsePoint)
parsedTestData = Testdata.map(parsePoint)


# Build the classification model
'''
impurity can be any of {gini, entropy, variance}
categoricalFeaturesInfo contains information pertaining to categorical features in the dataset
'''
start = timeit.timeit()
model = DecisionTree.trainClassifier(parsedData, numClasses=2, categoricalFeaturesInfo={},
                                     impurity='gini', maxDepth=30, maxBins=1000)
end = timeit.timeit()

print "Time to Train = " + str(end-start)

print model.toDebugString()

# BATCH PREDICTION
start = timeit.timeit()

predictions = model.predict(parsedTestData.map(lambda x: x.features))
labelsAndPredictions = parsedTestData.map(lambda lp: lp.label).zip(predictions)

# Dsiplay Training Mean Squared Error
trainMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(parsedTestData.count())
print('Training Mean Squared Error = ' + str(trainMSE))

# Dsiplay Training Error
trainErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(parsedTestData.count())

end = timeit.timeit()

print('Training Error = ' + str(trainErr))
print "Time to test = " + str(end-start)
