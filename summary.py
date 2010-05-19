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
        fnames, cText, htext = zip(*cityutils.SUMCOLUMNS)
        furls = [ '<a href="/with/%s" title="%s">%s</a>' % (x[0], x[2], x[1]) for x in cityutils.SUMCOLUMNS if x[0] not in cityutils.SKIPFIELDS ]
        cList = []
        for c in cityList:
            cvals = []
            for f, cText, hText in cityutils.SUMCOLUMNS:
                v = getattr(c,f)
                if (v == ''):
                    cvals.append({'name': cText, 'val':''})
                elif (f == 'name'):
                    cvals.append({'name': 'City', 'val': '<a href="/city/%s">%s</a>' % (urllib.quote(v), v)})
                    #cvals.append({'name': 'City', 'val': v})
                else:
                    #cvals.append({'name': cText, 'val':'+', 'txt': v}) 
                    cvals.append({'name': cText, 'val': cityutils.IMAGEURL, 'txt': v})
            cList.append(cvals)
            #
            # collect internal announcements
            #
            aments = file('links/announcements.list').readlines()
            aList = []
            for a in aments:
                url, label = a.split('|')
                aList.append('<a href="/static/%s">%s</a>' % (url.strip(), label.strip()))
            #
            # collect external links
            #
            externals = file('links/externals.list').readlines()
            eList = []
            for e in externals:
                url, label = e.split('|')
                if url:
                    eList.append('<a href="%s">%s</a>' % (url.strip(), label.strip()))
                else:
                    eList.append('<larger><bold>%s<bold></larger>' % (label,) )
        return (template.render('templates/summaryjq.html', 
                                                    {'announcements':aList, 
                                                     'externals':eList,
                                                     'cList':cList, 
                                                     'fields':furls,
                                                     'key': cityutils.SUMCOLUMNS,
                                                     }))
