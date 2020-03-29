class Square():

    def __init__(self, ispath,board,x,y):
        self.ispath=None
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
        if self.ispath==False:
            return self.tower

    def get_enemy(self):
        if self.ispath==True:
            return self.enemy

    def is_path(self):
        return self.ispath

    def set_tower(self, tower):
        if self.tower==None:
            self.tower==tower
            return True
        else:
            return False

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

    def remove_enemy(self):
        removed_enemy=self.get_enemy()
        self.enemy==None
        return removed_enemy