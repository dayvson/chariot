import time, pycassa, uuid
from pycassa.cassandra.ttypes import NotFoundException
from pycassa.pool import ConnectionPool

__all__ = ['VOD', 'LIVE']
POOL = pycassa.connect('Chariot')

VOD_POOL = pycassa.ColumnFamily(POOL, 'VOD')
LIVE_POOL = pycassa.ColumnFamily(POOL, 'LIVE')
MULTIMEDIA_POOL = pycassa.ColumnFamily(POOL, 'MULTIMEDIA')
EDGE_POOL = pycassa.ColumnFamily(POOL, 'EDGENODE')
CDNCOUNTRY_POOL = pycassa.ColumnFamily(POOL, 'CDNCOUNTRY')
FARM_POOL = pycassa.ColumnFamily(POOL, 'FARM')

class DatabaseError(Exception):
    """
    The base error that functions in this module will raise when things go
    wrong.
    """
    pass

class NotFound(DatabaseError):
    pass

class InvalidDictionary(DatabaseError):
    pass


class ModelBase(object):
    def __init__(self, pool, meta):
        self.POOL_MODEL = pool
        self.meta = meta
        
    def create(self, **kwargs):
        self.args = kwargs.copy()
        self.uuid = str(uuid.uuid1())
        self.timestamp = long(time.time() * 1e6)
        self.args['timestamp'] = str(self.timestamp)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.POOL_MODEL.insert(self.uuid, self.args)

    @classmethod
    def get(cls, pool_model, uuid):
        return pool_model.get(uuid)

    def to_dict(self):
        return self.args

    def __str__(self):
        return '<%s data:(%s)>' % (self.meta, str(self.args))

class MULTIMEDIA(ModelBase):
    def __init__(self):
        super(MULTIMEDIA, self).__init__(MULTIMEDIA_POOL, 'MULTIMEDIA')

    @classmethod
    def get(cls, uuid):
        return super(MULTIMEDIA, cls).get(MULTIMEDIA_POOL, uuid)

class LIVE(ModelBase):
    def __init__(self):
        super(LIVE, self).__init__(LIVE_POOL, 'LIVE')

    @classmethod
    def get(cls, uuid):
        return super(LIVE, cls).get(LIVE_POOL, uuid)

class VOD(ModelBase):
    def __init__(self):
        super(VOD, self).__init__(VOD_POOL, 'VOD')

    @classmethod
    def get(cls, uuid):
        return super(VOD, cls).get(VOD_POOL, uuid)

class EDGENODE(ModelBase):
    def __init__(self):
        super(EDGENODE, self).__init__(EDGE_POOL, 'EDGENODE')

    @classmethod
    def get(cls, uuid):
        return super(EDGENODE, cls).get(EDGE_POOL, uuid)

class CDNCOUNTRY(ModelBase):
    def __init__(self):
        super(CDNCOUNTRY, self).__init__(CDNCOUNTRY_POOL, 'CDNCOUNTRY')

    def create(self, args):
        self.uuid = str(uuid.uuid1())
        self.args = args
        CDNCOUNTRY_POOL.insert(self.uuid, self.args)
    @classmethod
    def get(cls, uuid):
        return super(CDNCOUNTRY, cls).get(CDNCOUNTRY_POOL, uuid)

class FARM(ModelBase):
    def __init__(self):
        super(FARM, self).__init__(FARM_POOL, 'FARM')

    @classmethod
    def get(cls, uuid):
        return super(FARM, cls).get(FARM_POOL, uuid)
