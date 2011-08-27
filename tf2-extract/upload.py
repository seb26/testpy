# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import wikitools
import os
import wikiUpload
import testpyconfig as config

uploader = wikiUpload.wikiUploader(config.username, config.password, config.url)

filelist = [
    'tf_danish.txt',
    'tf_dutch.txt',
    'tf_english.txt',
    'tf_finnish.txt',
    'tf_french.txt',
    'tf_german.txt',
    'tf_hungarian.txt',
    'tf_italian.txt',
    'tf_japanese.txt',
    'tf_korean.txt',
    'tf_norwegian.txt',
    'tf_polish.txt',
    'tf_portuguese.txt',
    'tf_romanian.txt',
    'tf_russian.txt',
    'tf_schinese.txt',
    'tf_spanish.txt',
    'tf_swedish.txt',
    'tf_tchinese.txt',
    'tf_turkish.txt'
    ]

def u(f, name, overwrite=False, reupload=False, summary=None):
    global uploader
    try:
        print 'upload():', f, 'uploading to', name, '...'
        uploader.upload(f, name, summary, overwrite=overwrite, reupload=reupload)
        print 'Attempted upload of %s | %s\n' % (f, name)
    except:
        print 'upload():', f, 'to', name, 'failed.'
        print 'error:upload() %s | %s\n' % (f, name)

def ux(flist, fdir, s):
    for f in flist:
        fpath = os.path.join(fdir, f)
        u(fpath, f.capitalize(), overwrite=True, reupload=True, summary=s)
        print fpath, f.capitalize(), s
    return True

print ux(filelist, r'X:\Sebi\Desktop\tf2-extract\tf2\team fortress 2 content.gcf\root\tf\resource', '[[August 23, 2011 Patch]]')