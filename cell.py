import math
CELL_SIZE = 15

class environment:
    def __init__(self, screen_width, screen_height):
        self.cells = []
        self.width = math.floor(screen_width / CELL_SIZE)
        self.height = math.floor(screen_height / CELL_SIZE)
        for i in range(0, self.height):
            row = []
            for j in range(0, self.width):
                row.append(cell(j * CELL_SIZE, i * CELL_SIZE))
            self.cells.append(row)
    
    def setCellAsAlive(self, xCord, yCord):
        heightIndex = int(yCord / CELL_SIZE)
        widthIndex = int(xCord / CELL_SIZE)
        self.cells[heightIndex][widthIndex].isAlive = True
    
    def flattenCells(self):
        result = []
        for _list in self.cells:
            result += _list
        return result

    def update(self):
        cellsNeedToUpdate = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                numNeighbors = self.numOfNeighbors(i, j)
                if self.cells[i][j].isAlive:
                    if numNeighbors < 2 or numNeighbors > 3:
                        cellsNeedToUpdate.append((i, j, False))
                else:
                    if numNeighbors==3:
                        cellsNeedToUpdate.append((i, j, True))
        for cell in cellsNeedToUpdate:
            self.cells[cell[0]][cell[1]].isAlive = cell[2]
        
                    
    def numOfNeighbors(self, xIndex, yIndex):
        num0fNeighbors = 0
        if xIndex > 0:
            num0fNeighbors+=self.cells[xIndex - 1][yIndex].isAlive
            if yIndex > 0:
                num0fNeighbors+=self.cells[xIndex - 1][yIndex - 1].isAlive
            if yIndex < self.width - 1:
                num0fNeighbors+=self.cells[xIndex - 1][yIndex + 1].isAlive
        if xIndex < self.height - 1:
            num0fNeighbors+=self.cells[xIndex + 1][yIndex].isAlive
            if yIndex > 0:
                num0fNeighbors+=self.cells[xIndex + 1][yIndex - 1].isAlive
            if yIndex < self.width - 1:
                num0fNeighbors+=self.cells[xIndex + 1][yIndex + 1].isAlive
        if yIndex > 0:
            num0fNeighbors+=self.cells[xIndex][yIndex - 1].isAlive
        if yIndex < self.width - 1:
            num0fNeighbors+=self.cells[xIndex][yIndex + 1].isAlive
        return num0fNeighbors

        
        
            
    def __str__(self) -> str:
        return self.cells

class cell:
    def __init__(self, xCord, yCord):
        self.xCord = xCord
        self.yCord = yCord
        self.isAlive = False
        