#!/usr/bin/env python3
from __future__ import print_function
import random

r = random.Random()
counter = 0

def next_name(prefix='v'):
    global counter
    counter += 1
    return '%s%d' % (prefix, counter)

class Type:
    def __init__(self, name, generic_params=0):
        self.name = name
        self.generic_params = generic_params

class Context:
    def __init__(self):
        self.types = [Type('int'), Type('string'), Type('uint64'), Type('seq', 1)]
        self.typeclasses = [Type('any')]

    def make_type(self):
        name = next_name('t')
        generic_params = max(random.randrange(0, 4) - 1, 0)
        generic_defs = ['G%d' % i for i in range(generic_params)]
        generic_s = '[%s]' % ', '.join(generic_defs) if generic_defs else ''
        s = 'type %s%s = object\n' % (name, generic_s)

        field_count = random.randrange(10)
        for i in range(field_count):
            if random.randrange(5 + generic_params) > 4:
                field_type = random.choice(generic_defs)
            else:
                field_type = self.gen_type()
            s += '  f%d: %s\n' % (i, field_type)

        typ = Type(name, generic_params)
        self.types.append(typ)
        self.typeclasses.append(typ)

        return s

    def make_typeclass(self):
        name = next_name('tp')
        generic_params = max(random.randrange(0, 4) - 1, 0)
        generic_defs = ['G%d' % i for i in range(generic_params)]
        generic_s = '[%s]' % ', '.join(generic_defs) if generic_defs else ''

        s = 'type %s%s = ' % (name, generic_s)
        s += self.gen_typeclass(generic_defs)

        self.typeclasses.append(Type(name, generic_params))

        return s

    def gen_typeclass(self, additional, can_alt=True):
        i = random.randrange(5)

        if i == 0 or (i == 1 and not additional):
            return self.gen_type()
        elif i == 1:
            return random.choice(additional)
        elif i == 2:
            return random.choice(self.typeclasses).name
        elif i == 3:
            if not can_alt: return random.choice(self.types).name
            options = [ self.gen_typeclass(additional, False) for i in range(random.randrange(2, 5)) ]
            return '(%s)' % ('|'.join(options))
        elif i == 4:
            tp = random.choice(self.typeclasses)
            s = tp.name
            if tp.generic_params:
                params = [ random.choice(additional + ['uint64']) for i in range(tp.generic_params) ]
                s += '[%s]' % ', '.join(params)
            return s

    def gen_type(self, max_type=10000000):
        ti = random.randrange(0, min(len(self.types), max_type))
        t = self.types[ti]
        type_string = t.name
        if t.generic_params:
            type_string += '[%s]' % ', '.join(self.gen_type(ti - 1) for _ in range(t.generic_params))
        return type_string

c = Context()
for i in range(4):
    print(c.make_type())

for i in range(10):
    print(c.make_typeclass())
