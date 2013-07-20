#!/usr/bin/python2

# Author: Joseph Wiseman <joswiseman@gmail>
# URL: https://github.com/dryes/nzbsubs/

import os,re,sys
from datetime import date
from pynzb import nzb_parser

def main(nzbfile):
    try:
        nzb = open(nzbfile, 'r').read()
    except:
        print('Error reading nzb.')
        return False

    try:
        nzbparse = nzb_parser.parse(nzb)
    except:
        print('Error parsing nzb.')
        return False

    nzbsubs = [] 
    for f in nzbparse:
        if re.search(r'[._-](vob)?sub(title)?s?[._-]?.*\.(r(ar|\d+)|sfv|srt|idx|sub|par2)\"', f.subject, re.IGNORECASE) is not None:
            nzbsubs.append(f)

    if len(nzbsubs) == 0:
        print('No subs found in nzb.')
        return False

    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    content += '<!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.1//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.1.dtd">\n'
    content += '<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">\n'
    for f in nzbsubs:
        unixdate = str(((f.date.toordinal() - date(1970, 1, 1).toordinal()) * 24*60*60))
        content += '<file poster="' + f.poster + '" date="' + unixdate + '" subject="' + f.subject.replace('"', '&quot;') + '">\n'

        content += '<groups>\n'
        for g in f.groups:
            content += '<group>' + g + '</group>\n'
        content += '</groups>\n'

        content += '<segments>\n'
        for s in f.segments:
            content += '<segment bytes="' + str(s.bytes) + '" number="' + str(s.number) + '">' + s.message_id + '</segment>\n'
        content += '</segments>\n'

        content += '</file>\n'

    content += '</nzb>'

    try:
        os.unlink(nzbfile)
    except:
        print('Error deleting input nzb.')
        return False

    with open(nzbfile, 'w') as f:
        try:
            f.write(content)
        except:
            print('Error writing nzb.')
            return False

    print('%r successfully processed.' % nzbfile)

if __name__ == '__main__':
    err = 0
    for f in sys.argv[1:]:
        if os.path.isfile(f) and main(sys.argv[1]) == False:
            err = (err+1)
    if err > 0:
        sys.exit(1)
