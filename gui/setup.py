#################################################################
# Do not remove the py2exe package, it is needed somewhere else #
#################################################################
import sys

sys.path.append(r'..')
sys.path.append(r'..\libs')
sys.path.append(r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\redist\x64\Microsoft.VC140.CRT')
sys.path.append(r'C:\Windows\WinSxS\amd64_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_750b37ff97f4f68b')
sys.path.append(r'C:\Windows\SysWOW64\downlevel')

import py2exe
import resources.gui_resources
from distutils.core import setup
from glob import glob
import site
import os.path

data_files = [
    (".", glob(r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\redist\x64\Microsoft.VC140.CRT\*.*')),
    (".", glob(r'C:\Windows\SysWOW64\downlevel\api-ms-win-crt-heap-l1-1-0.dll')),
    (".", glob(r'C:\Windows\SysWOW64\downlevel\api-ms-win-crt-runtime-l1-1-0.dll')),
    (".", glob(r'C:\Windows\SysWOW64\downlevel\api-ms-win-crt-stdio-l1-1-0.dll')),
    (".", glob(r'C:\Windows\SysWOW64\downlevel\api-ms-win-crt-string-l1-1-0.dll')),
    ("imageformats", [site.getsitepackages()[1] + "\\PyQt4" + "\\plugins\\imageformats\\qjpeg4.dll"]),
    ("imageformats", [site.getsitepackages()[1] + "\\PyQt4" + "\\plugins\\imageformats\\qico4.dll"]),
    ("imageformats", [site.getsitepackages()[1] + "\\PyQt4" + "\\plugins\\imageformats\\qgif4.dll"])]

excludes = ['Carbon', 'Carbon.Files', 'IronPythonConsole', 'System', 'System.Windows.Forms.Clipboard', '_imp',
            '_scproxy', '_sysconfigdata', '_thread', 'clr', 'com.sun', 'com.sun.jna', 'com.sun.jna.platform',
            'console', 'dummy.Process',
            'importlib.machinery', 'modes.editingmodes', 'ordereddict',
            'pkg_resources.extern.appdirs', 'pkg_resources.extern.packaging', 'pkg_resources.extern.six',
            'pkg_resources.extern.six.moves', 'pyreadline.keysyms.make_KeyPress',
            'pyreadline.keysyms.make_KeyPress_from_keydescr', 'pyreadline.keysyms.make_keyinfo',
            'pyreadline.keysyms.make_keysym', 'six.moves.urllib', 'startup', 'win32com.gen_py',
            'win32com.shell', 'winreg', 'cffi']
includes = ['sip', 'pkg_resources', 'PyQt4', 'sqlalchemy.sql.default_comparator', 'sqlalchemy.ext.baked']
packages = ['appdirs', 'packaging', 'encodings', 'sqlalchemy_utils']
dll_excludes = ['IPHLPAPI.DLL',
                'api-ms-win-crt-convert-l1-1-0.dll',
                'api-ms-win-crt-math-l1-1-0.dll',
                'api-ms-win-crt-math-l1-1-0.dll',
                'api-ms-win-crt-utility-l1-1-0.dll']

# important note: There is a bug in py2exe which requires setup.py to be executed twice to set an app icon
for _ in range(1, 3):
    setup(data_files=data_files,
          name='SQL Alchemy Viewer',
          author='Rida-Shamasneh',
          version="v0.0.1",
          description='SQL Alchemy Viewer, CSV viewer (POC)',
          packages=[os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\\libs'],
          options={'py2exe': {'excludes': excludes,
                              'includes': includes,
                              'packages': packages,
                              'dll_excludes': dll_excludes}},
          zipfile=None,
          windows=[{'script': 'main.py',
                    'dest_base': 'sql_alchemy',
                    'icon_resources': [(1, os.getcwd() + '\\resources\\images\\app_icon.ico')]
                    }]
          )
