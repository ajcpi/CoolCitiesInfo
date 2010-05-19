import urllib 

LINELENGTH = 60
COLORCLASS = ["darkrow", "lightrow"]
IMAGEURL = '<img src="/static/Anselmus_Green_Checkmark.png" alt="+" width="20" height="20"/>'
ONEDAY = 24*60*60
LISTABLE = ('Energy_efficiency', 
            'renewable', 
            'green_fleets', 
            'codes_policies_regulations',
            'comment',
            'more_comments')
SKIPFIELDS = ('email', 'city_email')

SUMCOLUMNS = (
('name', 'City', 'City'),
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
('biking_transportation', 'B_T', 'Biking/ Transportaion'),
('green_fleets', 'GF', 'Green Fleets'),
('codes_policies_regulations', 'C_P_R', 'Codes/ Policies/ Regulations'),
('comed_challenge', 'CE', 'ComEd Challenge'),
)

def listifyString(s):
    """Replace '*' in the string with items in an unnumbered list in html syntax"""
    if s.find('*') < 0:
        return s
    return s.replace('*', '</li><li>').replace('</li>', '<ul>', 1) + '</ul>'

def urlify(s):
    """turn any http:// strings into anchors"""
    if not s:
        return ''
    s = s.replace('\n', ' ').replace('\t', ' ')
    ustart = max(s.find('http://'), 0)
    qstart = ustart + 7
    uend = len(s)
    ulen =  s[ustart:].find(' ')
    if ulen > 0:
        uend = ustart + ulen
    neww =  '%s<a href="http://%s">%s</a>%s' % \
            (s[:ustart], urllib.quote(s[qstart:uend]), s[ustart:uend], s[uend:])
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
