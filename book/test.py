# -*- coding: utf-8 -*-
__author__ = 'andrew'


class Test:
    def __init__(self, param):
        self.a = param

if __name__ == "__main__":
    t = [1, 2, 3, 4, 5]
    test = Test(t)
    print "t:"
    print t
    print "test"
    print test.a
    print "---"
    test.a.append(6)
    print "t:"
    print t
    print "test"
    print test.a