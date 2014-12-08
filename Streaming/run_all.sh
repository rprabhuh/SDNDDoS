#!/usr/bin/env bash
gnome-terminal -x sh -c "sudo ./Setup_Net.py"
sleep 5
gnome-terminal -x sh -c "sudo ./Send_Samples.py"
sleep 5
gnome-terminal -x sh -c "sudo ./Recv_React.py"
sleep 5
gnome-terminal -x sh -c "sudo ${SPARK_HOME}/bin/spark-submit ./Classify_Response.py"
sleep 15
gnome-terminal -x sh -c "sudo ./emu_SYN.py"

