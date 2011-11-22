#!/usr/bin/env python
# encoding: utf-8
import pycassa
from pycassa.system_manager import *

class Schema(object):
    sys = None
    def __init__(self):
        self.sys = SystemManager()

    def hasSchema(self):
        if 'Chariot' in self.sys.list_keyspaces():
            msg = 'Looks like you already have a The Chariot keyspace.\nDo you '
            msg += 'want to delete it and recreate it? All current data will '
            msg += 'be deleted! (y/n): '
            resp = raw_input(msg)
            if not resp or resp[0] != 'y':
                print "Ok, then we're done here."
                return True
            else:
                self.dropSchema()
        return False

    def dropSchema(self):
        self.sys.drop_keyspace('Chariot')
        
    def createSchema(self):
        self.sys.create_keyspace('Chariot', SIMPLE_STRATEGY, {'replication_factor': '1'})
        self.sys.create_column_family('Chariot', 'VOD', comparator_type=UTF8_TYPE)
        self.sys.create_column_family('Chariot', 'LIVE', comparator_type=UTF8_TYPE) #TIME_UUID_TYPE)
        self.sys.create_column_family('Chariot', 'MULTIMEDIA', comparator_type=UTF8_TYPE)
        self.sys.create_column_family('Chariot', 'EDGENODE', comparator_type=UTF8_TYPE)
        self.sys.create_column_family('Chariot', 'CDNCOUNTRY', super=True, comparator_type=UTF8_TYPE)
        self.sys.create_column_family('Chariot', 'BGP', comparator_type=UTF8_TYPE)
        self.sys.create_column_family('Chariot', 'FARM', comparator_type=UTF8_TYPE)
             
    def sync(self):
        if not self.hasSchema():
            self.createSchema()
            print 'all done dude!'

if __name__ == "__main__":
    sc = Schema()
    sc.sync()