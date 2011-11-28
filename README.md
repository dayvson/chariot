# TheChariot
------------

TheChariot is a project to deliver the video url in our Content Delivery Network (CDN)
Select the best mirror for the user by his IP. Using MaxMind geolocation API and another internal database
with ip's ranges and subnet mask from operators telecom. Using CASSANDRA as database


Most of the magic happens in chariot/models.py, so check that out.

## Installation
---------------

Installing TheChariot is fairly straightforward.  Really it just involves
checking out Cassandra and TheChariot, doing a little configuration, and
then starting it up.  Here's a roadmap of the steps we're going to take to
install the project:

1. Check out the latest Cassandra source code
2. Check out the TheChariot source code
3. Install and configure Cassandra
4. Install Thrift
5. Create a virtual Python environment with TheChariot's dependencies
6. Start up the webserver

### Check out the TheChariot source code
----------------------------------------

    git clone git://github.com/dayvson/chariot.git

### Linux :: Cassandra from Source

#### Check out the latest Cassandra source code
-----------------------------------------------

    git clone git://git.apache.org/cassandra.git

#### Install and configure Cassandra
------------------------------------
Now build Cassandra:

    cd cassandra
    ant

Then we need to create our database directories on disk:

    sudo mkdir -p /var/log/cassandra
    sudo chown -R `whoami` /var/log/cassandra
    sudo mkdir -p /var/lib/cassandra
    sudo chown -R `whoami` /var/lib/cassandra

Finally we can start Cassandra:

    ./bin/cassandra -f

### Windows :: Cassandra from Binaries
--------------------------------------

TBD

### Create a virtual Python environment with TheChariot's dependencies
----------------------------------------------------------------------

First, make sure to have virtualenv installed.  If it isn't installed already,
this should do the trick:

    sudo easy_install -U virtualenv

Now let's create a new virtual environment, and begin using it:

    virtualenv chariot
    source chariot/bin/activate

We should install pip, so that we can more easily install TheChariot's
dependencies into our new virtual environment:

    easy_install -U pip

Now let's install all of the dependencies:

    pip install -U -r chariot/requirements.txt

Now that we've got all of our dependencies installed, we're ready to start up
the server.

### Create the schema
---------------------

Make sure you're in the TheChariot checkout, and then run the schema
command to create the proper keyspace in Cassandra:

    cd chariot
    python data/schema.py

### Start up the webserver
--------------------------

This is the fun part! We're done setting everything up, we just need to run it:

    python chariot.py

Now go to http://127.0.0.1:8000/ and you can play with TheChariot!

## Schema Layout
----------------

In Cassandra, the way that your data is structured is very closely tied to how
how it will be retrieved.  Let's start with the VOD/LIVE/MULTIMEDIA ColumnFamilies. 

VOD = {
  'V-UUID-123':{type:'flv', profile:'DR_123', file:'arquivo.flv', quality:'SD', timestamp:'18293201839021'},
  'V-UUID-124':{type:'flv',  profile:'DR_123', file:'arquivo2.flv', quality:'HD', timestamp:'18293201839091'},
  'V-UUID-125':{type:'flv', profile:'partner',file:'arquivo3.flv', quality:'SD', timestamp:'18293201839061'},
}

LIVE = {
  'L-UUID-456':{"bitrate":"700", "group":"1", "streamId":"1150", "streamLayer":"1"},
  'L-UUID-457':{"bitrate":"850", "group":"1", "streamId":"1150", "streamLayer":"2"},
  'L-UUID-458':{"bitrate":"2500", "group":"2", "streamId":"1150", "streamLayer":"4", "ishd":"1"}
}

MultiMedia = {
  "MULTIMEDIA-UUID-900":{
    'name':"Noticia do acidente tal",
    'duration':'100', 
    "type": "VOD",
    "delivery":"HTTP"
    'M-UUID-987':{"vod-uuid":'V-UUID-123', "timestamp":'1231313'},
    'M-UUID-987':{"vod-uuid":'V-UUID-125', "timestamp":'213901238'}
  },
  "MULTIMEDIA-UUID-900":{
    'name':"Nemo",
    'duration':'100', 
    "type": "VOD",
    "delivery":"RTMPE"
    'M-UUID-987':{"vod-uuid":'V-UUID-123', "timestamp":'1231313'},
    'M-UUID-987':{"vod-uuid":'V-UUID-125', "timestamp":'213901238'}
  },
  "MULTIMEDIA-UUID-902":{
    "name":'live-guadalajara',
    "type": "LIVE",
    "delivery":"RTMP"
    "L-UUID-765":{"live-uuid":"L-UUID-456"},
    "L-UUID-764":{"live-uuid":"L-UUID-458"},
    "L-UUID-763":{"live-uuid":"L-UUID-457"}
  }
}

