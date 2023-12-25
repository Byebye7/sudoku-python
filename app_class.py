import pygame
import random
import pickle
import sys
from settings import *
from buttonClass import *
from sudokusolve import *
import requests
from bs4 import BeautifulSoup

class App:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption("Sudoku!")
		self.hintCounter = 0
		self.running = True
		self.puzzleComplete = False
		self.difficulty = 1
		#self.grid = testBoard2
		self.timer = "00:00:00"
		self.puzzlenum = 0
		self.init_timer = 0
		self.selected = None
		self.mousePos = None
		self.state = "newgame"
		self.playingButtons = []
		self.newgameButtons = []
		self.menuButtons = []
		self.endButtons = []
		self.lockedCells = []
		self.incorrectCells = []
		self.press_counter = 0
		self.cellChanged = False
		self.solvedGrid = [[0 for x in range(9)] for x in range(9)]
		# copy original puzzle to solvedGrid

		self.loadButtons()
		#self.loadGame()
		self.font = pygame.font.SysFont("arial",cellSize//2)


	def run(self):
		while self.running:
			if self.state == "playing":
				self.playing_events()
				self.playing_update()
				self.playing_draw()
			elif self.state == "newgame":
				self.newgame_events()
				self.newgame_update()
				self.newgame_draw()

		pygame.quit()
		sys.exit()

############### NEW GAME FUNCTIONS #############
	def newgame_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mousePos = pygame.mouse.get_pos()
				#check to see if pushed any buttons
				for button in self.newgameButtons:
					if button.pressed(self.mousePos):
						button.function(button.params)

			elif event.type == pygame.KEYDOWN:
				if self.isInt(event.unicode):
					new_difficulty = int(event.unicode)
					if new_difficulty > 0 and new_difficulty < 5:
						self.difficulty = new_difficulty
						self.loadGame()


	def newgame_update(self):
		pass

	def newgame_draw(self):
		self.window.fill(WHITE)

		for button in self.newgameButtons:
			button.draw(self.window)

		pygame.display.update()




################ PLAYING FUNCTIONS############
	def playing_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			#User clicks
			elif event.type	== pygame.MOUSEBUTTONDOWN:

				self.mousePos = pygame.mouse.get_pos()
				#check to see if pushed any buttons
				for button in self.playingButtons:
					if button.pressed(self.mousePos):
						button.function(button.params)

				if self.mouseOnGrid():
					self.selected =  self.mouseOnGrid()

				if self.selected:
					print(self.selected)

			elif event.type == pygame.KEYDOWN:
				if self.selected != None:
					if self.isInt(event.unicode) and not self.selected in self.lockedCells:
						self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
						self.cellChanged = True

					elif event.key == pygame.K_LEFT:
						self.press_counter = 1
						if self.selected[0] > 0:
							self.selected[0] -= 1
					elif event.key == pygame.K_RIGHT:
						self.press_counter = 1
						if self.selected[0] < 8:
							self.selected[0] += 1
					elif event.key == pygame.K_UP:
						self.press_counter = 1
						if self.selected[1] > 0:
							self.selected[1] -= 1
					elif event.key == pygame.K_DOWN:
						self.press_counter = 1
						if self.selected[1] < 8:
							self.selected[1] += 1
					elif (event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE) and not self.selected in self.lockedCells:
						self.grid[self.selected[1]][self.selected[0]] = 0
						self.cellChanged = True



				print(self.selected)
		# Check to see if keys are being held down
		keys = pygame.key.get_pressed()
		if self.selected:
			if keys[pygame.K_UP]:
				self.press_counter += 1
				if self.press_counter > keyPressDelay:
					self.press_counter = int(keyPressDelay*0.7)
					if self.selected[1] > 0:
						self.selected[1] -= 1
			if keys[pygame.K_DOWN]:
				self.press_counter += 1
				if self.press_counter > keyPressDelay:
					self.press_counter = int(keyPressDelay*0.7)
					if self.selected[1] < 8:
						self.selected[1] += 1
			if keys[pygame.K_LEFT]:
				self.press_counter += 1
				if self.press_counter > keyPressDelay:
					self.press_counter = int(keyPressDelay*0.7)
					if self.selected[0] > 0:
						self.selected[0] -= 1
			if keys[pygame.K_RIGHT]:
				self.press_counter += 1
				if self.press_counter > keyPressDelay:
					self.press_counter = int(keyPressDelay*0.7)
					if self.selected[0] < 8:
						self.selected[0] += 1


	def playing_update(self):
		self.mousePos = pygame.mouse.get_pos()
		for button in self.playingButtons:
			button.update(self.mousePos)
		if self.cellChanged:
			if self.puzzleComplete:
				self.puzzleComplete = False
			self.incorrectCells.clear()
			self.cellChanged = False
			if self.unfinishedCells(self.grid)[0] == -1:
				# check if grid is correct
				self.checkAllCells()
				if not self.incorrectCells:
					# Everything is correct!
					self.puzzleComplete = True

	def playing_draw(self):
		self.window.fill(WHITE)
		if self.selected:
			if not self.selected in self.lockedCells:
				self.drawSelection(self.window,self.selected)
			else:
				self.drawSelection(self.window,self.selected,color=GRAY)
		self.drawGrid(self.window)

		for button in self.playingButtons:
			button.draw(self.window)

		self.drawNumbers(self.window)

		if self.puzzleComplete:
			textSurface = pygame.font.Font("freesansbold.ttf",20).render("Done!! used {} hints and took {}".format(self.hintCounter,self.timer),True,GREEN)
			textRect = textSurface.get_rect()
			textRect.center  = (340,20)
			self.window.blit(textSurface,textRect)


		textSurface = pygame.font.Font("freesansbold.ttf",20).render("{} - {}".format(difficulty_levels[self.difficulty],self.puzzlenum),True,BLACK)
		self.window.blit(textSurface,(10,10))

		self.drawTimer(self.window)


		pygame.display.update()



########### BUTTON FUNCTIONS ##############
	def button_clear(self,params):
		self.cellChanged = True
		self.hintCounter = 0
		for i in range(9):
			for j in range(9):
				if [j,i] not in self.lockedCells:
					self.grid[i][j] = 0

	def button_solve(self,params):
		for i in range(9):
			for j in range(9):
				if [j,i] not in self.lockedCells:
					if  self.grid[i][j] != self.solvedGrid[i][j]:
						self.grid[i][j] = self.solvedGrid[i][j]
						self.hintCounter += 1

		self.cellChanged = True

	def button_hint(self,params):
		if self.selected and self.selected not in self.lockedCells:
			self.cellChanged = True
			print(self.selected)
			self.grid[self.selected[1]][self.selected[0]] = self.solvedGrid[self.selected[1]][self.selected[0]]
			self.hintCounter += 1

	def button_new(self,params):
		print("button_new")
		self.state = "newgame"

	def button_easy(self,params):
		print("button_easy")
		self.difficulty = 1
		self.loadGame()

	def button_medium(self,params):
		self.difficulty = 2
		self.loadGame()

	def button_hard(self,params):
		self.difficulty = 3
		self.loadGame()

	def button_evil(self,params):
		self.difficulty = 4
		self.loadGame()


########### HELPER FUNCTIONS ###############
	def mouseOnGrid(self):
		if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
			return None
		if self.mousePos[0] > gridPos[0]+gridSize or self.mousePos[1] > gridPos[1]+gridSize:
			return None
		return [(self.mousePos[0]-gridPos[0])//cellSize,(self.mousePos[1]-gridPos[1])//cellSize]


	def drawSelection(self,window,pos,color=LIGHTBLUE):
		pygame.draw.rect(window,color,((pos[0]*cellSize)+gridPos[0],(pos[1]*cellSize)+gridPos[1],cellSize,cellSize))


	def drawGrid(self,window):
		pygame.draw.rect(window, BLACK, (gridPos[0],gridPos[1],WIDTH-150,HEIGHT-150),2)
		for x in range(9):
			pygame.draw.line(window,BLACK,(gridPos[0]+(x*cellSize),gridPos[1]),(gridPos[0]+(x*cellSize),gridPos[1]+450),2 if x % 3 == 0 else 1)
			pygame.draw.line(window,BLACK,(gridPos[0],gridPos[1]+(x*cellSize)),(gridPos[0]+450,gridPos[1]+(x*cellSize)),2 if x % 3 == 0 else 1)


	def loadGame(self):
		self.lockedCells.clear()
		self.grid = self.getPuzzle(self.difficulty)
		print(self.grid)
		self.hintCounter = 0
		self.puzzleComplete = False
		for idx,row in enumerate(self.grid):
			self.solvedGrid[idx]= row.copy()
		self.solve()

		for yidx,row in enumerate(self.grid):
			for xidx,num in enumerate(row):
				if num != 0:
					self.lockedCells.append([xidx,yidx])
		self.state = "playing"

		self.init_timer = pygame.time.get_ticks()
		#print (self.lockedCells)

	def loadButtons(self):
		self.playingButtons.append(Button(20,40,100,40,text="Clear",color=LIGHTBLUE,highlightcolor=NEONPINK,function=self.button_clear))
		self.playingButtons.append(Button(480,560,100,40,text="Give Up",color=RED,highlightcolor=NEONPINK,function=self.button_solve))
		self.playingButtons.append(Button(140,40,100,40,text="Hint",color=CYAN,highlightcolor=NEONPINK,function=self.button_hint))
		self.playingButtons.append(Button(480,40,120,40,text="New Game",color=GREEN,highlightcolor=NEONPINK,function=self.button_new))

		self.newgameButtons.append(Button(20,40,100,40,text="(1) Easy",color=GREEN,highlightcolor=NEONPINK,function=self.button_easy))
		self.newgameButtons.append(Button(20,90,120,40,text="(2) Medium",color=LIGHTBLUE,highlightcolor=NEONPINK,function=self.button_medium))
		self.newgameButtons.append(Button(20,140,100,40,text="(3) Hard",color=ORANGE,highlightcolor=NEONPINK,function=self.button_hard))
		self.newgameButtons.append(Button(20,190,100,40,text="(4) Evil",color=RED,highlightcolor=NEONPINK,function=self.button_evil))


	def drawNumbers(self,window):
		for yidx,row in  enumerate(self.grid):
			for xidx, num in enumerate(row):
				if num != 0:
					pos = [xidx*cellSize+gridPos[0],yidx*cellSize+gridPos[1]]
					if [xidx,yidx] in self.lockedCells:
						self.textToScreen(window,str(num),pos)
					elif [xidx,yidx] in self.incorrectCells:
						self.textToScreen(window,str(num),pos,color=RED)

					elif self.puzzleComplete:
						self.textToScreen(window,str(num),pos,color=GREEN)

					else:
						self.textToScreen(window,str(num),pos,color=DARKBLUE)


	def drawTimer(self,window):
		if not self.puzzleComplete:
			cur_timer = pygame.time.get_ticks()
			#if (cur_timer % 400) == 0:
			elapsed = (cur_timer - self.init_timer) / 1000
			hours = elapsed // 3600
			mins = elapsed // 60
			secs = elapsed % 60

			timer = "{:0>2}:{:0>2}:{:0>2}".format(int(hours),int(mins),int(secs))
			if timer != self.timer:
				#print(timer)
				self.timer = timer
			
		textSurface = pygame.font.Font("freesansbold.ttf",20).render(self.timer,True,BLACK)
		window.blit(textSurface,(280,570))
			


	def textToScreen(self,window,text,pos,color=BLACK):
		font = self.font.render(text,False,color)
		fontWidth = font.get_width()
		fontHeight = font.get_height()
		pos[0] += (cellSize - fontWidth)//2
		pos[1] += (cellSize - fontHeight)//2

		window.blit(font,pos)

	def isInt(self,string):
		try:
			 (int(string))
		except:
			return False
		return True

#difficulty is passed in as a string with 1 digit.  1-4
	def getPuzzle(self,difficulty,puzzlenum=-1):
		if puzzlenum == -1:
			puzzlenum = random.randrange(100)
		self.puzzlenum = puzzlenum
		print("puzzle: " + str(self.puzzlenum))
		return pickle.load(open('puzzles\\{}-{}.pz'.format(difficulty,puzzlenum),'rb'))


####### BOARD CHECKING FUNCTIONS #############
	def unfinishedCells(self,grid):
		for yidx,row in enumerate(grid):
			for xidx,num in enumerate(row):
				if num == 0:
					return [xidx,yidx]
		return [-1,-1]

	def checkAllCells(self):
		for i in range(9):
			for j in range(9):
				if self.grid[i][j]  != self.solvedGrid[i][j]:
					self.incorrectCells.append([j,i])


############# SOLVING FUNCTIONS #################



	def solve(self):
		next_cell = self.unfinishedCells(self.solvedGrid)
		if next_cell[0] == -1: #all done!
			return True

		for num in range(1,10):
			if(check_location_is_safe(self.solvedGrid,next_cell[1],next_cell[0],num)):
				self.solvedGrid[next_cell[1]][next_cell[0]] = num

				if self.solve():
					return True

				self.solvedGrid[next_cell[1]][next_cell[0]] = 0
		return False
