# Jason Angell
# 10/14/2024 10:56pm
# First attempt at a general-purpose crossword generator.

import sys

from pdb import set_trace

from source.puzzle import Puzzle

if __name__ == '__main__':

	# corner = """#D..
	# .I..
	# .F..
	# .F.#
	# TERS
	# ER#L"""
	# p = Puzzle(corner)
	# results = p.solve()
	# print('\n\n'.join(results))

	# sys.exit(0)

	# beg = Puzzle.fromCSV('./beg.csv')
	# results = beg.solve()

	# print('\n\n'.join(results))

	# sys.exit(0)
	# # basic 5x5, NYT mini 10/8
	# puzz = """ADAMS
	# SAUCE
	# I...E
	# FERNS
	# #SAG#"""
	# bigPuzz = """SMBC#HAUNT
	# .R..#ELSEE
	# ANGRYLEMON
	# .O.EE.#.AB
	# """
	# megPuzz = """....#.....#....
	# ....#.....#....
	# ANGRYLEMON#....
	# GODEEP#CABINETS
	# ###....#.....##
	# ........#......
	# .....#.....#...
	# ....#.....#....
	# ...#.....#.....
	# ......#SNAILPOD
	# ##.....#....###
	# PORTIMAO#......
	# ....#BABYTYRANT
	# ....#.....#....
	# ....#.....#...."""
	begPuzz = """#...##D..#F..##
	....#.I..#O....
	....#.F..#R....
	....#.F.##G....
	###.T.E..#I..##
	....H.R#..V...#
	....E###..E#...
	...#Q..#..N#...
	...#U..###E....
	#...E..#P.S....
	##..S#..A.S..##
	....T##.R.#....
	....I#..O.#....
	....O#..O.#....
	##..N#..N##...#"""
	
	p = Puzzle(begPuzz)
	result = p.solve()
	print('result:')
	print(result)








