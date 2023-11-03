import csv 
import threading
import queue
import sys

import grpc
import modelserver_pb2_grpc, modelserver_pb2

q = queue.Queue()

def pred_req(fname: str):
    with open(fname, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        for i in range(len(data)):
            data[i] = list(map(float, data[i]))
        
        hits = 0
        for i in range(len(data)):
            resp = stub.Predict(modelserver_pb2.PredictRequest(X=data[i]))
            hits += int(bool(resp.hit))

        q.put((hits, len(data)))

if __name__ == '__main__':
    # take port number from command line arguments
    port = sys.argv[1]
    channel = grpc.insecure_channel(f'localhost:{port}')
    stub = modelserver_pb2_grpc.ModelServerStub(channel)

    coefs_str = sys.argv[2]
    coefs = list(map(float, coefs_str.split(',')))
    stub.SetCoefs(modelserver_pb2.SetCoefsRequest(coefs=tuple([1.0,2.0,3.0])))

    threads = []
    for i in range(3, len(sys.argv)):
        csv_file = sys.argv[i]
        t = threading.Thread(target=pred_req, args=(csv_file,))
        threads.append(t) 

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    hits = 0
    total_len = 0
    for i in range(len(sys.argv) - 3):
        hit, len = q.get()
        hits += hit
        total_len += len

    print(hits / total_len)
    
