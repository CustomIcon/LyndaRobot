#!c:\users\aman\documents\github\lyndarobot\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PTable==0.9.2','console_scripts','ptable'
__requires__ = 'PTable==0.9.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('PTable==0.9.2', 'console_scripts', 'ptable')()
    )
