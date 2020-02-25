#!/usr/local/bin/python3

"""
Written by David Theriault

Categorize chase bank credit card statements.
Creates a new csv file with a new category column.

"""
import re
import os
import sys
import argparse


class Categorize:
    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        # Note ending , needed to avoid single entrie strings being joined on their letters.
        categories = (
            ("Car",             ("BMW", "auto works", "Honda", 'rgstry','fee-boston', 'subaru')),
            ("Pet",             ("Stoneham animal", "\\bpet\\b", "VETERINARY",)),
            ("Medical",         ("hospital", "pharmacy", "children's", "PEDIATRIC", "BIDMC", "fenway community", "dental", "walgreens", "chpa",\
                                 "therap", "doctors", "urgent care", "OTOLARYNGOLOGIC", "lahey", "funeral",)),
            ("Commute",	        ("mbta", "\\btoll\\b", "parking", "charlie", "rmv", "zpass", "city of boston par", "gapos", "congress st")),
            ("Donation",	("aclu", "wpy")),
            ("Utility",	        ("wakefield municipal", 'wmgld', 'MA DPH')),
            ("Fast Food",	("mcdonald", "burger", "panera", "grubhub", "five guys", "popeyes", "domino", "ice c", "cafe", "AUBONPAIN", \
                           "grabull", "common man so. irving", "Nick's", "vending", "dunkin", "taco", "concessio", "starbucks", "subway", "cosi",)),
            ("Gas (unleaded)",	("\\bgas\\b", "exon", "mobil", "shell oil", "sunoco", "AL Prime", "gulf")),
            ("Groceries",	("costco", "whole foods", "stop ", "shaws", "wholefds", "\\bmart\\b", "bakery", "cumberland farms", \
                           "farm land", "wine", "star market")),
            ("Dining",	        ("seasons 52", "pizza", "restaurant", "gourmet","scholar", "MARGARITAS", "mexico lindo", \
                                "southern kin cookhou", "house of ", "diner", "top of the hub", "elephant", "steak", "kitchen", \
                                "chili", "roost", "millennium place", "the fours boston", "brick oven", '\\bbar\\b')),
            ("Recreation",	("zoo", 'imax', 'theatre', 'park', "orchard", "busters", "cinema", "fandango", "golf", "\\bfarm\\b")),
            ("Shopping",	("target", "amazon", "macy", "ikea", "amz", "old navy", "dick's", "payless", "party", \
                          "overstock", "wagon wheel", "carseat", "talbots", "staples", "Christmas", "cardstore", \
                          "michaels", "Prudential center", "memories in an instan", 'tjmax', 'rei', 'vistaprint',)),
            ("Media",	        ("apple", "hulu", "cbs", "verizon", "itunes", "comcast", "hbo", "showtime", "steam", \
                               "audible", "theimageconn", "eig", "book", "netflix", )),
            ("Repairs",	        ("plumbing","unique indoor", "hart hdwe", "lowes", "home depot", )),
            ("Travel",          ("United ","tsa",)),
            ("Business",	("self storage", 'ASSOC. CRED SERV.', "linkedin",)),
            ("Health",	        ("gym", "UHC motion", "fitness", "cbd", "barber", "pod", "salon", "tippy", "care",)),
            ("Furniture",       ("furniture", "smartmove", "wayfair" )),
            #("Education",       ),
        )

        # chase left, custom right
        chase_category_map = { 
            "Shopping": "Shopping",
            "Groceries": "Groceries",
            "Gas": "Gas (unleaded)",
            "Entertainment":"Recreation",
            "Travel":"Travel",
            "Health & Wellness": "Health",
            "Gifts & Donations": "Donation",
            "Home": "Repairs",
            "Automotive":"Car",
            "Education":"Education",
        }

        compiled_categories = {}
        order = []
        for entry in categories:
            category = entry[0]
            #if(self.DEBUG):
            phrases = entry[1]
            order.append(category)
            comp_str = '(' + ')|('.join(phrases) + ')'
            if(self.DEBUG):
                print("\ncompiling for category:%s\nusing %s\ninto string:%s" % (category, phrases, comp_str))
            compile = re.compile('(' + ')|('.join(phrases) + ')', re.I)
            if(self.DEBUG):
                print("compiled:%s" % (compile))
            compiled_categories[category] = compile

        self.order = order
        self.compiled_categories = compiled_categories
        self.chase_category_map = chase_category_map
        
    def compare(self, description, category="", amount="", line=""):
        # first compare custom regex
        for custom_category in self.order:
            if(bool(self.compiled_categories[custom_category].search(description))):
                if(self.DEBUG):
                    print("matched custom %s for %s\t%s" % (custom_category , description, line))
                return custom_category
        # next defer to chase categories
        if(category in self.chase_category_map):
            if(self.DEBUG):
                print("matched chase map %s for %s\t%s" % (category , str(self.chase_category_map), line))
            return self.chase_category_map[category]
        # assume if meal is $50 or more it was dining, otherwise fast food
        if(category == 'Food & Drink'):
            custom_category = None
            if(float(amount) >= 50):
                custom_category = 'Dining'
            else:
                custom_category = 'Fast Food'
            if(self.DEBUG):
                print("matched food & drink, setting category %s for amount %s\t%s" % (custom_category , amount, line))
            return custom_category
        print("UNMATCHED:description:%s, line:%s" % (description, line))
        return "Unknown"

