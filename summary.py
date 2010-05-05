import cgi
import urllib
import logging
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import model
import loadData
import cityutils

class SummaryHandler(webapp.RequestHandler):
    def get(self):
        summpage = memcache.get('summpage')
        if summpage is None:
            summpage = self.render_summpage()
            if not memcache.add('summpage', summpage, cityutils.ONEDAY):
                logging.error('memcache set failed')
        self.response.out.write(summpage)

    def render_summpage(self):
        cityList = model.City.all()
        fnames, cls, fieldList = zip(*model.atList)
        furls = [ '<a href="/with/%s">%s</a>' % (x[0], x[2]) for x in model.atList if x[0] not in cityutils.SKIPFIELDS ]
        cList = []
        for c in cityList:
            cvals = []
            for f in fnames:
                if f in cityutils.SKIPFIELDS:
                    continue
                v = getattr(c,f)
                if (v == ''):
                    cvals.append(v)
                elif (f == 'name'):
                    cvals.append('<a href="/city/%s">%s</a>' % (urllib.quote(v), v))
                else:
                    # cvals.append('+') 
                    cvals.append(cityutils.IMAGEURL)
            cList.append(cvals)
            #
            # collect internal announcements
            #
            aments = file('links/announcements.list').readlines()
            aList = []
            for a in aments:
                url, label = a.split('|')
                aList.append('<a href="/static/%s">%s</s>' % (url.strip(), label.strip()))
            #
            # collect external links
            #
            externals = file('links/externals.list').readlines()
            eList = []
            for e in externals:
                url, label = e.split('|')
                eList.append('<a href="%s">%s</s>' % (url.strip(), label.strip()))

        self.response.out.write(template.render('templates/summary.html', 
                                                    {'announcements':aList, 
                                                     'externals':eList,
                                                     'cList':cList, 
                                                     'fields':furls }))                