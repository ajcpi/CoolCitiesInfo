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
        furls = [ '<a href="/with/%s">%s</a>' % (x[0], x[2]) for x in model.atList ]
        cList = []
        for c in cityList:
            cvals = []
            for f in fnames:
                if f in ('email', 'phone_email'):
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
        return template.render('templates/summary.html', { 'fields':furls, 'cList':cList})
