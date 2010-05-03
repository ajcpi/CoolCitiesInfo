#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import users
from google.appengine.ext import db

import model
import loadData

LINELENGTH = 60
COLORCLASS = ["darkrow", "lightrow"]
IMAGEURL = '<img src="/static/Anselmus_Green_Checkmark.png" alt="+" width="20" height="20"/>'
def listifyString(s):
    """Replace '*' in the string with items in an unnumbered list in html syntax"""
    return s.replace('*', '</li><li>').replace('</li>', '<ul>', 1) + '</ul>'

def urlify(s):
    """turn any http:// strings into anchors"""
    s = s.replace('\n', ' ').replace('\t', ' ')
    ustart = s.find('http://')
    qstart = ustart + 7
    uend = len(s)
    ulen =  s[ustart:].find(' ')
    if ulen > 0:
        uend = ustart + ulen
    neww = s[:ustart] + '<a href="http://' + urllib.quote(s[qstart:uend]) + '">' + s[ustart:uend] + '</a>' + s[uend:]
    return neww

def breakString(s, ll):
    working = s
    lines = ''
    while len(working) >= ll:
        sp = working[:ll].rfind(' ')
        if sp <= 0:
            break
        lines += working[:sp] + '<br>'
        working = working[sp+1:]
    lines += working
    return lines
    
class SummaryHandler(webapp.RequestHandler):
    def get(self):
            cityList = model.City.all()
            fnames, cls, fieldList = zip(*model.atList)
            furls = [ '<a href="/with/%s">%s</a>' % (x[0], x[2]) for x in model.atList ]
            cList = []
            for c in cityList:
                cvals = []
                for f in fnames:
                    v = getattr(c,f)
                    if (v == ''):
                        cvals.append(v)
                    elif (f == 'name'):
                        cvals.append('<a href="/city/%s">%s</a>' % (urllib.quote(v), v))
                    else:
                        # cvals.append('+') 
                        cvals.append(IMAGEURL)
                cList.append(cvals)
            self.response.out.write(template.render('templates/summary.html', 
                                          { 'fields':furls, 'cList':cList}))


class DebugInfo(webapp.RequestHandler):
    def get(self):
        #self.response.out.write( self.request.path_info)
        #self.response.out.write( self.request.script_name)
        #self.response.out.write( self.request.query_string)
        for k in dir(self.request):
            self.response.out.write( k + ':\t' + str(getattr(self.request, k)) + '<br>' )

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
                        value = getattr(theCity, field)
                        if field == 'Energy_efficiency' or field == 'renewable':
                            value = listifyString(value)
                        if field == 'web_site':
                            value = urlify(value)
                        groups[cl].append((field, value, printname))


            self.response.out.write(template.render('templates/city.html', 
                   {'name':theCity.name, 'cityList':cityList, 'groups':groups}))

class ReloadData(webapp.RequestHandler):
    def get(self):
        loadData.loadData(self.response)
        self.response.out.write( 'data reloaded')

def main():
    application = webapp.WSGIApplication([('/', SummaryHandler),
                                          ('/city', SummaryHandler),
                                          ('/city/', SummaryHandler),
                                          ('/city/.*', CityDetail),
                                          ('/with', SummaryHandler),
                                          ('/with/', SummaryHandler),
                                          ('/with/.*', CitiesWith),
                                          ('/reload', ReloadData),
                                          ('/DebugInfo', DebugInfo)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
