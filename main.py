# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN
# Authors: Theo,Kane
# ####################################################

#import utils  
# Tetris is function is only used to call on the class so object orientated programming can be used
import numpy as np

def Tetris(target):
    
    solution = Solver(target) 
    M = solution.M
    return M

class Solver:
    def __init__(self, T):
        self.T = T 
        self.T_c = T #T refrenced in the scan        
        self.row = len(self.T_c)  #number of rows
        self.column = len(self.T_c[0])  #number of columns 
        self.M = np.zeros([self.row, self.column], dtype=np.int).tolist() #Create copy of T to append shape id and piece id faster than deepcopy
        self.r = 0 #globally represents the row position in class
        self.c = 0 #globally represents the column position in class
        self.shape_id = 0                   
        self.piece_id = 0                   
        self.coord = [0,0,0,0] #coordinates used for appending shape
        self.n = 1 #value the scan is searching for to find empty
        self.e = 1 #last value of the tree checking empty
        print("Initialising tetromino solver")
        self.scan() #call the scan funtion first
        self.force() #once the scan is complete call the force  not nessecary to turn of for 
                     #high densities and increaces time by only 10%   
           
    def scan(self):
        """
        -------------------------- Stage 1 (iterative scan of matrix) -----------------------------
        - Matrix is searched through rows then collums to find the first empty space (or 1) 
        - If empty (0,0) is inserted at r,c and the it moves right and repeats
        - Because class variables r,c are updated the problem can recurse without calling 
          itslef and reaching recusrion limit 1000
        - If a 1 is found the choose shape function is called to see if shape can be placed
        """
        for self.r in range(self.row):
            for self.c in range(self.column): 
                if self.T_c[self.r][self.c] == 0:
                    self.M[self.r][self.c] = (0,0)                         
                if self.T_c[self.r][self.c] == self.n:
                    self.choose_shape(self,self.r,self.c) 
                        
    def choose_shape (self,T_c,r,c):
        """
        --- Stage 2 (Depth first greedy search (inorder traverasal) of accuracy/speed based tree) --------
        - Tree walks from orgin block finding available shape
        - Maximum 7 decisions before choosing to place a piece by calling
          piece place or make piece invalid by calling place empty 
        - The maximum number of pieces are elimanted from the search each for each level
          however logical order prioritses the accuracy based on logic below. This means the
          trees speed is optimised
        - Check index function called ensuring doesn't search outside target
          throwig an index error
        - Tree order optimsed for accuracy based on rank method increasing accuracy 5-10%
          but speed -20%
        - 
          [ -, -, x, 4, 4] - x in grid represents origin or first block found
          [ 2, 2, 2, 2, 2] - score is the sum of all the blocks which make up shape 
          [ 1, 1, 1, 1, 1] - Rank can be seen by reading down shape Id's on tree
          
         - A neighbours approach was also attempted but increaces time complexity by 4N^2
           as searching the the grid twice and for 4 different decisons.Re-order tree made 
           same accuracy difference without changing time complexity
        """        
        self.coord[0] = (r,c)
        if self.check_index(r,c+1) == self.n: #D.0. right
            self.coord[1] = (r,c+1) #insert to coords
            if self.check_index(r,c+2) == self.n: #D.0.0. 2 right
                self.coord[2] = (r,c+2)
                if self.check_index(r+1,c) == self.e: #D.0.0.0 down
                    self.coord[3] = (r+1,c) 
                    self.shape_id = 7
                    return self.place_piece()
                if self.check_index(r+1,c+1) == self.e: #D.0.0.1 down and right
                    self.coord[3] = (r+1,c+1)
                    self.shape_id = 15
                    return self.place_piece()
                if self.check_index(r+1,c+2) == self.e: #D.0.0.2 down and 2 right
                    self.coord[3] = (r+1,c+2)
                    self.shape_id = 9
                    return self.place_piece()
               
            if self.check_index(r+1,c) == self.n and self.check_index(r+1,c-1) == self.e:#D.0.1.0 down / down and left
                self.coord[2] = (r+1,c)
                self.coord[3] = (r+1,c-1)
                self.shape_id = 16
                return self.place_piece()
            if self.check_index(r+1,c+1) == self.n and self.check_index(r+1,c+2) == self.e:#D.0.1.1 down and right / down and 2 right
                self.coord[2] = (r+1,c+1)
                self.coord[3] = (r+1,c+2)
                self.shape_id = 18
                return self.place_piece() 
            if self.check_index(r+1,c) == self.n and self.check_index(r+2,c) == self.e:#D.0.1.2. down / 2 down
                self.coord[2] = (r+1,c)
                self.coord[3] = (r+2,c)
                self.shape_id = 10
                return self.place_piece()
            if self.check_index(r+1,c+1) == self.n and self.check_index(r+2,c+1) == self.e:#D.0.1.3 down and right / 2 down and right
                self.coord[2] = (r+1,c+1)
                self.coord[3] = (r+2,c+1)
                self.shape_id = 6
                return self.place_piece() 
          
        if self.check_index(r+1,c) == self.n:#D.1 down
            self.coord[1] = (r+1,c)
            if self.check_index(r+1,c-1) == self.n: #D.1.1 down and left
                self.coord[2] = (r+1,c-1)
                if self.check_index(r+1,c-2) == self.e: #D.1.1.0 down and 2 left
                    self.coord[3] = (r+1,c-2)
                    self.shape_id = 5
                    return self.place_piece()
                if self.check_index(r+1,c+1) == self.e: #D.1.1.1 down and right
                    self.coord[3] = (r+1,c+1)
                    self.shape_id = 13
                    return self.place_piece()
               
            if self.check_index(r+1,c+1) == self.n and  self.check_index(r+1,c+2) == self.e: #D.1.2 down and right / down 2 right
                self.coord[2] = (r+1,c+1)
                self.coord[3] = (r+1,c+2)
                self.shape_id = 11
                return self.place_piece()
            if self.check_index(r+1,c-1) == self.n and  self.check_index(r+2,c-1) == self.e: #D.1.3 down and left / 2 down and left
                self.coord[2] = (r+1,c-1)
                self.coord[3] = (r+2,c-1)
                self.shape_id = 19
                return self.place_piece()
            if self.check_index(r+1,c-1) == self.n and  self.check_index(r+2,c) == self.e: #D.1.4 2 down and left /2 down 
                self.coord[2] = (r+1,c-1)
                self.coord[3] = (r+2,c)
                self.shape_id = 14
                return self.place_piece()
            if self.check_index(r+2,c) == self.n and  self.check_index(r+1,c+1) == self.e:#D.1.5 2 down /down and right
                self.coord[2] = (r+2,c)
                self.coord[3] = (r+1,c+1)
                self.shape_id = 12
                return self.place_piece()
            if self.check_index(r+1,c+1) == self.n and  self.check_index(r+2,c+1) == self.e:#D.1.6 down and right /  2 down and right
                self.coord[2] = (r+1,c+1)
                self.coord[3] = (r+2,c+1)
                self.shape_id = 17
                return self.place_piece()
            if self.check_index(r+2,c) == self.n:#D.1.7. 2 down
                self.coord[2] = (r+2,c)
                if self.check_index(r+2,c-1) == self.e:#D.1.7.0 2 down and left
                    self.coord[3] = (r+2,c-1)
                    self.shape_id = 8
                    return self.place_piece()
                if self.check_index(r+2,c+1) == self.e:#D.1.7.1 2 down and right
                    self.coord[3] = (r+2,c+1)
                    self.shape_id = 4
                    return self.place_piece()
                else:
                    return self.place_empty(r,c)                            
            else:
                return self.place_empty(r,c)
        else:
            return self.place_empty(r,c)
        
    def check_index(self,r,c):
        """
        ------------------------- Sub Method -----------------------------------
        - Stops search from going outside target & returns refrence 
        """
        if (r == self.row) or (c == self.column) or (c == -1):
            False
        else:
            return self.T_c[r][c]
    
    def place_piece(self):
        """
        ---------------- Stage 4 (place piece using stored coords) -------------
        - Although longer in length decided to store coords as tree traversed 
          meaning placing piece done with O(1) time complexity
        - Where shape placed 2 insered target to stop overlaping
        """
        self.piece_id += 1
        self.T_c[self.coord[0][0]][self.coord[0][1]] =  2 
        self.T_c[self.coord[1][0]][self.coord[1][1]] =  2
        self.T_c[self.coord[2][0]][self.coord[2][1]] =  2
        self.T_c[self.coord[3][0]][self.coord[3][1]] =  2
        
        self.M[self.coord[0][0]][self.coord[0][1]]   =  (self.shape_id,self.piece_id) 
        self.M[self.coord[1][0]][self.coord[1][1]]   =  (self.shape_id,self.piece_id) 
        self.M[self.coord[2][0]][self.coord[2][1]]   =  (self.shape_id,self.piece_id) 
        self.M[self.coord[3][0]][self.coord[3][1]]   =  (self.shape_id,self.piece_id)

    def place_empty(self,r,c):
        """
        -------------------- Stage 4 (place empty if not found) -----------------
        - if tree traversed shape not found 3 inserted to origin block
          allows forcing function to look for 3 sets of 3 
        """
        self.T_c[r][c] = 3
        self.M[r][c] = (0,0)
    
    def force(self):
        """
        ------------------ Stage 5 (forcing pieces to increase accuracy) -----------
        - After first scan to find available pieces the class variables switched 
        - Now 3 is searched for and last 0 to ensure no overlap. 
        """
        self.n = 3 
        self.e = 0
        return self.scan()

    def show(self,matrix): # used for troubleshooting
        for i in matrix:
            print(i)
