# Classes for search functionality

import re


class Answer:
    def __init__(self, word: str, score: int = -1):
        """Constructor.

        Args:
            word (str): The answer itself.
            score (int, optional): "Score" value for the word. Not using this currently, but it's in the list. Default is -1 ("unknown").
        """
        self.word = word
        self.score = int(score)
        self._len = len(self.word)

    def __repr__(self):
        return self.word

    def __len__(self):
        return self._len

    def matches(self, searchString: str) -> bool:
        """Determines if searched string matches with this answer. Uses regex-ish style formatting.

        For single-letter wildcards, use "." or "_". All other re-style stuff in the given string will be
        used as-is, in a regex-y way. So, for a seven letter word with "ECAU" in positions 2-5, use
        something like this: _ECAU__; and for the equivalent, but where the second letter could be
        an E or an A, use _[ae]cau__.

        Args:
            contains (str): Regex string to search, in the style of python's "re" library.

        Returns:
            bool: True if this word matches the searched string; else, False.
        """
        return re.match(searchString, self.word) is not None


class Searcher:
    # listFile = 'resources/wordlist.txt'
    defaultListFile = 'resources/broda_diehl_list.txt'

    def __init__(self, sourceFiles: list = None):
        """Constructor.

        Args:
            sourceFiles (list of str): List of file paths from which to load answers (and scores).
        """
        sourceFiles = sourceFiles or [self.defaultListFile]
        self.lastSearch = None
        self.answerList = []
        self._wordsInAnswerList = set()
        self._cachedSearches = {}

        for file in sourceFiles:
            self.loadFile(file)

    def addAnswer(self, answer: Answer):
        """Add an answer to self.answerList, if it doesn't exist already in the set.

        Args:
            answer (Answer): The answer to attempt to add to the set.
        """
        if answer.word not in self._wordsInAnswerList:
            self._wordsInAnswerList.add(answer.word)
            self.answerList.append(answer)

    def loadFile(self, fpath: str):
        """Load words into the current word list from the given file.

        Files must be newline-delineated, with semicolons separating word from score. Duplicate words, or words already
        in self.answerList, will be skipped.

        Args:
            fpath (str): Path to the file to add words from.
        """
        print(f'loading word list from {fpath}')
        with open(fpath, 'r') as f:
            for line in f:
                print(f'\r{len(self.answerList)}')
                self.addAnswer(Answer(*line.split(';')))

    def addToCache(self, pattern: str):
        """Add a word-search pattern to the cache.

        Args:
            pattern (str): A regex-style pattern to add to the cache. Note that *each* missing letter is represented by its *own* period.
        """
        searchString = pattern.replace('_', '.').upper()

        # make sure beginning and end are capped
        if not searchString.startswith('^'):
            searchString = '^' + searchString
        if not searchString.endswith('$'):
            searchString += '$'

        self.lastSearch = searchString

        matches = []
        wordLen = len(searchString) - 2                # the minus 2 gets rid of the "start" (^) and "end" ($) regex chars
        for answer in self.answerList:
            if len(answer) == wordLen:                # this check wins us a TON of time - doing this as math instead of as regex cuts down search time by ~70%
                if answer.matches(searchString):
                    matches.append(answer)
        matches.sort(key=lambda w: -w.score)

        self._cachedSearches[pattern] = matches

    def find(self, pattern: str) -> list:
        if pattern not in self._cachedSearches:
            self.addToCache(pattern)

        return self._cachedSearches.get(pattern)


    def fp(self, pattern: str):
        """Stands for "find and print"."""
        matches = self.find(pattern)
        print('search string: ' + self.lastSearch + '\n----------\n' + '\n'.join(str(answer) for answer in matches))


class Interactive:
    exitQuery = 'q'     # this is the thing that exits interactive mode

    def __init__(self):
        self.searcher = Searcher()
        self.lastInput = None

    def run(self):
        print('starting interactive mode! to exit, input "q" and press enter')
        print('-------------------------------------------------------------')
        while True:
            print('search for:')
            query = input('')
            if query == self.exitQuery:
                break
            print()
            self.searcher.fp(query)
            print()

        print('-------------------------------------------------')
        print('now exiting interactive mode. thanks for playing!')
        print('-------------------------------------------------')