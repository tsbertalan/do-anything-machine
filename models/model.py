import random

class Model(list):
    'get_space should return a list of lists, each of which contain all possible selections for that variable'

    _space = None

    def __init__(self):
        super(Model, self).__init__()


    def get_space(self):
        output = []
        for c in self:
            output.append(c)
        return output

    @property
    def space(self):
        '''
        lazy evaluation of the dimensions to produce a space object
        it's worth noting that any model can be evaluated independently
        '''
        if self._space == None:
            self._space = Space()
            for c in self:
                self._space.append(c.get_space())
        return self._space

class DimensionIndexError( Exception ): pass

class Space(list):
    'wrapper for list and housing for space functions'
    _firstrun = False

    def current(self):
        output = []
        for dimension in self:
            output.append(dimension.current())
        return output

    def next(self, index=-1):
        'go back and set off any level of nexts that are needed'
        if self._firstrun == False:
            'gotta start by returning the zero state'
            self._firstrun = True
            return self.current()
        dimension = self[index]
        try:
            dimension.next()
        except DimensionIndexError as e:
            dimension.reset()
            self.next(index=index-1)

        return self.current()

    def randomize(self):
        'return a random set of coordinates within the space'
        output = []
        for dimension in self:
            output.append(dimension.randomize())
        return output

class Dimension(list):
    def __init__(self,name, spread):
        super(Dimension, self).__init__()
        self._name = name
        self.extend(spread)
        self._min = 0
        self._max = len(self)-1
        self.reset()

    def get_space(self):
        return self

    def reset(self):
        self.cursor = 0

    def next(self):
        try:
            self.cursor += 1
            selection = self[self.cursor]
        except IndexError as e:
            raise DimensionIndexError("Reached the limit of this dimension.")

    def current(self):
        return self[self.cursor]

    def randomize(self):
        "return a random coordinate"
        self.cursor = random.randrange(self._min, self._max)
        return self[self.cursor]

class Integer(Dimension):
    pass

class Boolean(Dimension):
    def __init__(self,name):
        super(Boolean, self, name, range(0,2)).__init__()

class List(Dimension):
    'should add to the output space n times the output space of the child'
    def __init__(self,name, max, child):
        super(List, self).__init__(name, range(0,max+1))
        self.child = child

    def get_space(self):
        sp = self.child
        return sp*self.max

class Test(Model):
    def __init__(self):
        super(Test, self).__init__()
        self.extend([
        Integer('row', range(0,10)),
        Integer('row', ["A","B","C","D"]),
        Integer('row', ["@","$","%"])
        ])


class Queen(Model):
    def __init__(self):
        self.extend([
        Integer('row', range(1,9)),
        Integer('row', ["A","B","C","D","E","F","G","H"]),
        Integer('row', range(1,9)),
        Integer('row', ["A","B","C","D","E","F","G","H"]),
        Integer('row', range(1,9)),
        Integer('row', ["A","B","C","D","E","F","G","H"])
        ])

class NineQueens(Model):
    def __init__(self):
        self.extend([
        List('queens', 9, Queen())
        ])

class Note(Model):
    children = [
    Integer('pitch',range(0,128)),
    Integer('duration', range(0,3000)),
    Integer('offset', range(0,3000)),
    Integer('velocity', range(0,150))
    ]


class Song(Model):
    children = [
    List('notes', 1000, Note())
    ]

