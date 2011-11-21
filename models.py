import time, pycassa
from pycassa.cassandra.ttypes import NotFoundException
from pycassa.pool import ConnectionPool

__all__ = ['MMediaModel', 'SourceModel']
POOL = pycassa.connect('Chariot')

MMEDIA = pycassa.ColumnFamily(POOL, 'MMedia')
SOURCES = pycassa.ColumnFamily(POOL, 'Sources')
MIRRORS = pycassa.ColumnFamily(POOL, 'Mirrors')

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


class SourceModel(object):
    id = 0
    name = ''
    source =''
    
    def create(self, id=None, name=None, source=None):
        self.id = id
        self.name = name
        self.source = source
    
    def to_dict(self):
        result = {
            'id':self.id,
            'name':self.name,
            'source':self.source
        }
    def __str__(self):
        return '<SourceModel id:(%s) name:(%s)>' % (self.id, self.name)
    
class MMediaModel(object):
    id = 0
    name = ""
    profile = ""
    file_name = ""
    file_size = 0
    ext = "MP4"
    source = 0
    
    def create(self, id=None,name=None,profile=None,file_name=None,file_size=None,ext=None,source=None):
        self.id = id
        self.name = name
        self.profile = profile
        self.file_name = file_name
        self.file_size = file_size
        self.ext = ext
        self.source = source
        
    def to_dict(self):
        result = {
            'id':str(self.id), 'ext': self.ext,
            'name':self.name, 'source': str(self.source),
            'profile': self.profile,
            'file_name': self.file_name,
            'file_size': str(self.file_size)
        }
        return result
        
    def __str__(self):
        return u'<MMedia Model id:(%s) name:(%s)' % (str(self.id), str(self.name))
