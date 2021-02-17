from concurrent import futures

import grpc

import golden_fish_pb2_grpc

from GoldenFishServicer import GoldenFishServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    golden_fish_pb2_grpc.add_GoldenFishServicer_to_server(GoldenFishServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

