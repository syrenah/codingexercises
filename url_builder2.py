
from urllib.parse import urlencode
class URLBuilder:
    def __init__(self):
        self._host=""
        self._protocol="http"
        self._port=80   #443 for https
        self._path=""
        self._query_params={}

    def set_query_params(self,key,value):
        self._query_params[key]=value
        return self
    
    def set_path(self,path):
        self._path=path
        return self
    

    def set_host(self,host):
        self._host=host
        return self

    def set_protocol(self,protocol):
        self._protocol=protocol
        if protocol=="https":
            self._port=443
        else:
            self._port=80

        return self

    def set_port(self,port):
        self._port=port
        return self


    def build(self):
        url=self._protocol+"://" + self._host
        url=url+ ":" + str(self._port)
        url=url+urlencode(self._query_params)
        return url



url =URLBuilder().set_host("example.some.com").set_query_params("key", "value").build()
print(url)