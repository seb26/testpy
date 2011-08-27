# Copyright (c) 2011 seb26. All rights reserved.
# Source code is licensed under the terms of the Modified BSD License.

import wikitools
import os
import re
from collections import defaultdict
import testpyconfig as config

template = u'''<!-- This page is updated by a bot. Changes made to it will likely be lost. -->
== Recent changes ==
{{tf diff|p=%s}}
%s
</div>
* [{{fullurl:{{FULLPAGENAMEE}}|action=history}} \'''Previous changelogs\''']
== Licensing ==
{{Externally linked}}
{{ExtractTF2}}
[[Category:Text files]]'''

class Re(object):
      def __init__(self):
        self.last_match = None
      def match(self,pattern,text):
        self.last_match = re.match(pattern,text)
        return self.last_match
      def search(self,pattern,text):
        self.last_match = re.search(pattern,text)
        return self.last_match

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

class diff:

    def __init__(self, difffile, patch, files):
        self.difffile = difffile
        self.patch = u(patch)
        self.files = files

        # Run dem functions.
        self.format()
        self.edit()

    def format(self):
        gre = Re()
        r_add = re.compile(r'^\+[^\+](.+)', re.MULTILINE)
        r_rem = re.compile(r'^\-[^\-](.+)', re.MULTILINE)
        r_head = re.compile(r'^@@(.+)', re.MULTILINE)
        r_con = re.compile(r'^\s[^\}](.+)', re.MULTILINE)
        r_diff = re.compile(r'^diff --git (a\/.*)\s(b\/.*)', re.MULTILINE)

        f = open(self.difffile, 'r')
        output = []
        print 'Parsing %s and formatting...' % self.difffile
        for line in f.readlines():
            if gre.match(r_add, line):
                output.append(u'{{tf diff|+|2=%s}}' % u(gre.match(r_add, line).groups(0)[0]))
            elif gre.match(r_rem, line):
                output.append(u'{{tf diff|-|2=%s}}' % u(gre.match(r_rem, line).groups(0)[0]))
            elif gre.match(r_head, line):
                output.append(u'{{tf diff|@|2=@@%s}}' % u(gre.match(r_head, line).groups(0)[0]))
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
        wiki = wikitools.Wiki(config.apiurl)
        wiki.login(config.username, config.password)
        print 'Logged in.'
        print 'Beginning edit iterator. Today I\'ll be editing:', self.files
        for f in self.files:
            if len(d[f]) == 0:
                # If there is no entry for the file, mark that it is unchanged. defaultdict does not
                # produce ValueErrors in the same way as a normal dict would.
                text = template % (self.patch, u'{{tf diff|c|2=No changes.}}')
                print f, '> formatted wikitext. No changes.'
            else:
                text = template % (self.patch, u'\n'.join(d[f]))
                print f, '> formatted wikitext.'
            print f, '> editing...'
            page = wikitools.Page(wiki, 'File:' + f.capitalize())
            page.edit(text, summary='Updated diff for [[%s]].' % self.patch, bot=1, skipmd5=True)
            print f, '> done.'

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

x = diff('raw.diff', 'August 23, 2011 Patch', filelist)