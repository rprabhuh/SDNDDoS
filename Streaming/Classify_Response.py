import sys, time, simplejson, socket
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.mllib.tree import DecisionTree, RandomForest
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from operator import add

HOST = '127.0.0.1'
QUERY_PORT = 3000
ANS_PORT = 3006
BUFFER_SIZE = 256

learning_data_file = './DDoSDataset_removed_encap.txt'
appName = "DDE"
conf = SparkConf().setAppName(appName).setMaster("local[2]") #at least 2
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 1)

# separate the classification label and the actual data
def parsePoint(line):
  values = [float(x) for x in line.split(',')]
  return LabeledPoint(values[0], values[1:])

# training the model
data = sc.textFile(learning_data_file)
parsedData = data.map(parsePoint)

model = (DecisionTree.trainClassifier(parsedData,
                                      numClasses=2,
                                      categoricalFeaturesInfo={2:9},
                                      impurity='gini',
                                      maxDepth=30))
"""
model = (RandomForest.trainClassifier(parsedData,
                                      numClassesForClassification=2,
                                      numTrees=6,
                                      categoricalFeaturesInfo={2:10},
                                      impurity='gini',
                                      maxDepth=30))
"""
print "====================== model trained ======================"

# streaming and parsing text
lines = ssc.socketTextStream(HOST, QUERY_PORT)
vectors = lines.flatMap(lambda x:x.split(',')).map(lambda l:float(l))

reply_conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
reply_conn.connect((HOST, ANS_PORT))

def classify_and_reply(x):
  print "==========================================================="
  # test if x is an empty RDD
  # http://mail-archives.apache.org/mod_mbox/spark-user/201402.mbox/%3C5303694D.2050705@exensa.com%3E
  if x.fold(0, add) != 0:
    sample = array(x.take(x.count())) # array is a numpy array
    answer = model.predict(sample)
    print answer  # 0.0 benign, 1.0 malicious

    timestamp = str(x.take(1))
    print "timestamp = " + timestamp
    result = {"pkt_id" : timestamp,
              "allow"  : True if float(answer) < 0.5 else False}
    out = simplejson.dumps(result)
    print out
    reply_conn.send(out)
  else:
    print "empty RDD"

vectors.foreachRDD(classify_and_reply)

ssc.start()
ssc.awaitTermination()
