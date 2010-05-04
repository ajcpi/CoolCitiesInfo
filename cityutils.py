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
SKIPFIELDS = ('name', 'email', 'phone_email')

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
