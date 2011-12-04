import os
import shutil
import subprocess
import hashlib

def zz(op, cmd):
    p = subprocess.Popen([ '7z', op ] + cmd, stdout=subprocess.PIPE)
    out = p.communicate()
    print(out[0])
    return out

def tardir(src, out):

    # Part 1: Archivin'
    dirs = []
    stray = []
    for i in os.listdir(src):
        item = os.path.join(src, i)
        if os.path.isdir(item):
            dirs.append(item)
        else:
            stray.append(item)
    for d in dirs:
        dname = os.path.split(d)[-1]
        outtar = os.path.join(out, '{0}.tar'.format(dname))
        wdir = os.path.join(src, '{0}\\'.format(dname))
        zz('a', [ '-ttar', outtar, wdir ])
    zz('a', [ '-ttar', os.path.join(out, '.contents.tar') ] + stray )

    # Part 2: Hashes & Logs
    hashes = os.path.join(out, '.sha256')
    logs = os.path.join(out, '.log')
    if not os.path.exists(hashes):
        os.mkdir(hashes)
    if not os.path.exists(logs):
        os.mkdir(logs)

    for f in os.listdir(out):
        print(f)
        sha256 = hashlib.new('sha256')
        if f.endswith('.tar'):
            print('It does', f)
            tarf = open(os.path.join(out, f), 'rb')

            # Hashing
            while True:
                data = tarf.read(500000)
                if not data:
                    break
                sha256.update(data)
            h = sha256.hexdigest()
            h_path = os.path.join(hashes, '{0}.sha256'.format(os.path.split(f)[-1]))
            hf = open(h_path, 'w')
            hf.write(h)

            # Logging
            log = zz('l', [ os.path.join(out, f) ])
            log_path = os.path.join(logs, '{0}.log'.format(os.path.split(f)[-1]))
            logf = open(log_path, 'wb')
            logf.write(log[0].strip())

tardir(
    r'X:\Sebi\Desktop\_ARCHIVE\archive_2011-10-05',
    r'X:\Sebi\Desktop\_ARCHIVE\archive_2011_out\archive_2011-10-05'
)