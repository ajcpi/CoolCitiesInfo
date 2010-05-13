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
SUMCOLUMNS = (('name', '', ''),
('web_site', 'GIW', "City's Green Initiative Website"),
('ghg_inventory', 'GGI', 'Greenhouse Gas inventory'),
('climate_action_plan', 'CAP', 'Climate Action Plan'),
('sustainability_plan', 'SP', 'Sustainability Plan'),
('green_team', 'GT', 'Green team'),
('environmental_concerns_committee', 'ECC', 'Environmental Concerns Committee'),
('green_ribbon_panel', 'GRP', 'Green Ribbon Panel'),
('Energy_efficiency', 'EE', 'Energy Efficiency'),
('green_buildings', 'GB', 'Green Builings'),
('renewable', 'RE', 'Renewable'),
('revolving_loan', 'RL', 'Revolving Loan'),
('biking_transportation', 'B/T', 'Biking/ Transportaion'),
('green_fleets', 'GF', 'Green Fleets'),
('codes_policies_regulations', 'C/P/R', 'Codes/ Policies/ Regulations'),
('comed_challenge', 'CE', 'ComEd Challenge'),
)
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
        fnames, cText, htext = zip(*SUMCOLUMNS)
        furls = [ '<a href="/with/%s" title="%s">%s</a>' % (x[0], x[2], x[1]) for x in SUMCOLUMNS if x[0] not in cityutils.SKIPFIELDS ]
        cList = []
        for c in cityList:
            cvals = []
            for f in fnames:
                v = getattr(c,f)
                if (v == ''):
                    cvals.append(v)
                elif (f == 'name'):
                    cvals.append({'sym':'<a href="/city/%s">%s</a>' % (urllib.quote(v), v)})
                else:
                    # cvals.append('+') 
                    cvals.append({'sym':cityutils.IMAGEURL, 'txt': v})
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
                eList.append('<a href="%s">%s</a>' % (url.strip(), label.strip()))

        self.response.out.write(template.render('templates/summary.html', 
                                                    {'announcements':aList, 
                                                     'externals':eList,
                                                     'cList':cList, 
                                                     'fields':furls,
                                                     'key': SUMCOLUMNS,
                                                     }))                