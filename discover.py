#!/usr/bin/env python

__author__ = 'Andrew Gwozdziewycz'
__email__ = 'web@apgwoz.com'
__license__ = 'GPLv3'

import sys
import codecs

from urllib import urlopen
from urlparse import urljoin
from pyquery import PyQuery as P
import feedparser

OPMLENV = """<opml version="1.1">
<head><title>Quora Feeds</title>
<dateCreated>2013-10-10 06:22:36.131417</dateCreated>
<dateModified>2013-10-10 06:22:36.131417</dateModified>
</head>
<body>
%s
</body>
</opml>
"""
OUTLINE = """
<outline htmlUrl="%(url)s" 
         text="%(title)s" 
         title="%(title)s" 
         type="rss" 
         version="RSS" 
         xmlUrl="%(alt)s" />
"""


def openpage(url):
    content = urlopen(url).read()
    return P(content)

def findalt(d):
    nodes = d.find('link[rel="alternate"]')
    if nodes:
        return nodes[0].attrib.get('href')
    return None

def readalt(alt):
    d = feedparser.parse(alt)
    return d

def readall(fname):
    alts = []
    with open(fname) as f:
        for line in f:
            name, url = line.strip().split('\t')
            try:
                d = openpage(url)
            except Exception, x:
                print >>sys.stderr, "Couldn't open %s at %s -- %s" % (name, url, x)
                continue

            alt = findalt(d)
            if alt:
                if not alt.startswith('http'):
                    alt = urljoin(url, alt)
                
                print >>sys.stderr, "ALT for '%s' at: %s" % (url, alt)
                try:
                    doc = readalt(alt)
                    alts.append({
                        'alt': alt,
                        'url': url,
                        'title': doc['feed']['title']
                    })
                except Exception, e:
                    print >>sys.stderr, "Couldn't read alt for '%s': %s" % (alt, e)
                    continue
            else:
                print >>sys.stderr, "Couldn't find an alt for '%s'" % url

    return alts
            

def opml(alts):
    return OPMLENV % '\n'.join(map(lambda x: OUTLINE % x, alts))

            
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, "usage: %s input out.opml" % sys.argv[0]
        raise SystemExit()
    alts = readall(sys.argv[1])
    with codecs.open(sys.argv[2], 'w', 'utf8') as f:
        f.write(opml(alts))
