from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import model
import cityutils

class CityDetail(webapp.RequestHandler):
    def get(self):
            pparts = self.request.path_info.split('/')
            city = pparts[2]
            query = model.City.all()
            cityList = []
            for c in query:
                cityList.append(c.name)
                if c.name == city:
                    theCity = c
                    groups = {'contact_info':[], 
                              'plan_info': [], 
                              'action_info':[]}
                    for field, cl, printname in model.atList:
                        if field in cityutils.SKIPFIELDS:
                            continue
                        value = getattr(theCity, field)
                        value = cityutils.listifyString(value)
                        if field == 'web_site':
                            value = cityutils.urlify(value)
                        groups[cl].append((field, value, printname))


            self.response.out.write(template.render('templates/city.html', 
                   {'name':theCity.name, 'cityList':cityList, 'groups':groups}))

