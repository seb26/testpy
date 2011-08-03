# -*- coding: utf-8 -*-

import wikitools
from wikitools import wiki, api
import config
import re

qlimit = config.default_limit
qnamespace = config.default_ns

wiki = wikitools.Wiki(config.apiurl)

def userStats():
    params = {
        'action': 'query',
        'meta': 'userinfo',
        'uiprop': 'groups'
        }
    req = api.APIRequest(wiki, params)
    res = req.query()
    print u'Welcome %s (ID:%s) %s' % (
        res['query']['userinfo']['name'],
        res['query']['userinfo']['id'],
        res['query']['userinfo']['groups'][:]
        )

def login():
    print 'Logging in as %s...' % config.username
    if not wiki.login(config.username, config.password, remember=True):
        pass
    userStats()


def logout():
    if wiki.logout():
        print 'Logged out.'

def getCategory(title, namespace=qnamespace, sort='sortkey', ts_start=False, ts_end=False, sk_start=False, sk_end=False, sk_only=False, cdir=False, limit=qlimit, qcontinue=True):
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': title,
        'cmlimit': limit,
        }
    if sort == 'timestamp':
        params['cmsort'] = 'timestamp'
        if ts_start:
            params['cmstart'] = ts_start
        if ts_end:
            params['cmend'] = ts_end
    else:
        params['cmsort'] = 'sortkey'
        if sk_start:
            params['cmstartsortkey'] = sk_start
        if sk_end:
            params['cmendsortkey'] = sk_end
        if sk_only:
            # Limit results to only a particular sortkey (defined by sk_only).
            # Handy for language-sorted categories.
            params['cmstartsortkey'] = sk_only
            params['cmendsortkey'] = sk_only
    if cdir:
        if cdir == 'asc':
            params['cmdir'] = 'asc'
        elif cdir == 'desc':
            params['cmdir'] = 'desc'

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)

    getCategory_l = []

    for j in res['query']['categorymembers']:
        getCategory_l.append(j['title'])
    return getCategory_l

def getPages(namespace=qnamespace, filterredir='nonredirects', limit=qlimit, qcontinue=True, lang=True):
    params = {
        'action': 'query',
        'list': 'allpages',
        'apnamespace': namespace,
        'apfilterredir': filterredir,
        'aplimit': limit
        }
    if filterredir:
        if filterredir in ('all', 'redirects', 'nonredirects'):
            params['apfilterredir'] = filterredir

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)
    getPages_l = []
    reLang = re.compile(r'\/(ar|cs|da|de|es|fi|fr|hu|it|ja|ko|nl|no|pl|pt|pt-br|ro|ru|sv|tr|zh-hans|zh-hant)')
    for j in res['query']['allpages']:
        if lang:
            getPages_l.append(j['title'])
        else:
            if not reLang.search(j['title']):
                getPages_l.append(j['title'])
    return getPages_l

def getFiles(namespace=qnamespace, filterredir='nonredirects', limit=qlimit, qcontinue=True):
    """
    getFiles: gets pages in the File namespace (NS:6).

    Original intention was to have a 'fileType' value to limit to certain file
    types, but it is perhaps better to include all filetypes in the result and
    then offer manual filtering in the listmaker later.
    """
    params = {
        'action': 'query',
        'list': 'allpages',
        'apnamespace': '6',
        'apfilterredir': filterredir,
        'aplimit': limit
        }
    if filterredir:
        if filterredir in ('all', 'redirects', 'nonredirects'):
            params['apfilterredir'] = filterredir

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)
    getFiles_l = []
    for j in res['query']['allpages']:
        getFiles_l.append(j['title'])
    return getFiles_l

def getTransclusions(title, namespace=qnamespace, filterredir='nonredirects', limit=qlimit, qcontinue=True):
    params = {
        'action': 'query',
        'list': 'embeddedin',
        'eititle': title,
        'eilimit': limit
        }
    if filterredir:
        if filterredir in ('all', 'redirects', 'nonredirects'):
            params['eifilterredir'] = filterredir

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)
    getTransclusions_l = []
    for j in res['query']['embeddedin']:
        getTransclusions_l.append(j['title'])
    return getTransclusions_l

def getDuplicates(title, limit=qlimit, qcontinue=True):
    # Part 1: get the SHA1 of the specified file.
    params_sha1 = {
        'action': 'query',
        'list': 'allimages',
        'aifrom': title,
        'ailimit': '1',
        'aiprop': 'sha1'
        }
    req_sha1 = api.APIRequest(wiki, params_sha1)
    res_sha1 = req_sha1.query(querycontinue=False) # False here, otherwise it'll keep querying 1 by 1 forever.
    title_sha1 = res_sha1['query']['allimages'][0]['sha1']

    # Part 2: use the SHA1 to list all other images with the same SHA1.
    params = {
        'action': 'query',
        'list': 'allimages',
        'ailimit': limit,
        'aisha1': title_sha1
        }
    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)
    getDuplicates_l = []

    # Finally: return the results in a list.
    for j in res['query']['allimages']:
        getDuplicates_l.append(j['name'])
    return getDuplicates_l

def whatLinksHere(title, namespace=False, filterredir=False, redirect=False, limit=qlimit, qcontinue=True):

    params = {
        'action': 'query',
        'list': 'backlinks',
        'bltitle': title,
        'bllimit': limit
        }
    if redirect:
        params['blredirect'] = '1'
    if filterredir:
        if filterredir in ('all', 'redirects', 'nonredirects'):
            params['blfilterredir'] = filterredir
    if namespace:
        params['blnamespace'] = namespace

    whatLinksHere_l = []

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)

    for j in res['query']['backlinks']:
        whatLinksHere_l.append(j['title'])
    return whatLinksHere_l

def whatUsesFile(title, namespace=False, filterredir=False, qcontinue=True, limit=qlimit):

    params = {
        'action': 'query',
        'list': 'imageusage',
        'iutitle': title,
        'iulimit': limit
        }

    if namespace:
        params['iunamespace'] = namespace
    if filterredir in ('all', 'redirects', 'nonredirects'):
        params['iufilterredir'] = filterredir

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)

    whatUsesFile_l = []

    for j in res['query']['imageusage']:
        whatUsesFile_l.append(j['title'])
    return whatUsesFile_l

def getImagesUsed(title, qcontinue=True, limit=qlimit):

    params = {
        'action': 'query',
        'titles': title,
        'prop': 'images',
        'imlimit': limit,
        'indexpageids': '1'
        }

    req = api.APIRequest(wiki, params)
    res = req.query(querycontinue=qcontinue)

    getImagesUsed_l = []

    for x in res['query']['pageids']:
        for j in res['query']['pages'][x]['images']:
            getImagesUsed_l.append(j['title'])
    return getImagesUsed_l

def run():
    print 'Hai'

if __name__ == '__main__':
	run()