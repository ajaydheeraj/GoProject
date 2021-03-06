### This will hold game data

import pygame
import copy
from static import *
from textBoxes import *
from stones import *

# game data is stored here
class Data(object):
	playerColors = {1: Colors.BLACK, 2: Colors.WHITE}

	# initializes data
	def __init__(self):
		self.me = None
		self.other = None
		self.otherInGame = False
		self.mousePos = (0, 0)
		self.start = True
		self.inGame = False
		self.removeStones = False
		self.gameOver = False
		self.textBox = None
		self.instructionsScreen = False
		self.startButtons = self.createStartButtons()
		
	# starting the game data
	def initGame(self):
		self.board = self.initBoard()
		self.oldBoard = copy.deepcopy(self.board)
		self.turn = 1
		self.lastTurnPassed = False
		self.p1score = 0
		self.p2score = 0
		self.start = False
		self.inGame = True
		self.removeStones = False
		self.gameOver = False
		self.textBox = None
		self.lastPlaced = None
		self.playerBox = PlayerBox()
		self.otherReadyToRemoveStones = False
		
	# creates the start screen buttons and returns them in a list
	def createStartButtons(self):
		pb = PlayButton()
		ib = InstructionsButton()
		titleBox = TitleBox()
		return (pb, ib, titleBox)

	# creates a 19x19 board of "Nones"
	@staticmethod
	def initBoard():
		board = []
		for i in range(GoConstants.COLUMNS+1):
			row = []
			for j in range(GoConstants.ROWS+1):
				row.append(None)
			board.append(row)
		return board

	# adds a stone to the board based on where the player clicked
	def placeStone(self, x, y):
		row, col = self.closestCorner(x, y)
		if row < 0 or col < 0 or row > GoConstants.ROWS or col > GoConstants.COLUMNS:
			return "Not on board!"
		
		if self.turn == 1:
			color = Colors.BLACK
		elif self.turn == 2:
			color = Colors.WHITE

		if self.board[row][col] == None:
			pygame.mixer.music.load('click_sound.wav')
			pygame.mixer.music.play()
			
			self.lastPlaced = (row, col)
			self.oldBoard = copy.deepcopy(self.board)
			self.board[row][col] = Stone(row, col, color)
			self.updateBoard()
			self.passTurn()
			return row, col
			
	# removes a stone upon click
	def removeStone(self, x, y):
		row, col = self.closestCorner(x, y)
		self.board[row][col] = None

	# returns row and col of the closest corner
	@staticmethod
	def closestCorner(*args):
		# the case if a tuple of coordinates is inputted instead of an x and a y
		if len(args) == 1:
			args = args[0]

		(x, y) = args
		row = Functions.round((y - GoConstants.MARGIN) / GoConstants.TILESIZE)
		col = Functions.round((x - GoConstants.MARGIN) / GoConstants.TILESIZE)
		return row, col

	# changes between player 1 and player 2
	def passTurn(self, justPassed=False):
		# if this function was called as a resulf of a player just passing, not
		# from the placeStone or undoMove functions
		if justPassed:
			if self.lastTurnPassed:
				self.playerBox.update(off=True)
				self.textBox = DeadStoneBox("remove dead stones")
				self.lastPlaced = None
			else:
				self.lastTurnPassed = True
				self.textBox = None
		self.turn = 3 - self.turn
		self.updateBoard()
		self.playerBox.update()
		for row in self.board:
			for corner in row:
				if corner != None:
					corner.wasChecked = False

	# updates the board (removes any pieces that have been captured)
	def updateBoard(self):
		for row in self.board:
			for corner in row:
				if corner != None and corner.color == self.playerColors[3 - self.turn]: # only check the other players' pieces
					self.board = corner.updatePiece(self.board)

	# if a player presses "u", they will get their turn back
	def undoMove(self):
		if self.board == self.oldBoard:
			return
		self.board = self.oldBoard
		self.lastPlaced = None
		self.textBox = None
		self.passTurn()
		
	# gets the scores from the board at the end of the game
	def getScore(self):
		# checks each square to see whether it belongs to black or white
		for i in range(len(self.board)):
			row = self.board[i]
			for j in range(len(row)):
				corner = row[j]
				if isinstance(corner, Stone):
					color = corner.color
				elif corner == None:
					color = self.getColor(self.board, i, j)
				
				if color == Colors.BLACK:
					self.p1score += 1
				elif color == Colors.WHITE:
					self.p2score += 1
			
	# at the end of the game, returns the owner of an empty square
	@staticmethod
	def getColor(board, row, col):
		directions = ["up", "down", "left", "right"]
		color = None
		
		# checks in a given direction to find out who an empty space belongs to
		def checkDirection(board, row, col, direction):
			dir = GoConstants.DIRECTIONS[direction]
			newRow, newCol = row + dir[1], col + dir[0]
			if (not (0 <= newRow <= GoConstants.ROWS) or not (0 <= newCol <= GoConstants.COLUMNS)):
				return None
			elif isinstance(board[row][col], Stone):
				return board[row][col].color
			else:
				return checkDirection(board, newRow, newCol, direction)
		
		for dir in directions:
			color = checkDirection(board, row, col, dir)
			if color != None:
				break
		
		return color
		
	# checks if it's the local player's turn
	def isMyTurn(self):
		print(Colors.index[self.playerColors[self.turn]])
		return Colors.index[self.playerColors[self.turn]] == self.me