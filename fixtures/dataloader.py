import time, pycassa, uuid, models
from random import choice, randint

VODS_UUIDS, LIVES_UUIDS = [], []

def create_multimedia_samples(qtd):
    """docstring for create_multimedia_samples
    MultiMedia = {
      'jkl':{
        name:"media1",duration:100, 
        timestamp:{vod-uuid:12345, timestamp:'1231313'},
        timestamp:{vod-uuid:6789, timestamp:'213901238'},
      },
      'qito':{
        name:'live-guadalajara',
        timestamp:{live-uuid:567y},
        timestamp:{live-uuid:r611z},
        timestamp:{live-uuid:fr42z},
      }
    }
    """
    POOLS = {'live':LIVES_UUIDS, 'vod': VODS_UUIDS}
    def add_multimedia(type, qtd):
        for x in range(qtd):
            duration = randint(100, 900)
            values= {'name':'Multimedia com o name(%s)' % x, 'type': type}
            t_uuid = uuid.uuid1()
            for i in range(choice([1,2,3])):
                _uuid = choice(POOLS[type])
                POOLS[type].remove(_uuid)
                if POOLS[type] == 'vod':
                    values['duration'] = duration
                values['%s_%i' % (t_uuid, i)] = _uuid

            multimedia = models.MULTIMEDIA()
            multimedia.create(**values)
    add_multimedia('vod',qtd)
    add_multimedia('live',qtd)
def create_vod_samples(qtd):
    """docstring for create_vod_samples
    VOD = {
      12345:{type:'flv', profile:'DR_123', file:'arquivo.flv', quality:'SD', timestamp:'18293201839021'},
      6789:{type:'flv',  profile:'DR_123', file:'arquivo2.flv', quality:'HD', timestamp:'18293201839091'},
      abcd:{type:'flv', profile:'PARCEIROS',file:'arquivo3.flv', quality:'SD', timestamp:'18293201839061'},
    }
    """
    profiles = ['DR_123','PARCEIROS']
    exts = ['MP4', 'FLV']
    qualities = ['SD', 'HD']
    for x in range (qtd):
        ext = choice(exts)
        profile = choice(profiles)
        quality = choice(qualities)
        values = {'type':ext, 'profile':profile, 'file':'arquivo %i.%s' % (x,ext), 'quality': quality}
        vod = models.VOD()
        vod.create(**values)
        VODS_UUIDS.append(vod.uuid)
        print models.VOD.get(vod.uuid)

def create_live_samples(qtd):
    """docstring for create_live_samples
    LIVE = {
      567y:{bitrate:700, group:'1', stream_id:'1150', stream_layer:'1'},
      r611z:{bitrate:850, group:'1', stream_id:'1150', stream_layer:'2'},
      fr42z:{bitrate:2500, group:'2', stream_id:'1150', stream_layer:'4', ishd:1},
    }
    """
    bitrates = [350,550,700,850,1500,2500]
    groups = [1,2,3,4]
    
    for x in range (qtd):
        bitrate = str(choice(bitrates))
        group = str(choice(groups))
        stream = str(x*1000)
        stream_layer = str(choice(groups))
        ishd = str(choice([0,1]))
        values = {'bitrate':bitrate, 'group':group, 'stream_id':stream, 
                  'stream_layer':stream_layer, 'ishd':ishd}
        live = models.LIVE()
        live.create(**values)
        LIVES_UUIDS.append(live.uuid)
        print models.LIVE.get(live.uuid)


EDGES_UUIDS = []
def create_edgenode_samples(qtd):
    '''
    EDGENODE = {
        'a1s2d9':{
            description:'VIRTUA-07-BHZ',
            ipv4:'10.125.9.165', 
            ipv6:'fe80::22:56c6%en1',
            country:'BR', state:'SP',
            mem-usage:'4gb', mem-total:'16gb', 
            space-usage:'100GB', space-total:'500GB'
        },
    }
    '''
    COUNTRIES = ['BR','USA','AR','CL','MX','DEFAULT']
    STATES = ['CR','AL','RS','SP','PE']
    DATACENTERS = ['AMAZON','VIRTUA','EMBRATEL','INTELIG','TELEFONICA','TERRA-POA','TERRA-SAO'] 
    for x in range(qtd): 
        for n in range(randint(1, len(DATACENTERS))):
            values = {
                'description': '%s-%i' % (DATACENTERS[n], x),
                'ipv4': '%i.%i.%i.%i' % (randint(10,255),randint(30,255),\
                                        randint(10,255),randint(50,255)),
                'ipv6': 'fe80::22:56:%i' % randint(10,20000),
                'country': choice(COUNTRIES),
                'state': choice(STATES),
                'mem-used': '%sGB' % randint(1,10),
                'mem-total': '10GB',
                'space-used': '%sGB' % randint(15,500),
                'space-total': '500GB'
            }
            edge = models.EDGENODE()
            edge.create(**values)
            print models.EDGENODE.get(edge.uuid)
            EDGES_UUIDS.append(edge.uuid)

FARMS_UUIDS = []
def create_samples_farm(qtd):
    '''
    FARM = {
      'VIRTUA' :{
        disabled:1,
        order:1
        timestamp:'a1s2d3',
        timestamp:'a1s2d9',
      },
      'MIA':{
        timestamp:'v1v2v3v4b5'
      },
      'AMAZON':{
        timestamp:'v1v2v3v4b5'
      }
    }
    '''
    for x in range(qtd): 
        values = { 'name': 'FARM_%s' % x, 'order': str(randint(1,qtd))}
        t_uuid = uuid.uuid1()
        if randint(0,2) < 1:
            values['disabled'] = '1'
        time.sleep(0.1)
        n_uuids = list(EDGES_UUIDS)
        for n in range(randint(1, 10)):
            _uuid = choice(n_uuids)
            n_uuids.remove(_uuid)
            values['%s_%i' % (t_uuid, n)] = _uuid
        farm = models.FARM()
        farm.create(**values)
        print models.FARM.get(farm.uuid)
        FARMS_UUIDS.append(farm.name)
def create_samples_cdncountry():
    """
    docstring for create_samples_cdncountry
    CDNCountry = {
      'BR':{
        12930128930128390:{farm:'VIRTUA', order:1}
        12930128930128390:{farm:'MIA', order:2}
      },
      'USA':{
        12930128930128390:{farm:'MIA', order:1}
        12930128930128390:{farm:'VIRTUA', order:3}
        12930128930128390:{farm:'AMAZON', order:2}
      }
    }
    """
    COUNTRIES = ['BR','USA','AR','CL','MX','DEFAULT']
    for x in COUNTRIES: 
        t_uuid = uuid.uuid1()
        time.sleep(0.1)
        values = {}
        for n in range(randint(1,3)):
            values['%s_%i' % (t_uuid, n)] = {'farm': choice(FARMS_UUIDS),'order': str(randint(1,3))}
        cdncountry = models.CDNCOUNTRY()
        cdncountry.create(values)
        print models.CDNCOUNTRY.get(cdncountry.uuid)

    

def initialize():
    factor = 100
    create_vod_samples(6*factor)
    create_live_samples(6*factor)
    create_multimedia_samples(1*factor)
    create_edgenode_samples(10*factor)
    create_samples_farm(1*factor)
    create_samples_cdncountry()
if __name__ == '__main__':
    initialize()