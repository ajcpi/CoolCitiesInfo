import model
import csv

FIELDNAMES = [
"name",
"mayor",
"city_contact_name",
"Title",
"phone_email",
"cool_city_contact",
"email",
"ghg_inventory",
"climate_action_plan",
"sustainability_plan",
"green_team",
"web_site",
"environmental_concerns_committee",
"green_ribbon_panel",
"Energy_efficiency",
"green_buildings",
"renewable",
"revolving_loan",
"biking_transportation",
"green_fleets",
"codes_policies_regulations",
"comments",
"more_comments",
"comed_challenge"
    ]
    

def loadData(response):
    datfile = open('ccprof.csv')
    rdr = csv.DictReader(datfile, fieldnames=FIELDNAMES)
    
    for l in rdr:
        c = model.City(name=l['name'])
        response.out.write( 'Created ' + l['name'] +  '<br>')
        for k in l:
            if (k == "None") or (not k):
                continue
            setattr(c, k, l[k])
            c.put()
    datfile.close()
    
def clearData(response, cities):
    n = 0
    for c in cities:
        c.delete()
        n += 1
    response.out.write('cleared %d cities' % (n,))
    
        