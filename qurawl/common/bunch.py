"""
Bunch Object for object.attribute Notation
"""

####



import os

####

class Bunch(dict):
    """Object for storing Key-Value Pairs"""

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)

    def __repr__(self):
        return ','.join("%s:%s" % (key, value) for key, value in sorted(self.items()))

    def __str__(self):
        return os.linesep.join("%s" % keyval for keyval in repr(self).split(','))

