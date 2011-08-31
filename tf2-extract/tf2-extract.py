# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import sys
import os
import re
import shutil
import wikitools
import hlextract
import wikiUpload
from collections import defaultdict

import wconfig
wconfig = wconfig.config['tfwiki']


def u(s):
    if type(s) is type(u''):
        return s
    if type(s) is type(''):
        try:
            return unicode(s)
        except:
            try:
                return unicode(s.decode('utf8'))
            except:
                try:
                    return unicode(s.decode('windows-1252'))
                except:
                    return unicode(s, errors='ignore')
    try:
        return unicode(s)
    except:
        try:
            return u(str(s))
        except:
            return s


class Re(object):
      def __init__(self):
        self.last_match = None
      def match(self,pattern,text):
        self.last_match = re.match(pattern,text)
        return self.last_match
      def search(self,pattern,text):
        self.last_match = re.search(pattern,text)
        return self.last_match


class tf2extract:

    def __init__(self):
        self.config = {}
        self.config['set'] = True

        # Edit below.
        self.config['package'] = 'team fortress 2 content.gcf'
        self.config['packagedir'] = r'C:\Program Files\Steam\steamapps\team fortress 2 content.gcf'
        self.config['outdir'] = r'X:\Sebi\Desktop\tf2-extract\tf2'

        self.config['extractlist'] = [
            r'root\tf\resource\closecaption_danish.dat',
            r'root\tf\resource\closecaption_danish.txt',
            r'root\tf\resource\closecaption_dutch.dat',
            r'root\tf\resource\closecaption_dutch.txt',
            r'root\tf\resource\closecaption_english.dat',
            r'root\tf\resource\closecaption_english.txt',
            r'root\tf\resource\closecaption_finnish.dat',
            r'root\tf\resource\closecaption_finnish.txt',
            r'root\tf\resource\closecaption_french.dat',
            r'root\tf\resource\closecaption_french.txt',
            r'root\tf\resource\closecaption_german.dat',
            r'root\tf\resource\closecaption_german.txt',
            # r'root\tf\resource\closecaption_hungarian.dat', Doesn't exist? WTB Hungarians.
            r'root\tf\resource\closecaption_hungarian.txt',
            r'root\tf\resource\closecaption_italian.dat',
            r'root\tf\resource\closecaption_italian.txt',
            r'root\tf\resource\closecaption_japanese.dat',
            r'root\tf\resource\closecaption_japanese.txt',
            r'root\tf\resource\closecaption_korean.dat',
            r'root\tf\resource\closecaption_korean.txt',
            r'root\tf\resource\closecaption_koreana.dat',
            r'root\tf\resource\closecaption_koreana.txt',
            r'root\tf\resource\closecaption_norwegian.dat',
            r'root\tf\resource\closecaption_norwegian.txt',
            r'root\tf\resource\closecaption_polish.dat',
            r'root\tf\resource\closecaption_polish.txt',
            r'root\tf\resource\closecaption_portuguese.dat',
            r'root\tf\resource\closecaption_portuguese.txt',
            r'root\tf\resource\closecaption_romanian.dat',
            r'root\tf\resource\closecaption_romanian.txt',
            r'root\tf\resource\closecaption_russian.dat',
            r'root\tf\resource\closecaption_russian.txt',
            r'root\tf\resource\closecaption_schinese.dat',
            r'root\tf\resource\closecaption_schinese.txt',
            r'root\tf\resource\closecaption_spanish.dat',
            r'root\tf\resource\closecaption_spanish.txt',
            r'root\tf\resource\closecaption_swedish.dat',
            r'root\tf\resource\closecaption_swedish.txt',
            r'root\tf\resource\closecaption_tchinese.dat',
            r'root\tf\resource\closecaption_tchinese.txt',
            r'root\tf\resource\closecaption_turkish.dat',
            r'root\tf\resource\closecaption_turkish.txt',
            r'root\tf\resource\tf_danish.txt',
            r'root\tf\resource\tf_dutch.txt',
            r'root\tf\resource\tf_english.txt',
            r'root\tf\resource\tf_finnish.txt',
            r'root\tf\resource\tf_french.txt',
            r'root\tf\resource\tf_german.txt',
            r'root\tf\resource\tf_hungarian.txt',
            r'root\tf\resource\tf_italian.txt',
            r'root\tf\resource\tf_japanese.txt',
            r'root\tf\resource\tf_korean.txt',
            r'root\tf\resource\tf_koreana.txt',
            r'root\tf\resource\tf_norwegian.txt',
            r'root\tf\resource\tf_polish.txt',
            r'root\tf\resource\tf_portuguese.txt',
            r'root\tf\resource\tf_romanian.txt',
            r'root\tf\resource\tf_russian.txt',
            r'root\tf\resource\tf_schinese.txt',
            r'root\tf\resource\tf_spanish.txt',
            r'root\tf\resource\tf_swedish.txt',
            r'root\tf\resource\tf_tchinese.txt',
            r'root\tf\resource\tf_turkish.txt',
            r'root\tf\steam.inf'
            ]

        self.config['uploadlist'] = [
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
        self.config['uploadpath'] = r'X:\Sebi\Desktop\tf2-extract\tf2\team fortress 2 content.gcf\root\tf\resource'

        self.config['difflist'] = self.config['uploadlist']
        self.config['diffile'] = r'X:\Sebi\Desktop\testpy\tf2-extract\raw.diff'
        # self.config['patch'] =

        self.template = u'''<!-- This page is updated by a bot. Changes made to it will likely be lost the next time it edits. -->
== Recent changes ==
{{tf diff|p=%s}}
%s
</div>
* [{{fullurl:{{FULLPAGENAMEE}}|action=history}} \'''Previous changelogs\''']
== Licensing ==
{{Externally linked}}
{{ExtractTF2}}
[[Category:Text files]]'''


    def extract(self):
        HL = hlextract.HLExtract(volatile=True)
        print 'Extracting...'
        HL.extract(self.config['packagedir'], self.config['outdir'], self.config['extractlist'], multidir=True)


    def recode(self):
        """Duplicates files, and recode them to utf-8."""
        txt = []
        fdir = os.path.join(self.config['outdir'], self.config['package'], r'root\tf\resource')
        for line in os.listdir(fdir):
            if re.search(r'\.txt', line):
                txt.append(line)
        for f in txt:
            utf = os.path.join(fdir, 'UTF-8')
            if not os.path.exists(utf):
                os.mkdir(utf)
            src = os.path.join(fdir, f)
            dst = os.path.join(fdir, 'UTF-8', f)
            if os.path.isfile(dst):
                os.remove(dst)
            shutil.copy2(src, dst)
            print f, 'Reading...'
            utf_f = open(dst, 'rb').read(-1).decode('utf16').encode('utf8')
            print f, 'Writing...'
            utf_fn = open(dst, 'wb').write(utf_f)


    def __upload__(self, f, name, summary):
        uploader = wikiUpload.wikiUploader(wconfig['usr'], wconfig['pwd'], wconfig['url'])
        try:
            print 'upload():', f, 'uploading to', name, '...'
            uploader.upload(f, name, summary, overwrite=True, reupload=True)
            print 'Attempted upload of %s | %s\n' % (f, name)
        except:
            print 'upload():', f, 'to', name, 'failed.'
            print 'error:upload() %s | %s\n' % (f, name)


    def upload(self):
        # f.upload(self.config['uploadlist'], self.config['uploadpath'], 'Updated patch for [[%s]]' % self.config['patch'])
        for f in self.config['uploadlist']:
            filepath = os.path.join(self.config['uploadpath'], f)
            print filepath, 'to:', f.capitalize(), 'summ:', 'HI!'
            self.__upload__(filepath, f.capitalize(), '[[%s]]' % self.config['patch'])
            print 'Uploaded:', filepath


    def format(self):
        gre = Re()
        r_add = re.compile(r'^\+[^\+](.+)', re.MULTILINE)
        r_rem = re.compile(r'^\-[^\-](.+)', re.MULTILINE)
        r_head = re.compile(r'^@@(.+)', re.MULTILINE)
        r_con = re.compile(r'^\s[^\}](.+)', re.MULTILINE)
        r_diff = re.compile(r'^diff --git (a\/.*)\s(b\/.*)', re.MULTILINE)

        f = open(self.config['diffile'], 'r')
        output = []
        print 'Parsing %s and formatting...' % self.config['diffile']
        for line in f.readlines():
            if gre.match(r_add, line):
                output.append(u'{{tf diff|+|2=%s}}' % u(gre.match(r_add, line).groups(0)[0]))
            elif gre.match(r_rem, line):
                output.append(u'{{tf diff|-|2=%s}}' % u(gre.match(r_rem, line).groups(0)[0]))
            elif gre.match(r_head, line):
                output.append(u'{{tf diff|@|2=%s}}' % u(gre.match(r_head, line).groups(0)[0]))
            elif gre.match(r_con, line):
                output.append(u'{{tf diff|c|2=%s}}' % u(gre.match(r_con, line).groups(0)[0]))
            elif gre.match(r_diff, line):
                p = gre.match(r_diff, line).groups(1)[0]
                output.append('#' + os.path.split(p)[-1])
            elif line.startswith('index'):
                pass
            elif line.startswith('+++') or line.startswith('---'):
                pass
            elif line.startswith(' }'):
                pass
            elif line.startswith('Binary files'):
                pass
            else:
                output.append(line)

        self.formatted = [ x.strip() for x in output if x ] # Blank line and whitespace stripping.
        print 'Done.'


    def edit(self):
        output = []
        d = defaultdict(list)
        print 'Some rearranging...'
        for item in self.formatted:
            if item.startswith('#'):
                hook = item[1:]
            else:
                d[hook].append(item)
        print 'Logging in.'
        wiki = wikitools.Wiki(wconfig['url-api'])
        wiki.login(wconfig['usr'], wconfig['pwd'])
        print 'Logged in.'
        print 'Beginning edit iterator. Today I\'ll be editing:', self.config['difflist']
        for f in self.config['difflist']:
            if len(d[f]) == 0:
                # If there is no entry for the file, mark that it is unchanged. defaultdict does not
                # produce ValueErrors in the same way as a normal dict would.
                text = self.template % (self.config['patch'], u'{{tf diff|c|2=No changes.}}')
                print f, '> formatted wikitext. No changes.'
            else:
                text = self.template % (self.config['patch'], u'\n'.join(d[f]))
                print f, '> formatted wikitext.'
            print f, '> editing...'
            page = wikitools.Page(wiki, 'File:' + f.capitalize())
            page.edit(text, summary='Updated diff for [[%s]].' % self.config['patch'], bot=1, skipmd5=True)
            print f, '> done.'


    def run(self, patch, extract=False, upload=False, diffs=False):
        self.config['patch'] = patch
        if extract is True:
            self.extract()
            self.recode()
        if upload is True:
            self.upload()
        if diffs is True:
            self.format()
            self.edit()
        if extract is False and upload is False and diffs is False:
            # Oh god ^
            print 'I do nothing?'
            return self.config


tf = tf2extract()
tf.run('August 30, 2011 Patch', extract=False, upload=False, diffs=True)