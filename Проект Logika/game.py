from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from panda3d.core import *
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        self.land.loadLand("My_land2.txt")
        self.hero = Hero((10, 10, 2), self.land)
        base.camLens.setFov(90)
        self.btype = 1

        base.accept("f1", self.land.planeLand)
        base.accept("f5", self.land.saveMap, ["my_map.dat"])
        base.accept("f6", self.land.loadMap, ["my_map.dat"])

game = Game()
game.run()
