from types import CellType
import pygame
import time
from cell import environment, cell, CELL_SIZE
import math

#Constants
CELL_COLOR1 = (255, 255, 0)
CELL_COLOR2 = (0, 191, 255)
LINE_COLOR = (255, 255, 255)
BOARD_WIDTH = 1500
#Height was set for my 15in MBP
BOARD_HEIGHT = 990
FORMATIONS_FOLDER = 'Formations'

def adjustCellCoordinate(cord):
    return CELL_SIZE * math.floor(cord / CELL_SIZE)

def getCoordinateFromFile(filename, addVerticalShift = 0, addHorizontalShift = 0):
    coords = []
    with open(FORMATIONS_FOLDER + '/' + filename) as f:
        coords = f.readlines()
        f.close()
    formattedCords = []
    for coord in coords:
        temp = coord.rstrip()
        temp = temp.replace('(', '')
        temp = temp.replace(')', '')
        x,y = temp.split(',')
        formattedCords.append((int(x) + addHorizontalShift,int(y) + addVerticalShift))
    return formattedCords

class simulation:
    def __init__(self, initialSetup = None):
        pygame.init()
        #Canvas Dimensions
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        #Canvas Color
        self.color = (0,0,0)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        #Creates display
        self.screen = pygame.display.set_mode((self.width, self.height))
        #Setup Phase
        self.isSetupPhase = True
        #Collection of Cells
        self.environment = environment(self.width, self.height)
        if initialSetup:
            for coord in initialSetup:
                self.environment.setCellAsAlive(coord[1] * CELL_SIZE, coord[0] * CELL_SIZE)
    
    def drawGrid(self):
        horizontalLines = int(BOARD_HEIGHT / CELL_SIZE) 
        for x in range(1, horizontalLines):
            lineY = x * CELL_SIZE
            pygame.draw.line(self.screen, LINE_COLOR, (0, lineY), (BOARD_WIDTH, lineY), 1)
        verticalLines = int(BOARD_WIDTH / CELL_SIZE)
        for y in range(1, verticalLines):
            lineX = y * CELL_SIZE
            pygame.draw.line(self.screen, LINE_COLOR, (lineX, 0), (lineX, BOARD_HEIGHT), 1)
            
    def drawCells(self, cell_color):
        for cell in self.environment.flattenCells():
            if cell.isAlive:
                #Left, Top, Width, Height
                rectangleDimensions = (cell.xCord, cell.yCord, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, cell_color, (rectangleDimensions))
    
    def bigBang(self):
        pygame.display.set_caption('The Game of Life')
        self.screen.fill(self.color)
        pygame.display.flip() 
        running = True
        while running:
            #Reset Screen
            self.screen.fill(self.color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.isSetupPhase:
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        xCord = adjustCellCoordinate(pos[0])
                        yCord = adjustCellCoordinate(pos[1])
                        self.environment.setCellAsAlive(xCord, yCord)
                    
                    if event.type == pygame.KEYDOWN:
                        cells_in_environment = self.environment.flattenCells()
                        if event.key == pygame.K_RETURN:
                            self.isSetupPhase = False
                        elif event.key == pygame.K_LEFT:
                            for i in range(0, len(cells_in_environment)):
                                cells_in_environment[i].xCord -= CELL_SIZE
                        elif event.key == pygame.K_RIGHT:
                            for i in range(0, len(cells_in_environment)):
                                cells_in_environment[i].xCord += CELL_SIZE
                        elif event.key == pygame.K_UP:
                            for i in range(0, len(cells_in_environment)):
                                cells_in_environment[i].yCord -= CELL_SIZE
                        elif event.key == pygame.K_DOWN:
                            for i in range(0, len(cells_in_environment)):
                                cells_in_environment[i].yCord += CELL_SIZE                               
            if self.isSetupPhase:
                self.drawGrid()
                self.drawCells(CELL_COLOR2)
            else:
                self.environment.update()
                self.drawCells(CELL_COLOR1)
            pygame.display.update() 
            #Slow down for visual input
            time.sleep(.05)
            
        pygame.quit()
        
if __name__ == '__main__':
    print('Game of Life')
    initialCoords = None
    loadFormation = input('Would you like to load a formation? (Y/N): ')
    if loadFormation=='Y':
        selection = input('1 for Pulsar, 2 for Spaceship, 3 for Glider Gun: ')
        if selection=='1':
            initialCoords = getCoordinateFromFile('pulsar.txt', 5, 5)
        if selection=='2':
            initialCoords = getCoordinateFromFile('spaceship_1.txt', 0, 0)
        if selection=='3':
            initialCoords = getCoordinateFromFile('glider_gun.txt', 10, 5)
    game = simulation(initialCoords)
    game.bigBang()