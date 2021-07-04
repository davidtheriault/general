#!/usr/bin/python
"""
Written by David Theriault
Problem from fivethirtyeight.com

Given an infinite row of houses on a street,
a person will only move into a house if they have no
adjacent neighbor.

A possible pattern (E empty, O occupied) E O E O
another pattern  E E O E E O

Given an infinite street where people try to fill
in all the houses following the above rules,
what will be the ratio of occupied to unoccuied
houses?
"""


import random
import sys

class Neighborhood:
    def __init__(self, houses=100):
        self.street = [0] * houses
        self.occupy = 0
        self.houses = houses

    def main(self):
        street_order = range(self.houses)
        random.shuffle(street_order)
        for house in street_order:
            if(not self.no_neighbors(house)):
                
                self.occupy += 1
                self.street[house] = 1
        self.print_all()

        
    def no_neighbors(self, house):
        if(house < 0 or house > self.houses):
            raise NameError("house %d out of bounds with houses %d" % (house, self.houses))

        # first house
        if ( house == 0 ):
            return self.street[1] 
        # last house
        if ( house == self.houses - 1):
            return self.street[house - 1]
        return self.street[house - 1] or self.street[house] or self.street[house + 1]

    def test_all(self):
        for house in range(self.houses):
            print self.no_neighbors(house)
        print "\n%d occupided out of %d houses, ratio:%f" % (self.occupy, self.houses, float(self.occupy) / self.houses)

    def print_all(self):
        if(self.houses <= 100):
            print self.street
        print "\n%d occupided out of %d houses, ratio:%f" % (self.occupy, self.houses, float(self.occupy) / self.houses)

    # TODO move out of class
    def test(self):
        self.street[1] = 1
        for house in range(3):
            assert self.no_neighbors(house), "failed test at house %d" % house
        self.print_all()


if __name__ == '__main__':
    houses = 10000
    if (len(sys.argv) > 1):
        houses = int(sys.argv[1])
    n = Neighborhood(houses)
    n.main()
