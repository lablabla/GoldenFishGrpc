from concurrent import futures
import time
import logging

import grpc

import golden_fish_pb2
import golden_fish_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = golden_fish_pb2_grpc.GoldenFishStub(channel)
        valve = golden_fish_pb2.Valve(id=1, description="Meow")
        response = stub.RegisterValve(valve)
        logging.warning(f'Wow! Got {response.details}')


if __name__ == '__main__':
    logging.basicConfig()
    run()
