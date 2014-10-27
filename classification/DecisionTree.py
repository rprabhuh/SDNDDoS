from pyspark.mllib.tree import DecisionTree
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
'''
impurity can be any of {gini, entropy, variance}
categoricalFeaturesInfo contains information pertaining to categorical features in the dataset
'''
model = DecisionTree.trainClassifier(parsedData, numClasses=2, categoricalFeaturesInfo={},
                                     impurity='gini', maxDepth=5, maxBins=100)
# Evaluating the model on training data

predictions = model.predict(parsedData.map(lambda x: x.features))
labelsAndPredictions = parsedData.map(lambda lp: lp.label).zip(predictions)
trainMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(parsedData.count())
print('Training Mean Squared Error = ' + str(trainMSE))
print('Learned regression tree model:')
print(model)
