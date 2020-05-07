class Square():

    def __init__(self, ispath,board,x,y):
        self.ispath=None
        self.boardWidth=20
        self.x=x
        self.y=y
        self.board=board
        self.enemy=None
        self.tower=None
        if ispath==True:
            self.ispath=True
        else:
            self.ispath=False

    def get_tower(self):
        return self.tower

    def get_enemy(self):
        if self.ispath==True:
            return self.enemy

    def is_path(self):
        return self.ispath

    def set_tower(self, tower):
        self.tower=tower

    def set_enemy(self, enemy):
        if self.enemy==None:
            self.enemy=enemy
            return True
        else:
            return False

    def remove_tower(self):
        removed_tower=self.get_tower()
        self.tower==None
        return removed_tower

    def get_neighboring(self):
        neighboringPaths = []
        for x in [self.x-1,self.x,self.x+1]:
            for y in [self.y-1,self.y,self.y+1]:
                if x in list(range(0,self.boardWidth)) and y in list(range(0,self.boardWidth)) and (x,y)!=(self.x,self.y):
                    square=self.board.get_square([x,y])
                    if square!=False:
                        if square.ispath:
                            neighboringPaths.append([square.x,square.y])
        return neighboringPaths
