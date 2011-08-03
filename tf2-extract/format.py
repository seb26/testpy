import re
import sys

# Not mine. StackOverflow :< I could never write this.
class Re(object):
  def __init__(self):
    self.last_match = None
  def match(self,pattern,text):
    self.last_match = re.match(pattern,text)
    return self.last_match
  def search(self,pattern,text):
    self.last_match = re.search(pattern,text)
    return self.last_match

def readDiff(f):

    diff = open(f, 'rb').read(-1).decode('utf8')

    gre = Re()

    dlist = diff.splitlines()

    r_add = re.compile(r'^\+(.+)', re.MULTILINE)
    r_rem = re.compile(r'^\-(.+)', re.MULTILINE)
    r_head = re.compile(r'^@@(.+)', re.MULTILINE)
    r_con = re.compile(r'^\s(.+)', re.MULTILINE)

    output = []

    for line in dlist:
        if gre.match(r_add, line):
            output.append('{{tf diff|+|2=%s}}' % gre.match(r_add, line).groups(0))
        elif gre.match(r_rem, line):
            output.append('{{tf diff|-|2=%s}}' % gre.match(r_rem, line).groups(0))
        elif gre.match(r_head, line):
            output.append('{{tf diff|@|2=%s}}' % gre.match(r_head, line).groups(0))
        elif gre.match(r_con, line):
            output.append('{{tf diff|c|2=%s}}' % gre.match(r_con, line).groups(0))
        else:
            output.append(line)

    for x in output:
        if x:
            print x

print readDiff('raw.diff')