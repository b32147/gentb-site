# pylint: disable=wildcard-import
"""
Find and initialize the settings/local.py - this file documents all the
settings and keys which should /NEVER/ be committed to a repository and it
seperates out the sys-admin responsibility from the programmer's.
"""

from shutil import copyfile

import logging
import sys
import os

BASE_DIR = os.path.dirname(__file__)
SETTINGS = 'local.py'

from .base import *

try:
    from .local import *
except ImportError:
    TARGET = os.path.join(BASE_DIR, SETTINGS)
    if not os.path.exists(TARGET):
        for template in (TARGET + '.template', TARGET[:-3] + '.template'):
            if os.path.exists(template):
                copyfile(template, TARGET)
                break
    try:
        from .local import *
    except ImportError:
        logging.error("No settings found and default template failed to load.")
        exit(3)

for n, v in globals().items():
    if n.split('_')[-1] in ('DIR', 'DIRECTORY', 'PATH', 'ROOT'):
        if v and v[0] != '/':
            raise IOError("Setting %s should be an absolute path." % n)
        if not isdir(v):
            try:
                sys.stderr.write("INFO: Making directory: %s for %s" % (v, n))
                os.makedirs(v)
            except:
                raise IOError("Failed to make directory: %s" % v)
