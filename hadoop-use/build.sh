docker build . -f hdfs.Dockerfile -t p4-hdfs
docker build . -f notebook.Dockerfile -t p4-nb
docker build . -f namenode.Dockerfile -t p4-nn
docker build . -f datanode.Dockerfile -t p4-dn
