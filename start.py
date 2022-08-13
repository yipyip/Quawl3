#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Qurawl Entry Point"""

####



import sys

####

import qurawl.control as control

####

def main(argv):

    config = control.CONFIG
    return control.main(config)

####

if __name__ == '__main__':
    sys.exit(main((sys.argv)))
