#!/usr/local/bin/python3

"""
Written by David Theriault

General tool for text searching
in files or searching for files by name.

Multi-threaded, colorized output.

search.py --help
"""

import os
import sys
import re
import argparse
import threading
import time
import signal
from threading import Thread
from io import open
import codecs

from colorama import init, Fore, Back, Style
from mylogger import MyLogger

# init color.
init()
LOG_DIR = None
ELLIPSIS = '\u2026'
class Search:
    def __init__(self, phrase, extensions=False, ignore_case=False, before=None, after=None, regex=False, find=False, exclude=None, exdir=None, depth=None, debug=False):
        self.start = time.time()
        before = before or 0
        after  = after  or 0
        log_level = 'error'
        if(debug):
            log_level = 'debug'
            print("Search, args:%s" % str(locals()))
        self.log = MyLogger(LOG_DIR, log_level, "search.py")
        self.max_width = 40
        self.phrase = phrase
        self.before=before
        self.after=after
        self.regex = regex
        self.find = find
        self.max_depth = depth
        reg_phrase = phrase

        ignore_dir = '.svn .cvs .git .snapshot .cache'
        self.file_ex_list = 'jpg jpeg gif png tar zip gzip gz tgz pdf jar wav mp3 avi mpeg swp swx psd yml dll exe pdb pyc'
       
        if(ignore_case):
            ignore_case = re.I
        else:
            ignore_case = 0

        if(exdir):
            ignore_dir += ' '+' '.join(exdir)

        if(exclude):
            self.file_ex_list += ' '+' '.join(exclude)
        try:
            if(not self.regex):
                reg_phrase = re.escape(phrase)
            
            self.re_phrase = re.compile(reg_phrase, ignore_case)
            self.ex_dir = re.compile("^(%s)$" % re.sub(' ', ')|(', ignore_dir))

            # If extension then can ignore file_ex_list since we're only looking for pos matches
            if(extensions):
                in_file_regex = "\.((%s))$" % ')|('.join(extensions)
                self.match = True
                self.reg_file = re.compile(in_file_regex)
                self.log.debug("in_file_regex:%s" % in_file_regex)
            else:
                self.match = False
                ex_file_regex = "\.((%s))$" % re.sub(' ', ')|(', self.file_ex_list)
                self.reg_file = re.compile(ex_file_regex, ignore_case)
                self.log.debug("ex_file_regex:%s" % ex_file_regex)
        except:
            self.log.error("Reg Ex compile error:%s" % str(sys.exc_info()[0]))
            sys.exit(1)
        
        self.num_file_search = 0
        self.num_file_match  = 0
        self.num_match       = 0
        self.total_match     = 0
        self.file_error      = 0
        self.dir_error       = 0
        self.thread_error    = 0
        self.thread_limit    = 50
        self.use_threading   = True
        self.skip_sym_dir    = True
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def search(self):
        self.dirSearch()
        while( threading.activeCount()>1):
            time.sleep(.2)
        #for thread in threading.enumerate():
        #    if(thread is not threading.currentThread()):
        #        thread.join()
        seconds = time.time() - self.start
        minutes = 0
        if(seconds > 60):
            minutes = int(seconds / 60)
            seconds = seconds % 60
        if(minutes):
            print("\n%sSearch Completed in %s%d%s min %s%1.3f%s sec" % \
                (Style.BRIGHT, Fore.BLUE, minutes, Fore.RESET, Fore.BLUE, seconds, Fore.RESET))
        else:
            print("\n%sSearch Completed in %s%1.3f%s sec" % \
                (Style.BRIGHT, Fore.BLUE, seconds, Fore.RESET))
        # TODO don't print('s' for singular results.
        print("Searched %s%d%s Files, Matched:%s%d%s Files, Line Matches:%s%d%s, Total Matches:%s%d%s" % \
                (Fore.BLUE, self.num_file_search, Fore.RESET, Fore.BLUE, self.num_file_match, Fore.RESET, Fore.BLUE, self.num_match, Fore.RESET, Fore.BLUE, self.total_match, Fore.RESET))
        if(self.thread_error):
            print("%s%d%s Thread Errors" % (Fore.RED, self.thread_error, Fore.RESET))
        if(self.file_error):
            print("%s%d%s File Errors" % (Fore.RED, self.file_error, Fore.RESET))
        if(self.file_error):
            print("%s%d%s Directory Errors" % (Fore.RED, self.dir_error, Fore.RESET))
        print(Style.RESET_ALL,)

    def findMatch(self, fullpath, filename=None):
        self.log.debug("%s file matches phrase:%s ?" % (filename, self.phrase))
        self.num_file_search += 1
        if(not filename):
            filename = os.path.split(fullpath)[-1]
        self.log.debug("findMatch filename:%s, matching against:%s, fullpath:%s" % (filename, self.phrase, fullpath))
        if(self.regex):
            match = bool(self.re_phrase.match(filename))
        else:
            match = self.phrase == filename
            self.log.debug("match:%s" % str(match))
        if(match):
            self.num_file_match += 1 
            print("%s%s%s" % \
                (Fore.GREEN, fullpath, Fore.RESET))
        return bool(match)

    def dirSearch(self, dirname='./', depth=0):
        self.log.debug("dirSearch lookiing in dir %s" % dirname)
        assert os.path.isdir(dirname), "dirSearch did not get a dir: %s" % dirname


        try:
            files = os.listdir(dirname)
        #except OSError as (errno, strerror):
        except OSError as errno:
            if(not self.dir_error):
                self.log.warn("I/O error({0}): {1}".format(errno))
            self.dir_error += 1
            return

        dirs = []
        for filename in files:
            fullpath = os.path.join(dirname, filename)
            if(os.path.isfile(fullpath)):
                if(self.find):
                    if(not self.findMatch(fullpath, filename)):
                        continue
                elif(self.match == bool(self.reg_file.search(filename))):
                    if(os.path.islink(fullpath)):
                        link_path = os.path.realpath(fullpath)
                        self.log.debug("*** file %s is a sym link, located at %s going to %s" % (fullpath, os.path.realpath(dirname), link_path))
                        self.log.debug("checking if %s == %s" % (os.path.realpath(dirname),  os.path.split(link_path)[0]))
                        # Check if symbolic path resovles to this same directory.
                        if(os.path.realpath(dirname) == os.path.split(link_path)[0]):
                            # If symbolic link goes to this same dir then don't search it.
                            self.log.debug("%s is a link is in this dir, skipping to avoid searching same file twice." % filename)
                            continue
                    else:
                        self.log.debug("%s is not a link" % filename)
                    # Using more than 1 thread here only slows down
                    if(self.use_threading and threading.activeCount() < 1 ):
                        try:
                            t = Thread(target=self.fileSearch, args=(fullpath,))
                            t.start()
                        except:
                            self.thread_error +=1
                            if(not self.thread_error):
                                self.log.error("file thread creation error:", sys.exc_info()[0])
                            self.fileSearch(fullpath)
                    else:
                        self.fileSearch(fullpath)
                else:
                    self.log.debug("file extention %s found on exclude list:%s" %(filename, self.file_ex_list))
            elif(os.path.isdir(fullpath)):
                if(self.ex_dir.match(filename)):
                    self.log.debug("exculde dir match on:%s" % filename)
                    continue
                if( self.skip_sym_dir and os.path.islink(fullpath)):
                    self.log.debug("skipping %s, it's a symlink")
                    continue
                #self.log.debug("Got dir %s" % filename)
                # Search will be done Breadth first, not Depth, process dirs after files.
                dirs.append(fullpath)
            else:
                self.log.debug("Unknown filetype:%s" % fullpath)
                continue
        self.log.debug("searching of %s complete, going to dirs:%s" % (dirname, str(dirs)))
        self.log.debug("max_depth:%s, depth now:%d" % (str(self.max_depth), depth))
        if(self.max_depth is None or self.max_depth > depth):
            for dir in dirs:
                if(self.find):
                    self.findMatch(dir)
                self.log.debug("calling nested dir:%s" % dir)
                if(self.use_threading and threading.activeCount() < self.thread_limit):
                    try:
                        t = Thread(target=self.dirSearch, args=(dir,depth+1,))
                        t.start()
                    except:
                        if(not self.thread_error):
                            #self.log.error("dir thread creation error:%s" % str(sys.exc_info()[0]))
                            self.log.error("dir thread creation error:%s" % str(sys.exc_info()))
                        self.thread_error +=1
                        self.dirSearch(dir, depth+1)
                else:
                    self.dirSearch(dir, depth+1)
                self.log.debug("return to level %s from %s" % (dirname, dir))

    def wrapRed(self, line):
        return Fore.RED + line + Fore.RESET
    
    def wrapYellow(self, line):
        return Fore.YELLOW + line + Fore.RESET

    def replace(self, matchobj):
        return self.wrapRed(matchobj.group(0))

    def trunk(self, line, max_width=None):
        max_width = max_width or self.max_width
        width = len(line)
        if(width >= max_width):
            line = line[:max_width] + self.wrapYellow(ELLIPSIS + " \n")
        return line

    def trunkMatch(self, line):
        end = len(line)
        last_match = 0
        trunk_line = ''
        trunk_limit = int(self.max_width / 2)
        last_print = 0
        matches = 0
        for match in self.re_phrase.finditer(line):
            matches += 1
            match_start = match.start()
            match_end   = match.end()
            self.log.debug("last_match:%d, match_start:%d, match_end:%d, matches:%d" % (last_match, match_start, match_end, matches))
            # short circuit if matches are touching.
            if(match_start == last_match or match_start == last_print + 1):
                trunk_line += self.wrapRed(line[match_start:match_end])
                last_print = match_end
                last_match = match_end 
                continue

            # not first, print right buffer of previous match
            if(matches > 1):
                self.log.debug("overlap? match_start %d - last_match %d (= %d) > trunk_limit %d: %s" % (match_start, last_match, match_start - last_match, trunk_limit, str(match_start - last_match > trunk_limit)))
                # If no overlap between previous match right limit and current.
                if(match_start - last_match > trunk_limit):
                    # Need to print to right of last match up to trunk
                    self.log.debug("adding to trunk right of prev trunked:%s" % line[last_match:last_match + trunk_limit]+ self.wrapYellow(ELLIPSIS))
                    trunk_line += line[last_match:last_match + trunk_limit] + self.wrapYellow(ELLIPSIS)
                    last_print = trunk_limit
                # print up to the overlap
                else:
                    self.log.debug("adding to trunk right of prev full:%s" % line[last_match:match_start ])
                    trunk_line += line[last_match:match_start]
                    last_print = match_start

            # Print left buffer of current match

            # should not have printed the current match yet
            assert last_print <= match_start, "last_print %d <= match_start %d" % (last_print, match_start)
            # prev match is within left bound.
            #if(last_print + trunk_limit < match_start):
            if( match_start - last_print <= trunk_limit):
                trunk_line += line[last_print:match_start]
                self.log.debug("adding to trunk:%s" % line[last_print:match_start])
                last_print = match_start 
            # prev match is beyond left bound, trunk
            else:
                # print backwards from match up to limit
                left_bound = match_start - trunk_limit
                assert left_bound >= 0, "bad math left_bound %d >= 0; match_start:%d, trunk_limit:%d, last_print:%d" \
                        % (left_bound, match_start, trunk_limit, last_print)
                assert left_bound < match_start, "bad math left_bound %d < match_start %d" % (left_bound, match_start)
                trunk_line += self.wrapYellow(ELLIPSIS) + line[left_bound:match_start ]
                self.log.debug("adding to trunk:%s" % self.wrapYellow(ELLIPSIS) + line[left_bound:match_start ])
                last_print = match_start 
            
            assert last_print <= match_end, "last_print %d <= match_end %d" % (last_print, match_end)

            # Add the match 
            trunk_line += self.wrapRed(line[match_start:match_end])
            self.log.debug("adding to trunk:%s" % self.wrapRed(line[match_start:match_end]))
            last_print = match_end
            last_match = match_end

        if(matches > 0):
            # Capture final right buffer
            # do we need to trunk
            self.log.debug("do we need final right? end:%d, last_print:%d, trunk_limit:%d" % (end, last_print, trunk_limit))
            if(end == last_print):
                self.log.debug("nothing to add")
            elif(end - last_print > trunk_limit):
                trunk_line += line[last_print:last_print + trunk_limit] + self.wrapYellow(ELLIPSIS + "\n")
                self.log.debug("adding to trunk:%s" % line[last_print :last_print + trunk_limit] + self.wrapYellow(ELLIPSIS))
            else:
                trunk_line += line[last_print:]
                self.log.debug("adding to trunk:%s" % line[last_print:])
            self.log.debug("returning trunk_line:\n%s\nmatches:%d" % (trunk_line, matches))
        return (trunk_line, matches)

    def fileSearch(self, filename):
        self.log.debug("checking file %s" % filename)
        assert os.path.isfile(filename), "fileSearch did not get a file: %s" % filename
        try:
            fh = codecs.open(filename, 'r', encoding='utf-8', errors='ignore')
        except IOError as errno:
            if(not self.file_error):
                self.log.warn("I/O error({0}): {1}".format(errno))
            self.file_error += 1
            return
        self.num_file_search += 1
        line_num=0
        line_matches=0
        matches=0
        before = self.before
        after = self.after
        after_left = 0
        before_lines = [''] * before
        file_summary = ''
        
        for line in fh:
            line_num += 1
            replacements = 0
            if(len(line) > self.max_width):
                (line, replacements) = self.trunkMatch(line)
            else:
                # replace is called for every non-overlapping occurrence of pattern.
                (line, replacements) = self.re_phrase.subn(self.replace, line)
            # If line matched
            if(replacements):
            #self.log.debug("line now:%s\nreplacements:%d" % (line, replacements))
                line_matches+=1
                if(before):
                    for b_line_num in range(line_num - before, line_num):
                        marker = b_line_num % before
                        if(not before_lines[marker]):
                            continue
                        
                        file_summary += self.wrapYellow("%d-" % b_line_num)
                        file_summary += "\t%s" % self.trunk(before_lines[marker])
                        before_lines[marker] = ''
                if(after):
                    after_left = after
                        
                file_summary += Fore.YELLOW + Style.BRIGHT + "%d:" % line_num + Style.RESET_ALL

                matches += replacements
                file_summary += "\t%s" % line
            elif(after_left):
                file_summary += Fore.YELLOW + "%d+" % line_num + Fore.RESET
                file_summary += "\t%s" % self.trunk(line)
                after_left -= 1
            # If we just printed a line or an after line don't record this line for before or could lead to double printing
            elif(before):
                before_lines[line_num % before] = line
        fh.close()
        # TODO when using threads need to add locks so that only one thread prints results at a time.
        if(line_matches):
            self.num_file_match+=1
            header = "\n%sline matches:%d%s\t%smatches:%d%s\t%s%s%s" % \
                    (Fore.CYAN, line_matches, Fore.RESET, Fore.CYAN, matches, Fore.RESET, Fore.GREEN, filename, Fore.RESET)
            if(line_matches >= 30):
                file_summary += header + "\n"
            # No need to print newline, file_summary will always end with a newline
            print(header + "\n" + file_summary,)
            # For long matches print(the header again.
            self.num_match+=line_matches
            self.total_match += matches

    def signal_handler(self, signal, frame):
        """ Capture Ctrl+C signal, useful for multithreaded programs."""
        self.log.error("\nCtrl+C exit")
        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search for text in files')
    parser.add_argument('phrase', help='The phrase to be searched for')
    parser.add_argument('extensions', nargs='*',help='File extenions to use, assumed to be prefixed with \'.\', space separated e.g. pl pm')
    parser.add_argument('-i', '--ignore_case', action='store_true', help='Ignore case when matching against phrase.')
    parser.add_argument('-a', '--after', type=int, nargs='?', const=1, help='Number of lines to display after match.')
    parser.add_argument('-b', '--before', type=int, nargs='?', const=1, help='Number of lines to display before match.')
    parser.add_argument('-c', '--after_before', type=int, nargs='?', const=1, help='Number of lines to display before and after a match.')
    parser.add_argument('-r', '--regex', action='store_true', help='treat phrase as a regular expression')
    parser.add_argument('-f', '--find', action='store_true', help='instead of searching in file, simply find the file path')
    parser.add_argument('-e', '--exclude', nargs='+', help='additional file extentions to ignore')
    parser.add_argument('-d', '--exdir', nargs='+', help='additional directorys to ignore')
    parser.add_argument('-D', '--depth', type=int, help='Maximum depth of directories to go in.')
    #parser.add_argument('-o', '--or', help='or contain this phrase', dest='phrase2')

    parser.add_argument('--debug', action='store_true', help='run in debug mode')
    args = parser.parse_args()
    send_args = vars(args)
    if(send_args['after_before']):
        send_args['before'] = send_args['after_before']
        send_args['after'] = send_args['after_before']
    del send_args['after_before']
    print("\tsearching" + ELLIPSIS)
    s = Search(**send_args)
    s.search()