EDGENODE = {
  'a1s2d9':{
    description:'VIRTUA-07-BHZ',
    
    HOST:{
      ipv4:{
        RTMP:'10.10.101.1',
        RTMPE:'10.10.101.1'
        HTTP: '10.125.9.165', 
        SMOOTH: '1.1.1.1',
      },
      ipv6:{
        HTTP: '10.125.9.165', 
      }
    }
    location:{country:'BR', state:'SP'},
    machine:{mem-usage:'4gb', mem-limit:'16gb', 'cpu':'50%', 'cpu-limit':'80%'
            'bandwith-usage': '1GB', 'bandwith-total': '5GB', 
            }
  },
  'a1s2d3':{
    description:'VIRTUA-08-BHZ',
    ipv4:'10.225.16.165',
    location:{country:'BR', state:'RS'},
    ipv6:'fe80::226:bbff:fe17:56c6%en1',
    machine:{mem-usage:'4gb', mem-limit:'16gb', 'cpu':'50%', 'cpu-limit':'80%'
            'bandwith-usage': '1GB', 'bandwith-total': '5GB', 
            }
  },
  'v1v2v3v4b5':{
    description:'MIA-03',
    disable:1,
    ipv4:'10.225.16.165', 
    location:{country:'USA', state:'FLORIDA'}
    ipv6:'fe17:56c6%en1',
    machine:{mem-usage:'4gb', mem-limit:'16gb', 'cpu':'50%', 'cpu-limit':'80%'
            'bandwith-usage': '1GB', 'bandwith-total': '5GB', 
            }
  }
  'amz01':{
    description:'AMZ-02',
    ipv4:'78.30.16.165', 
    location:{country:'USA', state:'VIRGINIA'}
    ipv6:'fe17:56c6%en1',
    machine:{mem-usage:'4gb', mem-limit:'16gb', 'cpu':'50%', 'cpu-limit':'80%'
            'bandwith-usage': '1GB', 'bandwith-total': '5GB', 
            }
  
  }
}

//EdgeNode.multiget(['a1s2d9', 'a1s2d3'])
CDNCountry = {
  'BR':{
    12930128930128390:{
      farm:'FARM-DEFAULT', 
      order:1
    },
    12930128930128390:{farm:'MIA'}
  },
  'CL':{
    12930128930128390:{farm:'AMAZON', order:2}
  },
  'USA':{
    12930128930128390:{farm:'AMAZON', order:2},
    12930128930128390:{farm:'FARM2-GVT', order:2}
  },
  'DEFAULT':{
    12930128930128390:{farm:'FARM-DEFAULT', order:1}
    12930128930128390:{farm:'TLF', order:2}
  }
}

IPRANGES = {
  'VIRTUA':{
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'}
  },
  'GVT':{
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
  },
  'BRT':{
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
  },
  'TLF':{
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
    uuid:{submask:'10.101.101.1', subnet:'255.255.255.0'},
  }
}


FARM = {
  'FARM1-GVT' :{
    current_bandwith:'4GB(em bits ou bytes)',
    max_bandwith:'8GB(em bits ou bytes)',
    disabled:1,
    ranges:{
      range_uuid:{IPRANGE:'VIRTUA', order:1}
      range_uuid:{IPRANGE:'GVT', order:2}
      range_uuid:{IPRANGE:'BRT', order:3}      
    }
    timestamp:'a1s2d3',
    timestamp:'a1s2d9',
  },
  'FARM2-GVT':{
    ranges:{
      range_uuid:{IPRANGE:'GVT', order:3}
    }
    timestamp:'v1v2v3v4b5'
  },
  'FARM1-BRT':{
    timestamp:'v1v2v3v4b5'
  },
  'FARM-DEFAUL:{
     timestamp:'v1v2v3v4b5'
  },
  'MIA':{
     timestamp:'v1v2v3v4b5'
  }
}
