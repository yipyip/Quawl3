#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        acmons = actors + monsters
        self.coord_actors = dict(list(zip([actor.position for actor in acmons], acmons)))
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
        doable = dict((xy, move_multipos[xy]) for xy in move_multipos\
                      if xy not in static and\
                        self.level_map[xy] in self.free_places)

        free_static, free_moves = self.free_moving(doable)
        static_sf = self.propagate_static(move_multipos, static | free_static)

        coll_set = set(doable.keys()) - static_sf
        coll_move_pos = dict((xy, move_multipos[xy]) for xy in coll_set)
        coll_static, coll_moves = self.collision_moving(coll_move_pos)
        static_sfc = self.propagate_static(coll_move_pos, static_sf | coll_static)

        print('multipos', move_multipos)
        print('free', free_static, free_moves, static_sf)
        print('coll', coll_static, coll_moves, static_sfc)
        print('s', static)

        movings = free_moves.copy()
        movings.update(coll_moves)
        static = static_sfc
        return dict((move, self.coord_actors[pos]) for move, pos in list(movings.items())
                    if move not in static)


    def propagate_static(self, moves, static):

        visited = set()
        for mov in moves:
            if mov in static:
                if mov not in visited:
                    visited |= graphs.dfs_connected(moves, mov)
                    print('v', visited)

        return visited


    def free_moving(self, moves):

        static = []
        movings = {}
        for move, positions in list(moves.items()):
            if move not in self.pos_move:
                pos = sorted(positions, key=lambda p: self.coord_actors[p].priority)
                movings[move] = pos[0]
                static.extend(pos[1:])

        return set(static), movings



    def collision_moving(self, moves):

        static = []
        movings = {}
        for move, positions in list(moves.items()):
            if move in self.pos_move:
                for pos in positions:
                    if move == self.pos_move[pos]:
                        static.append(move)
                        static.append(pos)
                        break
            else:    
                sortpos = sorted(positions, key=lambda p: self.coord_actors[p].priority)
                movings[move] = pos[0]
                static.extend(pos[1:])

        return set(static), movings


    def action(self):

        for monster in self.monsters:
            self.move(monster, monster.move_action())
        self.set_actors(self.resolve_moves())


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


    def move_rel(self, direct):

        dx, dy = Actor.moves[direct]
        self.position = self.x + dx, self.y + dy


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


    def move_action(self):

        return next(self.move_cycle)


####

raw_level =\
"""\
###########
#.........#
#.........#
#.........#
#.........#
#.........#
###########"""



class Qurawl(object):

    messages = {'no_name': "Who's that?",
                'no_direction': 'Ups, What direction?'}


    def __init__(self, conf):

        self.conf = conf
        #self.reset()


    def start(self):

        actor1 = Actor('x', 'X', 1, 1)
        actor2 = Actor('o', 'O', 1, 2)
        actor3 = Actor('y', 'Y', 1, 3)

        quad = 'left', 'down', 'right', 'up'
        rl3 = 'right', 'right', 'right','left', 'left', 'left'

        m1 = Monster('fly', 'F', 4, 3, quad)
        m2 = Monster('fly', 'G', 2, 5, rl3)
        m3 = Monster('fly', 'H', 1, 5, rl3)
        actors = actor2,  actor3,
        monsters = m2, m3

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
