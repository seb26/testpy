import wikitools
import settings
import re

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

# Settings
print 'Logging in.'
wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
print 'Logged in.'

regex = re.compile(r'(.*?)\/zh-hans')

f = open('todelete.txt', 'r')
print 'Opened todelete.txt'

for title in f:
    title = u(title)
    summary = u'wrong name'
    delete = wikitools.page.Page(wiki, title).delete(reason=summary)
    print 'Deleted %s: %s' % (title, summary)