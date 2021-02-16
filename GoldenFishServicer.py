import time

import golden_fish_pb2
import golden_fish_pb2_grpc


class GoldenFishServicer(golden_fish_pb2_grpc.GoldenFishServicer):

    def __init__(self, logger):
        self.logger = logger
        self.logger.info('GoldenFish Servicer initializing')

    def RegisterValve(self, request, context):
        self.logger.info(f'Received request to register valve with id {request.id}')
        return golden_fish_pb2.Status(code=0, details="Meow indeed")
