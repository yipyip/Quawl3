"""
Useful and Necessary System Informations
"""

####



import sys

####

import qurawl.common.bunch as bunch

####

__all__ = ['ENV']

####

def _environment():
    data = {}
    data['os'] = sys.platform
    data['pyversion'] = '{0:x}'.format(sys.hexversion)
    data['encoding'] = sys.stdout.encoding or sys.getfilesystemencoding()
    return data

####

ENV = bunch.Bunch(**_environment())

####
