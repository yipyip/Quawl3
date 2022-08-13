# -*- coding: utf-8 -*-

"""
2 Dimensional Character Field Display

Qurawl Logic Map Chars are taken over.
"""

####




####

__all__ = ['QurawlChars']

####

class CharQurawl(object):
    """Console drawing"""

    def __init__(self, engine, conf):

        self.engine_klass = engine
        self.engine = engine(conf.get('width', 1), conf.get('height', 1))


    def update_engine(self, width, height):

        if not (width == self.engine.width and height == self.engine.height):
            self.engine = self.engine_klass(width, height)


    def draw_terrain(self, terrain):

        self.update_engine(terrain.width, terrain.height)
        for ty in range(terrain.height):
            for tx in range(terrain.width):
                self.engine.color(terrain[tx, ty])
                self.engine.point(tx, ty)


    def draw_item(self, item):

        self.engine.color(item.symbol)
        self.engine.point(*item.position)


    def display(self):

        self.engine.display()

####
