from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import model
import loadData


class DebugInfo(webapp.RequestHandler):
    def get(self):
        #self.response.out.write( self.request.path_info)
        #self.response.out.write( self.request.script_name)
        #self.response.out.write( self.request.query_string)
        for k in dir(self.request):
            self.response.out.write( k + ':\t' + str(getattr(self.request, k)) + '<br>' )


class ClearCache(webapp.RequestHandler):
    def get(self):
        memcache.delete('summpage')
        self.response.out.write( 'memcache cleared')


class ReloadData(webapp.RequestHandler):
    def get(self):
        cities=model.City.all()
        loadData.clearData(self.response, cities)
        loadData.loadData(self.response)
        self.response.out.write( 'data reloaded')
        
class ClearData(webapp.RequestHandler):
    def get(self):
        cities=model.City.all()
        loadData.clearData(self.response, cities)
        self.response.out.write( 'data reloaded')