# class for word-specific logic (word points to a board, but is not a source of truth for board contents)

class Word:
	def __init__(self, puzzle, x, y, isAcross, length):
		self.puzzle = puzzle
		self.x = x
		self.y = y
		self.isAcross = isAcross
		self.length = length

	def readWord(self):
		word = ''
		x = self.x
		y = self.y
		ind = 0

		while ind < self.length:
			word += self.puzzle.board[y][x]
			ind += 1
			if self.isAcross:
				x += 1
			else:
				y += 1

		return word

	def writeWord(self, word):
		x, y = self.x, self.y
		for letter in word:
			self.puzzle.board[y][x] = letter
			if self.isAcross:
				x += 1
			else:
				y += 1

	def __repr__(self):
		return self.readWord()