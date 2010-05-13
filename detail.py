from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import model
import cityutils

    

class CityDetail(webapp.RequestHandler):
    def getCityList(self):
        cityList = memcache.get('cityList')
        if cityList is None:
            query = model.City.all()
            cityList = []
            for c in query:
                cityList.append(c.name)
            if not memcache.add('cityList', cityList, cityutils.ONEDAY):
                logging.error('memcache set failed')
        return cityList
    def get(self):
            pparts = self.request.path_info.split('/')
            city = pparts[2]
            query = model.City.all()
            for c in query:
                if c.name == city:
                    theCity = c
                    groups = {'contact_info':[], 
                              'plan_info': [], 
                              'action_info':[]}
                    for field, cl, printname in model.atList:
                        if field in cityutils.SKIPFIELDS + ('name',):
                            continue
                        value = getattr(theCity, field)
                        value = cityutils.listifyString(value)
                        if field == 'web_site' and value != '':
                            value = cityutils.urlify(value)
                        groups[cl].append((field, value, printname))


            self.response.out.write(template.render('templates/city.html', 
                   {'name':theCity.name, 'cityList':self.getCityList(), 'groups':groups}))