class ProcessFile:
    # Chase columns
    # Type,Trans Date,Post Date,Description,Amount
    # column array mappings
    Date        = 0
    Post_Date   = 1
    Description = 2
    Category    = 3
    Type        = 4
    Amount      = 5
    # new columns
    NEW_HEADER  = "Trans Date,Trans Period,Description,Category,Amount\n"

    def __init__(self, old_csv_filename, new_csv_filename=None, debug=False):
        self.DEBUG = debug
        self.old_csv_filename = old_csv_filename
        self.new_csv_filename = new_csv_filename
        # TODO assert old filename exists
        self.categorize = Categorize(self.DEBUG)

    def process(self):
        try:
            old_csv_fh = open(self.old_csv_filename, 'r') 
            new_csv_fh = open(self.new_csv_filename, 'w')
        except IOError:
            print("I/O error({0}): {1}".format(sys.exc_info()[2]))
        first_line = old_csv_fh.readline()
        #new_csv_fh.write(ProcessFile.NEW_HEADER)
        new_lines = []
        for line in old_csv_fh:
            columns = line.split(',')
            if(columns[ProcessFile.Type] != 'Sale'):
                if (self.DEBUG):
                    print("skipping non sale:%s" % line.rstrip()) 
                continue
            # strip out the day
            month_year = columns[ProcessFile.Date][0:3] + columns[ProcessFile.Date][-4:]
            # strip out negative sign
            amount = columns[ProcessFile.Amount].strip('-')
            category = self.categorize.compare(columns[ProcessFile.Description], columns[ProcessFile.Category], amount, line.rstrip())
            new_line = ','.join((columns[ProcessFile.Date], month_year, columns[ProcessFile.Description], category, amount))
            new_lines.append(new_line)
            #new_csv_fh.write(new_line)
        new_lines.reverse()
        for new_line in new_lines:
            new_csv_fh.write(new_line)
        old_csv_fh.close()
        new_csv_fh.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Chase Credit Card CSV')
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode')
    parser.add_argument('-o', '--old_csv_filename', default='chase.csv', help='The filename to parse')
    parser.add_argument('-n', '--new_csv_filename', default='new_chase.csv', help='The filename to output to, will overwrite if exists')
    args = parser.parse_args()
    send_args = vars(args)

    process_file = ProcessFile(**send_args)
    process_file.process()
