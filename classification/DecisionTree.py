from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark import SparkContext, SparkConf
import sys

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
	print("Please pass the filename of the dataset as a commandline argument")
	exit(0);

# Read the input data file
data = sc.textFile("../Data/"+sys.argv[1])

# Parse the data to construct a classification dataset
parsedData = data.map(parsePoint)

#Indicate the categorical attributes
#categorical_attributes = {2:2,3:3,4:3}
# Build the classification model
'''
impurity can be any of {gini, entropy, variance}
categoricalFeaturesInfo contains information pertaining to categorical features in the dataset
'''
model = DecisionTree.trainClassifier(parsedData, numClasses=2, categoricalFeaturesInfo={0:3},
                                     impurity='gini', maxDepth=30, maxBins=100)

# PRINT THE MODEL
#print('Learned decision tree model:')
#print(model.toDebugString())

# Evaluating the model on training data
#sys.stdout.write(model)

# Working: Predict with a single input
#predictions = model.predict(array([2,1032,0,0,0,0,0,0,0,0,0,255,255,1,0,1,0,0,0]))

# BATCH PREDICTION
predictions = model.predict(parsedData.map(lambda x: x.features))
labelsAndPredictions = parsedData.map(lambda lp: lp.label).zip(predictions)

# Dsiplay Training Mean Squared Error
trainMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(parsedData.count())
print('Training Mean Squared Error = ' + str(trainMSE))

# Dsiplay Training Error
trainErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(parsedData.count())
print('Training Error = ' + str(trainErr))

