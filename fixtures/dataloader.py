import time, pycassa, uuid, models
from random import random


POOL = pycassa.ConnectionPool('Chariot')
MMEDIA = pycassa.ColumnFamily(POOL, 'MMedia')

def create_sources_sample():
    """docstring for create_sources_sample"""
    
def create_mmedias_samples():
    """docstring for create_mmedias_samples"""
    profiles = ['SD','HD']
    exts = ['MP4', 'FLV']
    for x in range(1000):
        mmedia1 = models.MMediaModel()
        mmedia1.create( id=x,name="Max %i" % x ,profile=profiles[round(random()*1)], \
                        file_name="Arquivo - %i" % i,file_size=round(random()*100000), \
                        ext=exts[round(random()*1)],source=3006)
        mmedia1_uuid = str(uuid.uuid1())
        MMEDIA.insert(mmedia1_uuid, mmedia1.to_dict())
        mBack = MMEDIA.get(mmedia1_uuid)
        print mBack

def initialize():
    create_mmedias_samples()
    
if __init__ == '__main__':
    initialize()