# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import os
import sys
import wikiUpload
import subprocess
import hashlib
import testpyconfig as config

paint = {
    'all': [
        '3B1F23',
        '256D8D',
        '839FA3',
        '18233D',
        '28394D',
        '384248',
        '483838',
        '654740',
        '803020',
        'A89A8C',
        'B88035',
        'C36C2D',
        '2F4F4F',
        '7C6C57',
        '7D4071',
        '7E7E7E',
        '32CD32',
        '424F3B',
        '694D3A',
        '729E42',
        '5885A2',
        '51384A',
        '141414',
        '808000',
        'A57545',
        'B8383B',
        'C5AF91',
        'CF7336',
        'D8BED8',
        'E6E6E6',
        'E7B53B',
        'E9967A',
        'F0E68C',
        'FF69B4'
        ],
    'new': [
        '3B1F23',
        '256D8D',
        '839FA3',
        '18233D',
        '28394D',
        '384248',
        '483838',
        '654740',
        '803020',
        'A89A8C',
        'B88035',
        'C36C2D'
        ]
    }

uploader = wikiUpload.wikiUploader(config.username, config.password, config.url)

summary_new = u"""
== Specifications ==
  rot: (25.276474 -38.199379 -18.572231)
  lightrot: (64.244095 -179.224884 -16.692621)
  trans: (30.559074 0.000000 2.061374)
  fov: 48
  phongboost: .25
{{subst:pid}}
  """

summary_ovr = u'Retaken. rot:(25.276474 -38.199379 -18.572231)|lightrot:(64.244095 -179.224884 -16.692621)|trans:(30.559074 0.000000 2.061374)|fov:48|phongboost:.25'

log = open('uploadpaint.log', 'a')

def upload(f, name, overwrite=False, reupload=False, summary=None):
    global uploader
    try:
        print 'upload():', f, 'uploading to', name, '...'
        uploader.upload(f, name, summary, overwrite=overwrite, reupload=reupload)
        log.write('Attempted upload of %s | %s\n' % (f, name))
    except:
        print 'upload():', f, 'to', name, 'failed.'
        log.write('error:upload() %s | %s\n' % (f, name))

def run(hat, fprefix, wdir, **kwargs):
    log.write('# Start run: %s\n' % hat)
    for color in paint['all']:
        fname = fprefix + color + '.png'
        wname = 'Painted ' + hat + ' ' + color + '.png'
        if 'style' in kwargs:
            wname = wname[:-4] + ' ' + kwargs['style'] + '.png'
        wname = wname.replace(' ', '_')
        fpath = os.path.join(wdir, fname)

        if os.path.exists(fpath):
            if color in paint['new']:
                print color, wname, fpath
                upload(fpath, wname, overwrite=False, summary=summary_new)
            else:
                print color, wname, fpath
                upload(fpath, wname, overwrite=True, reupload=True, summary=summary_ovr)
        else:
            log.write('error:run()[noexist] %s | %s\n' % (fpath))


print run("Vintage Tyrolean", 'tyrolean_', r'X:\Sebi\Desktop\PAINT_newp3\medic\tyrolean')