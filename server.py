from concurrent import futures
from datetime import datetime
import logging
import os
import sys
import grpc

import golden_fish_pb2_grpc

from GoldenFishServicer import GoldenFishServicer


def serve(logger):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    golden_fish_pb2_grpc.add_GoldenFishServicer_to_server(GoldenFishServicer(logger), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logger = logging.getLogger('MainLogger')
    logger.setLevel(logging.DEBUG)

    if not os.path.exists('logs'):
        os.makedirs('logs')
    fh = logging.FileHandler('logs/server_{:%Y-%m-%d %H-%M-%S}.log'.format(datetime.now()))
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logger.level)
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(console)
    serve(logger)
