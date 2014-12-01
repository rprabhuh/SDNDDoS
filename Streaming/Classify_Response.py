import sys, time, simplejson, socket
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from operator import add

HOST = 'localhost'
QUERY_PORT = 3000
ANS_PORT = 3006
BUFFER_SIZE = 256

#learning_data_file = './DDoSDataset.txt'
#learning_data_file = './DDoSDataset_medium.dat'
learning_data_file = './ExampleDataset.dat'
appName = "DDE"
conf = SparkConf().setAppName(appName).setMaster("local")
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 1)

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

#model = (DecisionTree.trainClassifier(parsedData,numClasses=2,categoricalFeaturesInfo={2:10},impurity='gini',maxDepth=30,maxBins=1000))

print "&&&&&&&&&&&&&&&&&&&&&&  model trained  &&&&&&&&&&&&&&&&&&&&&&&&"

reply_conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
reply_conn.connect((HOST, ANS_PORT))

# streaming and parsing text
lines = ssc.socketTextStream(HOST, QUERY_PORT)

"""
print '++++++++++++++++++++++++++++++++started the stream'
def printInput(x):
  print x.first()
lines.foreachRDD(printInput)
"""

vectors = lines.flatMap(lambda x:x.split(',')).map(lambda l:float(l))

def classify_and_reply(x):
  # test if x is an empty RDD  
  # http://mail-archives.apache.org/mod_mbox/spark-user/201402.mbox/%3C5303694D.2050705@exensa.com%3E
  if x.fold(0, add) != 0:
    print "============================================================"
    sample = array(x.take(x.count())) # array is a numpy array
    answer = model.predict(sample)
    print answer
    result = {"pkt_id" : "10.0.0.1", "allow": True if float(answer) > 0.5 else False}
    out = simplejson.dumps(result)
    print out
    reply_conn.send(out)
  # else:
  #   print "^^^^^^^^^^^^^^ RDD is empty ^^^^^^^^^^^^^"

vectors.foreachRDD(classify_and_reply)

ssc.start()
ssc.awaitTermination()
