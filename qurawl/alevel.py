"""How to manage an ascii level map
   Tested with Python 2.6, 3.2
"""




raw_level =\
"""\
######
#....#
#....#
######\
"""

class Level(object):

    def __init__(self, level):
        self.level_map = list(map(list, level.split()))


    def __getitem__(self, xy):
        x, y = xy
        return self.level_map[y][x]


    def __setitem__(self, xy, item):
        x, y = xy
        self.level_map[y][x] = item


    def __iter__(self):
        return ("".join(row) for row in self.level_map)


    def __str__(self):
        return "\n".join(row for row in self)


def main():

    print('___')
    print(raw_level)
    print( '~~~')

    alevel = Level(raw_level)
    print("alevel")
    print(alevel)
    print()
    print("alevel rows and setitem")
    alevel[1,2] = "?"
    for row in alevel:
        print(row)

if __name__ == '__main__':
    main()


