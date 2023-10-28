import random
import numpy as np
import time
import pygame

class World:
    def __init__(self, random_x_range, random_y_range, cell_size):
        self.alive_cells = []
        self.num_start_alive = 6
        self.visual_x_size = random_x_range
        self.visual_y_size = random_y_range
        self.all_dead_neighbours = []
        self.cell_size = cell_size
        
    def kill_all_cells(self):
        self.alive_cells = []

    def create_random_cells(self, start_num_alive):   
        pos = []          
        while len(self.alive_cells) < start_num_alive: #creates exactly number of start_num_alive, all different
            x = (random.randint(0, self.visual_x_size) // self.cell_size) #* self.cell_size
            y = (random.randint(0, self.visual_y_size)  // self.cell_size)# * self.cell_size
            if [x,y] not in pos:
                
                cell = Cell(x, y)
                self.alive_cells.append(cell)     
                pos.append([x,y])   

        return pos
    
    def create_pattern(self, pattern_list):
        for elemnt in pattern_list:
            cel = Cell(elemnt[0], elemnt[1])
            self.alive_cells.append(cel)  
              

    def count_neighbours(self):
        self.all_dead_neighbours = [] #is used to check if dead cells turn alive

        for cell in self.alive_cells:
            pos_neigh = [] # in this list are all positions around the cell
            pos_corner = [cell.x-1, cell.y-1]
            
            for y in range(3):
                for x in range(3):
                    if pos_corner != [cell.x, cell.y]:
                        pos_neigh.append(pos_corner.copy())
                    pos_corner[0] += 1
                pos_corner[0] -= 3
                pos_corner[1] += 1

            num_neighbours = 0
            dead_neighbours = pos_neigh #all elemnts of dead neighbours are appended to the self.all_dead_neighbours
            for possible_neig in self.alive_cells:
                if [possible_neig.x, possible_neig.y] in pos_neigh:
                    dead_neighbours.remove([possible_neig.x, possible_neig.y])
                    num_neighbours += 1
                cell.num_alive_neighbours = num_neighbours
            self.all_dead_neighbours.extend(dead_neighbours) # here the dead neighbours from every cell are appended to self.all_dead_neighbours

    def die_over_under_pop(self):
        copy_of_alive_cells = self.alive_cells.copy()
        for cell in copy_of_alive_cells: #this checks the number of neighbours of every alive cell
            if cell.num_alive_neighbours < 2:
                self.alive_cells.remove(cell)
            elif cell.num_alive_neighbours > 3:
                self.alive_cells.remove(cell)

    def birth_new_cells(self):
        all_new_cells = []
        while len(self.all_dead_neighbours) > 3:
            realiven_cell = self.all_dead_neighbours[0]
            count = self.all_dead_neighbours.count(realiven_cell)
            if count == 3: # if a dead cell appears exactly three times in the list that means it has three alive neighbours since three alive cells have the same dead neighbour 
                new_cell = Cell(realiven_cell[0], realiven_cell[1])
                all_new_cells.append(new_cell)
            while realiven_cell in self.all_dead_neighbours: # this removes the dead cells that have been checked from the self.all_dead_neighbours list
                self.all_dead_neighbours.remove(realiven_cell)

        self.all_dead_neighbours = []
        return all_new_cells # can't be directly appended to self.alive_cells otherwise they could already die before being displayed

    def update(self):      
        self.count_neighbours()
        new_cells = self.birth_new_cells() # needs to be done before die_over_under_pop() otherwise some cells would already be dead
        self.die_over_under_pop()
        self.alive_cells.extend(new_cells) # new born cells are appended after all the living cells are checked

        positions_cell = []
        for cell in self.alive_cells:
            positions_cell.append([cell.x, cell.y])
        return positions_cell # this list contains all the coordinates of all alive cells, will be displayed in an array

class Cell:
    def __init__(self, x, y):
        self.x = x  
        self.y = y  
        self.num_alive_neighbours = 0

pattern_list = [[[11, 10], [11, 9], [12, 9], [13, 9], [13, 10], [13, 11], [11, 11], [11, 14], [11, 13], [13, 13], [13, 14], [13, 15], [12, 15], [11, 15], [23, 32]], [[3, 4], [4, 4], [4, 3], [3, 3], [7, 9], [6, 10], [6, 11], [7, 12], [8, 11], [8, 10], [15, 5], [16, 6], [17, 4], [16, 4], [17, 5], [15, 21], [15, 23], [14, 22], [16, 22], [25, 18], [26, 19], [26, 17], [27, 16], [28, 17], [27, 18], [29, 7], [29, 6], [30, 6], [31, 7], [31, 8], [31, 9], [32, 9], [15, 14], [16, 13], [17, 12], [16, 15], [17, 15], [18, 13], [18, 14], [17, 32]], [[4, 2], [4, 4], [3, 3], [5, 3], [4, 3], [14, 2], [14, 3], [14, 4], [13, 3], [15, 3], [23, 3], [24, 2], [24, 3], [24, 4], [25, 3], [33, 3], [34, 3], [34, 2], [35, 3], [34, 4], [9, 9], [9, 10], [9, 11], [8, 10], [10, 10], [20, 11], [20, 10], [20, 9], [19, 10], [21, 10], [29, 9], [29, 10], [28, 10], [29, 11], [30, 10], [4, 16], [4, 17], [4, 18], [3, 17], [5, 17], [14, 16], [14, 18], [15, 17], [14, 17], [13, 17], [24, 16], [24, 17], [23, 17], [24, 18], [25, 17], [34, 16], [34, 18], [35, 17], [34, 17], [33, 17], [9, 23], [9, 24], [9, 25], [8, 24], [10, 24], [20, 23], [20, 24], [20, 25], [21, 24], [19, 24], [29, 23], [29, 24], [29, 25], [28, 24], [30, 24], [22, 32]], [[2, 3], [4, 3], [3, 3], [8, 12], [9, 11], [9, 10], [10, 12], [10, 13], [11, 11], [16, 5], [16, 4], [16, 3], [17, 4], [17, 5], [17, 6], [3, 21], [3, 20], [4, 20], [4, 21], [6, 23], [5, 23], [6, 22], [5, 22], [26, 2], [27, 2], [28, 2], [28, 3], [28, 4], [26, 3], [26, 4], [27, 4], [29, 2], [29, 3], [29, 4], [30, 4], [31, 4], [32, 4], [32, 3], [32, 2], [30, 2], [31, 2], [30, 3], [27, 21], [27, 22], [27, 23], [28, 24], [29, 24], [30, 24], [31, 24], [28, 21], [28, 22], [27, 20], [29, 23], [30, 23], [28, 19], [29, 19], [30, 19], [30, 20], [29, 20], [31, 19], [32, 20], [31, 21], [32, 21], [31, 22], [32, 22], [32, 23], [22, 32], [12, 20], [12, 21], [13, 21], [13, 22], [13, 23], [15, 21], [15, 22], [15, 23], [16, 21], [16, 20], [12, 24], [12, 25], [11, 24], [11, 23], [16, 24], [16, 25], [17, 24], [17, 23], [18, 11], [18, 12], [19, 11], [20, 12], [20, 14], [21, 15], [22, 15], [22, 14], [17, 32]], [[1, 17], [1, 15], [2, 14], [4, 17], [5, 16], [5, 15], [5, 14], [4, 14], [3, 14], [8, 15], [8, 17], [9, 14], [10, 18], [12, 17], [13, 16], [13, 15], [13, 14], [10, 14], [11, 14], [12, 14], [16, 15], [17, 14], [16, 17], [18, 18], [19, 18], [21, 17], [22, 16], [22, 15], [22, 14], [18, 14], [19, 14], [20, 14], [21, 14], [13, 32]], [[12, 10], [13, 10], [14, 10], [15, 10], [15, 11], [14, 11], [12, 11], [13, 11], [12, 12], [13, 12], [14, 12], [15, 12], [16, 10], [16, 11], [16, 12], [13, 13], [12, 13], [14, 13], [16, 13], [15, 13], [16, 14], [15, 14], [14, 14], [13, 14], [12, 14], [22, 32]], [[13, 13], [14, 12], [14, 11], [14, 10], [12, 13], [11, 13], [13, 15], [12, 15], [11, 15], [14, 16], [14, 17], [14, 18], [16, 16], [16, 18], [16, 17], [18, 15], [17, 15], [19, 15], [16, 12], [16, 11], [16, 10], [17, 13], [18, 13], [19, 13], [13, 20], [12, 20], [11, 20], [9, 16], [9, 18], [9, 17], [17, 20], [19, 20], [18, 20], [21, 16], [21, 17], [21, 18], [9, 12], [9, 10], [9, 11], [11, 8], [12, 8], [13, 8], [17, 8], [18, 8], [19, 8], [21, 12], [21, 11], [21, 10], [16, 32]], [[12, 8], [13, 7], [13, 8], [14, 7], [12, 10], [13, 10], [13, 11], [14, 11], [15, 8], [15, 9], [15, 10], [16, 9], [20, 32]], [[4, 2], [5, 2], [6, 2], [6, 1], [5, 0], [14, 2], [15, 3], [15, 4], [14, 4], [13, 4], [5, 11], [6, 12], [6, 13], [4, 13], [5, 13], [0, 19], [1, 19], [1, 17], [2, 19], [2, 18], [13, 8], [14, 9], [14, 10], [13, 10], [12, 10], [11, 14], [12, 15], [12, 16], [11, 16], [10, 16], [6, 20], [7, 22], [6, 22], [5, 22], [7, 21], [23, 1], [24, 2], [24, 3], [23, 3], [22, 3], [22, 6], [23, 7], [23, 8], [22, 8], [21, 8], [18, 32]]]
