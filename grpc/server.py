import threading
from concurrent import futures

import torch
import grpc 

import modelserver_pb2_grpc, modelserver_pb2

lock = threading.Lock()

class PredictionCache:
    def __init__(self):
        lock.acquire()
        self.coefs = None
        self.lru_cache = {}
        self.recency_order = []
        self.cache_size = 10
        lock.release()

    def SetCoefs(self, coefs):
        lock.acquire()
        self.lru_cache.clear()
        self.recency_order = []
        self.coefs = torch.tensor(coefs, dtype=torch.float32)
        lock.release()

    def Predict(self, X):
        lock.acquire()
        X = torch.tensor(X, dtype=torch.float32)
        X = torch.round(X, decimals=4)
        tuple_X = tuple(X.flatten().tolist())

        if tuple_X in self.lru_cache:
            hit  = True
            y = self.lru_cache[tuple_X]
            self.recency_order.remove(tuple_X)
            self.recency_order.append(tuple_X)
        else:
            hit = False
            y = X @ self.coefs
            self.lru_cache[tuple_X] = y
            self.recency_order.append(tuple_X)

            if len(self.lru_cache) > self.cache_size:
                least_recent = self.recency_order.pop(0)
                self.lru_cache.pop(least_recent)

        lock.release()
        return y, hit
    
class ModelServer(modelserver_pb2_grpc.ModelServerServicer):
    def __init__(self):
        self.prediction_cache = PredictionCache()

    def SetCoefs(self, request, context):
        self.prediction_cache.SetCoefs(request.coefs)
        return modelserver_pb2.SetCoefsResponse(error="")

    def Predict(self, request, context):
        y, hit = self.prediction_cache.Predict(request.X)
        return modelserver_pb2.PredictResponse(y=y.float(), hit=hit, error="")

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=(('grpc.so_reuseport', 0),))
    modelserver_pb2_grpc.add_ModelServerServicer_to_server(ModelServer(), server)
    server.add_insecure_port("[::]:5440", )
    server.start()
    server.wait_for_termination()

        