# class for puzzle logic, which includes source(s) of board truth and filling (or "solving") tools

import csv
import os
import time     # currently, only used for profiling

from copy import deepcopy
from pdb import set_trace

from .searcher import Searcher
from .word import Word


class Puzzle:
    writePath = './results/'

    def __init__(self, puzzleText: str):
        """Constructor. puzzleText should be NxN, with "." for blanks and "#" for blocks, case-insensitive.

        Args:
            puzzleText (str): Text representation of the puzzle board. Should have '.' for blanks, '#' for blocks, and
                be comma-delimited, with line breaks separating rows.
        """
        self.board = []
        for line in puzzleText.split():
            self.board.append(list(line))

        self.height = len(self.board)
        self.width = len(self.board[0])

        # now, collect the "words", based on starting position, direction, and length
        self.across = []
        self.down = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                # now we have each letter, with its x and y coord
                # x is left-to-right distance from the left side of the puzzle, and y is top-to-bottom distance from the top of the puzzle

                if self.board[y][x] == '#':
                    continue

                # this indicates that this coordinate is the start of an across word
                if x == 0 or self.board[y][x-1] == '#':
                    ind = x + 1
                    while ind < self.width and self.board[y][ind] != '#':
                        ind += 1
                    self.across.append(Word(self, x, y, True, ind - x))

                # and this indicates that this coord is the start of a down word
                if y == 0 or self.board[y-1][x] == '#':
                    ind = y + 1
                    while ind < self.height and self.board[ind][x] != '#':
                        ind += 1
                    self.down.append(Word(self, x, y, False, ind - y))

        self.searcher = Searcher()

    @classmethod
    def fromCSV(cls, csvPath):
        with open(csvPath, 'r') as f:
            csvReader = csv.reader(f)
            toRet = '\n'.join(''.join(l or '.' for l in row) for row in csvReader)
        return cls(toRet)

    def __deepcopy__(self, memo):
        """Overriding the default deepcopy to share words & searcher"""
        new_inst = type(self).__new__(self.__class__)

        new_inst.searcher = self.searcher

        new_inst.across = deepcopy(self.across, memo)
        new_inst.down = deepcopy(self.down, memo)
        new_inst.board = deepcopy(self.board, memo)
        return new_inst

    def setSearcher(self, searcher: Searcher, retainCache: bool = False):
        """Update the default searcher.

        Args:
            searcher (Searcher): New searcher object to use.
            retainCache (bool, optional): If True, keep the search cache from the previous searcher. Default is False.
        """
        if retainCache:
            searcher._cachedSearches = self.searcher._cachedSearches
        self.searcher = searcher

    def __repr__(self):
        return '\n'.join(' '.join(row) for row in self.board)

    @property
    def words(self):
        return self.across + self.down

    @property
    def incompleteWords(self):
        toRet = []
        for word in self.words:
            if '.' in str(word):
                toRet.append(word)
        return toRet


    @property
    def hashableString(self):
        return ''.join(''.join(row) for row in self.board)

    def getMostConstrainedWord(self):
        # create a dictionary that maps from the word _object_ to how many possible fits it has
        constraint = {}
        constraintTime = {}
        mostConstrainedLen = 1e99
        mostConstrainedWord = None

        for word in self.incompleteWords:
            iterStart = time.time()
            options = self.searcher.find(str(word))
            constraint[word] = len(options)
            if len(options) < mostConstrainedLen:
                mostConstrainedLen = len(options)
                mostConstrainedWord = word
            iterEnd = time.time()
            constraintTime[word] = iterEnd - iterStart
        from pprint import pprint
        # pprint(constraintTime)
        # set_trace()

        return mostConstrainedWord

    def solve(self, results=[], seen=[]):

        startTime = time.time()

        if self.hashableString in seen:
            # avoid repeat work by bailing if we've seen the same puzzle state before
            return

        seen.append(self.hashableString)

        postHashCheckTime = time.time()

        # "completed puzzle" check
        if not len(self.incompleteWords):
            results.append(str(self))
            writePath = os.path.join(self.writePath, f'result_{len(results)}.csv')
            print(f'{len(results)} results found! writing to {writePath}')
            self.writeToCSV(writePath)
            return results

        postCompletionCheckTime = time.time()

        mostConstrainedWord = self.getMostConstrainedWord()

        postConstraintTime = time.time()

        options = self.searcher.find(str(mostConstrainedWord))
        print(f'current puzzle state:\n{self}')
        print(f'most constrained word is {mostConstrainedWord}')
        print(f'options: {options}')
        print('~~~\n')

        postOptionsTime = time.time()

        for option in options:

            curOptTime = time.time()

            mostConstrainedWord.writeWord(option.word)

            postWriteTime = time.time()

            innerPuzzle = deepcopy(self)

            postCopyTime = time.time()

            dHash = postHashCheckTime - startTime
            dCompCheck = postCompletionCheckTime - postHashCheckTime
            dConstraint = postConstraintTime - postCompletionCheckTime
            dOptions = postOptionsTime - postConstraintTime
            dWrite = postWriteTime - curOptTime
            dCopy = postCopyTime - postWriteTime

            # set_trace()

            innerPuzzle.solve(results=results, seen=seen)

        return results

    def writeToCSV(self, path):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            for row in self.board:
                writer.writerow(row)
