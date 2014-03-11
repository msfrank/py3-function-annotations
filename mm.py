#!/usr/bin/env python3
#
# Example code for implementing multimethods using parameter
# type hints from function annotations.  This code was cribbed
# from the following stackoverflow discussion, which itself
# was modified (i think) from Guido's blog post.
#
# My one modification is to use the inspect module to build
# the correct types-tuple.
#
# http://stackoverflow.com/a/7811344/2308548
# http://www.artima.com/weblogs/viewpost.jsp?thread=101605

import inspect

registry = {}

class MultiMethod(object):
    def __init__(self):
        self.typemap = {}
    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args)
        function = self.typemap.get(types)
        if function is None:
            raise TypeError("no match")
        return function(*args)
    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function

def multimethod(function):
    name = function.__name__
    annotations = function.__annotations__
    mm = registry.get(name)
    if mm is None:
        mm = registry[name] = MultiMethod()
    signature = inspect.signature(function)
    types = tuple(annotations[param] for param in list(signature.parameters))
    mm.register(types, function)
    return mm


@multimethod
def foo(a: int):
    return "just a lonely int"

@multimethod
def foo(a: int, b: str):
    return "an int and a string, what a perfect pair"

@multimethod
def foo(a: str, b: int):
    return "a string and an int, what a devilish combination"

if __name__ == '__main__':
    print("foo(7) = {}".format(foo(7)))
    print("foo(1,'a') = {}".format(foo(1,'a')))
    print("foo('b',3) = {}".format(foo('b',3)))
    print("foo(3.14) = {}".format(foo(3.14)))
