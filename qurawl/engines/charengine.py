# -*- coding: utf-8 -*-

"""Console Output for Character Canvas
"""

####



import os
import sys

####

from common.environ import ENV

####

__all__ = ['CharEngine']

####

CODING = ENV['encoding']

####

write = sys.stdout.write

####

class CharEngine(object):
    """Console output"""

    def __init__(self, width, height):
        """Initialize canvas memory."""

        self.width = width
        self.height = height
        self.canvas = [['?'] * self.width for _ in range(self.height)]
        self.act_color = '.'


    def __getitem__(self, xy):

        x, y = xy
        return self.canvas[y][x]


    def __setitem__(self, xy, item):

        x, y = xy
        self.canvas[y][x] = item


    def __iter__(self):
        """get columns"""
        return ("".join(row) for row in self.canvas)


    def __unicode__(self):

        return (os.linesep).join(row for row in self)


    def __str__(self):

       return self.__unicode__()


    def color(self, color):

        self.act_color = color


    def point(self, x, y):

        self[x, y] = self.act_color


    def display(self):

        write(str(self))

####
