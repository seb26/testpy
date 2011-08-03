# -*- coding: utf-8 -*-

import query

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

query.login()

# print query.getTransclusions('Template:Stub', limit='10', qcontinue=False)
# print query.getDuplicates('Medic taunts16 de.wav')
# print query.whatLinksHere('User_talk:seb26', qcontinue=False, limit='10', filterredir='redirects')
# print query.getCategory('Category:Users', limit='10', qcontinue=False)
# print query.whatUsesFile('File:Leaderboard class scout.png', limit='10', qcontinue=False)
# print query.getImagesUsed('Main Page', qcontinue=False)

x = query.getPages(qcontinue=True, lang=True)

for y in x:
    print y