FROM p4-hdfs
RUN pip3 install jupyterlab==4.0.3 pyarrow==13.0.0 requests==2.31.0 nbconvert==7.9.2

CMD export CLASSPATH=`$HADOOP_HOME/bin/hdfs classpath --glob` && \
    hdfs datanode -D dfs.datanode.data.dir=/var/datanode -fs hdfs://boss:9000
