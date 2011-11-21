class GeoLocation(object):
    def __init__(self, path_maxmind):
        self.geoip = pygeoip.GeoIP(path_maxmind)
        
    def get_country_code(self, ip):
        return self.geoip.country_code_by_addr(ip)