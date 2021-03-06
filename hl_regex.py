# -*- coding: utf-8 -*-

__module_name__ = 'hl_regex'
__module_description__ = 'XChat - highlight messages using regular expressions.'
__module_version__ = '0.1'

"""

    hl_regex.py

    Python script for X-Chat Python plugin to notify the user when
    incoming chat matches any defined regular expression.

    The script then logs each highlight in the server tab so that
    the user can view previous highlights with ease. Most useful
    for IRC bouncers that have instant buffer playback where
    highlights can be missed by text flying past fast.


    INSTALLATION:

    To use the script, this file must be placed into the %APPDATA%
    directory (e.g. C:\Users\X\AppData\Roaming\X-Chat 2\) and the
    Python plugin must be installed for X-Chat. This requires
    Python 2.7 to be installed somewhere on the machine.

    NOTE:

    To make changes to the regex while X-Chat is running, edit the
    file and then use the command '/py reload hl_regex.py' to
    reload it.


"""

# CONFIG

# Regular expressions, in list form
# Script will test all of them and highlight on the first one that matches
# After a match, it'll stop searching and just highlight
regexps = [
    r'\b_?s+(?:cab+|e+b+)i?\d*(?:ington|ers*|ito|ville|poot(?:is|er)?|ton|BOT|abstract|demoman|berg|asti[ae]n)*',
    r'\~(?:staff|tf2(?:update|blogupdate|patch|schema))'
]

# Matched when scanning already highlighted messages (i.e. X-Chat highlights nickname by default)
# This should be set to your nickname with the word boundary marker
regexp_already_hl = r'_seb\b'

# The tab to send logged highlights to
server_name = 'freenode'

# Nicknames never to scan messages from
bad_nick = [
    'Spacenet',
    'Spacenet_'
]

# Le script

# For documentation on X-Chat Python library
# See http://labix.org/xchat-python
import xchat
import re

xchat.prnt('hl_regex.py loaded!')

def check_msg(word, word_eol, userdata):
    server_tab = xchat.find_context(channel=server_name)

    if word[0] in bad_nick:
        return xchat.EAT_NONE
    if len(word_eol) > 1:
        for reg in regexps:
            r = re.compile(reg, re.IGNORECASE)
            if r.search(word_eol[1]):
                xchat.command('gui color 3')
                xchat.emit_print( 'Channel Msg Hilight', word[0], word[1])
                server_tab.prnt('02[%s02] 05<%s> %s' % (xchat.get_info('channel'), word[0], word_eol[1]))
                return xchat.EAT_ALL
            else:
                continue
    return xchat.EAT_NONE

def check_hl(word, word_eol, userdata):
    server_tab = xchat.find_context(channel=server_name)
    r2 = re.compile(regexp_already_hl, re.IGNORECASE)
    if len(word_eol) > 1:
        if r2.search(word_eol[1]):
            server_tab.prnt('02[%s02] 05<%s> %s' % (xchat.get_info('channel'), word[0], word_eol[1]))
        else:
            return xchat.EAT_NONE

xchat.hook_print('Channel Msg Hilight', check_hl)
xchat.hook_print('Channel Action Hilight', check_hl)
xchat.hook_print('Channel Message', check_msg)
xchat.hook_print('Channel Action', check_msg)