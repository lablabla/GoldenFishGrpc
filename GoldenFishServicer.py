from datetime import datetime
import logging
import os
import sqlite3
import sys

import grpc
import golden_fish_pb2
import golden_fish_pb2_grpc
from DBManager import DBManager
from data.Models import Valve


class GoldenFishServicer(golden_fish_pb2_grpc.GoldenFishServicer):

    def __init__(self):
        self.logger = logging.getLogger('MainLogger')
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_path = 'logs/server_{:%Y-%m-%d %H-%M-%S}.log'.format(datetime.now())
        fh = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s | %(name)-10s | %(levelname)-8s | %(lineno)04d | %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(self.logger.level)
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(console)
        self.logger.info('GoldenFish Servicer initializing')
        self.db_manager = DBManager(self.logger)

    def RegisterValve(self, request, context):
        self.logger.info(f'Received request to register valve with id {request.id}')
        v = Valve(request.id, request.description)
        try:
            self.db_manager.register_valve(v)
        except sqlite3.Error as ex:
            self.logger.exception(ex)
            context.set_details(str(ex))
            context.set_code(grpc.StatusCode.INTERNAL)
            return golden_fish_pb2.Status(code=-1, details=str(ex))

        return golden_fish_pb2.Status(code=0, details="OK")
