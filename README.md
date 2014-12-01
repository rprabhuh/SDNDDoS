SDNDDoS
=======

Project repository for Cloud Computing Course [EEL6935] - Fall 2014

PROJECT TITLE: Big Data Analytics for Real-time DDoS Detection and Mitigation in SDN
TEAM: Rahul Prabhu, Sanil Sinai Borkar, Sile Hu, Umar Majeed


Folder Contents:
classification
- The MLlib algorithms that are provided as part of Apache Spark


Clustering
- KMeans.py: a way to find out the feature set using K-Means


Data
- Attack Dataset
	- Attack datasets (obtained from CAIDA)
- Normal Dataset
	- Normal datasets (extracted by the controller, containing the requests sent by HULK in SDN)
- FeatureSet.txt : The 43 features that were extracted from the incoming network packets by the controller to be sent to the DDE for prediction
- DDoSDataset.csv : A mix of attack data along with normal data


Defense
- SimpleTopology.py : Code to quarantine a suspected attacker


Interface
- Files containing code to render a visualization of the bandwidth consumption at the host


ntpddos
- Files pertaining to NTP DDoS attacks carried out initially (locally)


Screenshots
- Screenshots of various screens


Streaming
- .py Files : Files contaning python code to send data to EC2 from the controller and receive data from the DDE at the controller
- encode_protocol.py : Encoding for all the protocols used for network packet transmission
- IP_Protocols.csv : All the protocols used for network packet transmission, in use today
