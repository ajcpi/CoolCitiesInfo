from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import urllib

import model

class CitiesWith(webapp.RequestHandler):
    def get(self):
            cities = model.City.all()
            theAttr = self.request.path_info.split('/')[2]
            hasList = []
            cityList = []
            for c in cities:
                cityList.append(c.name)
                val = getattr(c, theAttr)
                if val != '':
                    hasList.append( { 'name':'<a href="/city/%s">%s</a>' % \
                        (urllib.quote(c.name), c.name), 'value':val})
            self.response.out.write(template.render('templates/attribute.html', 
                                    { 'cityList':cityList, 'hasList':hasList}))
            return
