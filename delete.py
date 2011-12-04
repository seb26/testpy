# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import wikitools
from wikitools import pagelist
import wconfig

f = open('delete.txt', 'rb')

# Setup wiki
config = wconfig.config['tfwiki']
print 'Logging in.'
wiki = wikitools.Wiki(config['url-api'])
wiki.login(config['usr'], config['pwd'])
print 'Logged in.'

rawlist = [ line.strip() for line in f ]
rawlist.sort()

pageobjs = pagelist.listFromTitles(wiki, rawlist)

stats = { 'deleted': [], 'failed': [] }

for page in pageobjs:
    if page.exists:
        delete = page.delete(reason='auto: unused file, replaced by file at proper name (see [[Comics/ru]])')
        print page.title, '> deleted.'
        stats['deleted'].append(page)
    else:
        print page.title, '> does not exist.'
        stats['failed'].append(page)

print 'Done ~ {0} pages total, {1} deleted, {2} failed. Print `stats` from interpreter to view.'.format(
    len(pageobjs),
    len(stats['deleted']),
    len(stats['failed'])
    )