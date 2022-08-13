#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Qurawl Game
"""

####



import sys
import os
from collections import defaultdict as defdict
import itertools as it

####

import common.graphs as graphs

####

__all__ = ['LevelMap', 'Level', 'Item', 'Actor', 'Qurawl']

####

OBSTACLES = ('#',)
FREE_PLACES = ('.',)
ACTOR_PRIORITY = 2
MONSTER_PRIORITY = 1

####

class LevelMap(object):


    def __init__(self, level):

        self.level_map = list(map(list, level.split()))
        self.width = len(self.level_map[0])
        self.height = len(self.level_map)


    def __getitem__(self, xy):
        x, y = xy
        return self.level_map[y][x]

####

class Level(object):


    def __init__(self, level_map, actors, monsters, items,
                 obstacles=OBSTACLES, free_places=FREE_PLACES):

        self.level_map = level_map
        self.actors = actors
        self.monsters = monsters
        self.items = items
        acmo = actors + monsters
        self.coord_actors = dict(list(zip([actor.position for actor in acmo], acmo)))
        self.obstacles = obstacles
        self.free_places = free_places
        self.future_moves = defdict(list)
        self.pos_move = dict()


    @property
    def width(self):

        return self.level_map.width


    @property
    def height(self):

        return self.level_map.height


    def is_valid_move(self, x, y):

        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        if self.level_map[x, y] in self.obstacles:
            return False
        #if (x, y) in self.coord_actors.keys():
        #    return False

        return True


    def move(self, actor, direct):

        start = actor.position
        goal = actor.look(direct)
        if self.is_valid_move(*goal):
            self.future_moves[goal].append(actor)
            self.pos_move[actor.position] = goal
            return True
        return False


    def set_actors(self, moves):
        """Selectively update  actor, monster positions"""
        is_new = set()
        for new_position, actor in list(moves.items()):
            if actor.position not in is_new:
                self.coord_actors.pop(actor.position)
            actor.position = new_position
            is_new.add(new_position)
            self.coord_actors[new_position] = actor

        self.future_moves = defdict(list)
        self.pos_move = {}


    def _pr_future_moves(self, future_moves):

        for pos, act in list(future_moves.items()):
            print(pos, act)
            for a in act:
                print(a.name, a.symbol, end=' ')
            print()


    def resolve_moves(self):

        move_multipos = defdict(list)
        for move, actors in list(self.future_moves.items()):
            for actor in actors:
                move_multipos[move].append(actor.position)

        static = set(self.coord_actors) - set(self.pos_move)
        static |= self.propagate_static(move_multipos, static)

        doable = {}
        for move in move_multipos:
            if move not in static and self.level_map[move] in self.free_places:
                doable[move] = move_multipos[move]

        movings = {}
        for move, positions in list(doable.items()):
            if move not in self.pos_move and move not in static:
                sortpos = sorted(positions, key=lambda p: self.coord_actors[p].priority)
                movings[move] = sortpos[0]
                static.update(sortpos[1:])

        static |= self.propagate_static(doable, static)

        beset = {}
        for move in set(doable) - set(movings):
            beset[move] = doable[move]

        for move, positions in list(beset.items()):
            if move not in static:
                for pos in positions:
                    if move == self.pos_move[pos] and pos == self.pos_move[move]:
                        static.add(move)
                        static.add(pos)
                        break
                valid_pos = [p for p in positions if p not in static]
                if not valid_pos:
                    continue
                sortpos = sorted(valid_pos, key=lambda p: self.coord_actors[p].priority)
                movings[move] = sortpos[0]
                static.update(sortpos[1:])

        static |= self.propagate_static(doable, static)

        real_moves = {}
        for move, pos in list(movings.items()):
            if move not in static:
                real_moves[move] = self.coord_actors[pos]

        return real_moves


    def propagate_static(self, moves, static):

        visited = set()
        for move in moves:
            if move in static and move not in visited:
                visited |= graphs.dfs_connected(moves, move)

        return visited


    def action(self):

        for monster in self.monsters:
            self.move(monster, monster.move_action())

        real_moves = self.resolve_moves()
        self.set_actors(real_moves)


    def render(self, renderer):

        renderer.draw_terrain(self.level_map)
        list(map(renderer.draw_item, list(self.coord_actors.values())))


####

class Item(object):

    def __init__(self, name, symbol, x, y):

        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y


    @property
    def position(self):

        return self.x, self.y


    @position.setter
    def position(self, xy):

        self.x, self.y = xy


    def __repr__(self):

        return "{0} {1} {2} {3}".format(self.name, self.symbol, self.x, self.y)

####

class Actor(Item):


    moves = {'up': (0, -1), 'left': (-1, 0), 'down': (0, 1), 'right': (1, 0)}


    def __init__(self, name, symbol, x, y, priority=ACTOR_PRIORITY):

        super(Actor, self).__init__(name, symbol, x, y)
        self.priority = priority


    def look(self, direct):

        dx, dy = Actor.moves[direct]
        return self.x + dx, self.y + dy


    def __repr__(self):

        return "{0} {1} {2} {3} {4}".format(self.name, self.symbol, self.x, self.y,
                                            self.priority)

####

class Monster(Actor):

    def __init__(self, name, symbol, x, y, moves, priority=MONSTER_PRIORITY):

        super(Monster, self).__init__(name, symbol, x, y)
        self.priority = priority
        self.move_cycle = it.cycle(moves)


    def move_action(self, step=1):

        for _ in range(step):
            direct = next(self.move_cycle) 
        return direct

####

raw_level =\
"""\
#############
#...........#
#...........#
#...........#
#...........#
#...........#
#...........#
#...........#
#############"""



class Qurawl(object):

    messages = {'no_name': "Who's that?",
                'no_direction': 'Ups, What direction?'}


    def __init__(self, conf):

        self.conf = conf
        #self.reset()


    def start(self):

        actor1 = Actor('x', 'X', 1, 1)
        actor2 = Actor('o', 'O', 1, 2)
        actor3 = Actor('y', 'Y', 1, 4)

        quad = 'left', 'down', 'right', 'up'
        rl3 = 'right', 'right', 'right','left', 'left', 'left'

        m1 = Monster('fly', 'f', 4, 2, quad)
        m2 = Monster('fly', 'g', 3, 2, quad)
        m3 = Monster('fly', 'h', 3, 3, quad)
        m4 = Monster('fly', 'i', 4, 3, quad)

        m2.move_action(1)
        m3.move_action(2)
        m4.move_action(3)

        lr2 = 'right', 'right', 'left', 'left'
        rl2 = lr2[::-1]
        m11 = Monster('fly', 'a', 2, 6, lr2)
        m12 = Monster('fly', 'b', 3, 6, lr2)
        m21 = Monster('fly', 'b', 7, 6, rl2)
        m22 = Monster('fly', 'a', 8, 6, rl2)



        actors = actor2,  actor3,
        monsters = m1, m2, m3, m4, m11, m12, m21, m22
        level_map = LevelMap(raw_level)
        self.level = Level(level_map, actors, monsters, [], obstacles=('#',))
        self.name_actors = dict(list(zip((actor.name for actor in actors), actors)))


    def input_action(self, *args, **kwargs):

        name, direct = args
        if name not in self.name_actors:
            return self.messages['no_name']
        actor = self.name_actors[name]
        if direct not in actor.moves:
            return self.messages['no_direction']

        self.level.move(actor, direct)
        return ''


    def item_action(self, item):

        return item


    def action(self):

        self.level.action()

####
