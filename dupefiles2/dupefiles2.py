# -*- coding: UTF-8 -*-

import wikitools
import settings
import datetime
import time
import rawdata
from wikitools import wiki, api
from collections import defaultdict

print 'Logging in.'
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
print 'Logged in.'

report_title = settings.page_prefix + 'Duplicate files'

report_template = '''
List of all files with matching {{w|SHA-1}} hashes; %s unique files, <onlyinclude>%s</onlyinclude> duplicated files in total. Data as of %s.

== List ==
%s
'''

"""
res = { 'query': { 'allimages': [

    { 'name': 'FileA.png', 'sha1': '477c3d4234936fd32f02a08b9a76e902d3efd9c4' },
    { 'name': 'FileB.png', 'sha1': '477c3d4234936fd32f02a08b9a76e902d3efd9c4' },
    { 'name': 'FileX.png', 'sha1': 'bbc9033429c4132f236091f6ab18f70ebad863dc' },
    { 'name': 'FileY.png', 'sha1': 'bbc9033429c4132f236091f6ab18f70ebad863dc' },
    { 'name': 'FileZ.png', 'sha1': 'bbc9033429c4132f236091f6ab18f70ebad863dc' },
    { 'name': 'File0.png', 'sha1': 'da237d1c6232f27e0c1b5c59451664edf84f276f' }

    ] } }

"""
params = {
    'action': 'query',
    'list': 'allimages',
    'aiprop': 'sha1',
    'aplimit': '5000'
    }
print 'Getting API data.'
req = api.APIRequest(wiki, params)
res = req.query(querycontinue=True)
print 'Gottam.'

# res = rawdata.res

print 'Set out data into SHA1 index.'
sha1_index = defaultdict(list)
for f in res['query']['allimages']:
    name = f['name']
    sha1 = f['sha1']
    sha1_index[sha1].append(name) # Structure: ('hash', [ 'Foo.png', 'Bar.png' ])

print 'Preparing wikitext.'
i = 0
j = 0
output = []
w_format = u'# {{code|%s}} [[:File:%s]]'
for h in sha1_index.items():
    if len(h[1]) > 1: # Non-duplicates don't get through
        for z in h[1]:
            output.append(w_format % (h[0], z))
            j += 1 # The amount of duplicate files
        i += 1 # The amount of duplicated hashes
    else:
        pass

report = wikitools.Page(wiki, report_title)
current_time = (datetime.datetime.utcnow() - datetime.timedelta(seconds = 0)).strftime('%H:%M, %d %B %Y (UTC)')
report_text = report_template % (i, j, current_time, '\n'.join(output))
# report_text = report_text.encode('utf-8')
print 'Editing.'

report.edit(report_text, summary=settings.editsumm + ' (%s unique files, %s duplicates)' % (i, j), bot=1)
print 'Saved. All done.'