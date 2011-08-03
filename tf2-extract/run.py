import os
import shutil
import re
from collections import defaultdict

config = {
    'gcf': {
        'team fortress 2 content.gcf': r'C:\Program Files\Steam\steamapps\team fortress 2 content.gcf',
        'team fortress 2 materials.gcf': r'C:\Program Files\Steam\steamapps\team fortress 2 materials.gcf'
        },
    'files': {
        'team fortress 2 content.gcf': [
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
        },
    'extract': r'X:\Sebi\Desktop\tf2-extract\tf2' # X:\Sebi\Desktop\testpy\tf2-extract\03
    }

def mkdirs(gcf, fdir):
    fulldir = os.path.join(config['extract'], gcf, fdir)
    if not os.path.exists(fulldir):
        os.makedirs(fulldir)
        return True
    else:
        return False

def hlextract(p, d, e):
    """
    p - Path to package.
    d - Directory to extract to. Directory must already exist or extraction will fail.
    e - Filepaths to extract.
    """

    try:
        print 'Opening process.'
        process = os.popen(r'hlextract -p "%s" -v -d "%s" %s' % (p, d, e))
        for i in process.readlines():
            print i.strip()
        process.close()
        print 'Done.'
    except:
        print 'extract() failed.'

def tf_extract():
    d = {}
    e = {}
    for z in config['files'].items():
        temp = []
        gcf = z[0]
        d[gcf] = defaultdict(list)
        for fp in z[1]:
            wdir = os.path.split(fp)[0]
            d[gcf][wdir].append(fp)
        e[gcf] = {}
        for t in d[z[0]].items():
            fdir = t[0]
            f = t[1]
            e[gcf][fdir] = '-e "' + '" -e "'.join(f) + '"'
    for k, v in e.items():
        for fdir, f in v.items():
            edir = os.path.join(config['extract'], k, fdir)
            mkdirs(k, fdir)
            hlextract(config['gcf'][k], edir, f)

def tf_recode():
    """Duplicates files, and recode them to utf-8."""
    txt = []
    fdir = os.path.join(config['extract'], 'team fortress 2 content.gcf', r'root\tf\resource')
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

def run():
    tf_extract()
    tf_recode()

print run()