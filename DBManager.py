import enum
import logging
import os
from database import Database
from data.Models import Valve
import sys


class Tables(enum.Enum):
    Valves = 'Valves',
    Events = 'Events'


class DBManager(object):

    def __init__(self, main_logger):
        self.logger = logging.getLogger('DBLogger')
        self.logger.setLevel(logging.DEBUG)
        for lh in main_logger.handlers:
            self.logger.addHandler(lh)
        self.logger.debug('DBManager init')
        self.db_name = 'GoldenFish.sqlite3'
        self.init_db()

    def init_db(self):
        with Database(self.db_name) as db:
            db.query(f'CREATE TABLE IF NOT EXISTS {Tables.Valves.name} ('
                      'Id integer PRIMARY KEY,'
                      'Description STRING NOT NULL'
                      ')')

    def register_valve(self, valve: Valve):
        with Database(self.db_name) as db:
            db.write(Tables.Valves.name, 'Id,Description', f'{valve.id},\"{valve.description}\"')


