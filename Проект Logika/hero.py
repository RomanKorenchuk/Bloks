from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from panda3d.core import *

class Hero():
    def __init__(self, pos, land):
        self.land  = land
        self.pos = pos
        self.mode = True
        self.hero = loader.loadModel("smiley")
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
        self.btype = 1
        self.text_change(type)
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)
    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)

        return from_x + dx, from_y + dy, from_z       
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle) 
    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)
    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)
    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH() + 90 ) % 360
        self.move_to(angle)
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)
    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)
    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)
    def changeMode(self):
       if self.mode:
           self.mode = False
       else:
           self.mode = True 
    def try_move(self, angle):
       pos = self.look_at(angle)
       if self.land.isEmpty(pos):
           pos = self.land.findHighestEmpty(pos)
           self.hero.setPos(pos)
       else:
           pos = pos[0], pos[1], pos[2] + 1
           if self.land.isEmpty(pos):
               self.hero.setPos(pos)
    def setBuild(self, type):
        self.btype = type
        self.text_change(type)
    def build(self):
       angle = self.hero.getH() % 360
       pos = self.look_at(angle)
       if self.mode:
           self.land.addBlock(pos, type = self.btype)
       else:
           self.land.buildBlock(pos, type = self.btype)
    def destroy(self):
       angle = self.hero.getH() % 360
       pos = self.look_at(angle)
       if self.mode:
           self.land.delBlock(pos)
       else:
           self.land.delBlockFrom(pos)
    def text_change(self, btype):
        fg1 = (0, 0, 0, 1)
        fg = (1, 0, 0, 1)

        self.label1 = DirectLabel(text = "1", scale = 0.1, pos = Vec3(-0.35, 0, -0.99), text_fg = fg)
        self.label2 = DirectLabel(text = "3", scale = 0.1, pos = Vec3(0, 0, -0.99), text_fg = fg1)
        self.label3 = DirectLabel(text = "5", scale = 0.1, pos = Vec3(0.35, 0, -0.99), text_fg = fg1)
        self.label4 = DirectLabel(text = "2", scale = 0.1, pos = Vec3(-0.175, 0, -0.99), text_fg = fg1)
        self.label5 = DirectLabel(text = "4", scale = 0.1, pos = Vec3(0.175, 0, -0.99), text_fg = fg1)

        if btype == 1:
            self.label1["text_fg"] = fg
            self.label2["text_fg"] = fg1
            self.label3["text_fg"] = fg1
            self.label4["text_fg"] = fg1
            self.label5["text_fg"] = fg1
        elif btype == 2:
            self.label1["text_fg"] = fg1
            self.label2["text_fg"] = fg
            self.label3["text_fg"] = fg1
            self.label4["text_fg"] = fg1
            self.label5["text_fg"] = fg1
        elif btype == 3:
            self.label1["text_fg"] = fg1
            self.label2["text_fg"] = fg1
            self.label3["text_fg"] = fg
            self.label4["text_fg"] = fg1
            self.label5["text_fg"] = fg1
        elif btype == 4:
            self.label1["text_fg"] = fg1
            self.label2["text_fg"] = fg1
            self.label3["text_fg"] = fg1
            self.label4["text_fg"] = fg
            self.label5["text_fg"] = fg1
        elif btype == 5:
            self.label1["text_fg"] = fg1
            self.label2["text_fg"] = fg1
            self.label3["text_fg"] = fg1
            self.label4["text_fg"] = fg1
            self.label5["text_fg"] = fg

        OnscreenImage("block2.png", pos = Vec3(-0.35, 0, -0.85), scale = Vec3(0.05, 0, 0.05))
        OnscreenImage("block5.png", pos = Vec3(-0.175, 0, -0.85), scale = Vec3(0.05, 0, 0.05))
        OnscreenImage("block3.png", pos = Vec3(0, 0, -0.85), scale = Vec3(0.05, 0, 0.05))
        OnscreenImage("block6.png", pos = Vec3(0.175, 0, -0.85), scale = Vec3(0.05, 0, 0.05))
        OnscreenImage("block4.png", pos = Vec3(0.35, 0, -0.85), scale = Vec3(0.05, 0, 0.05))

    def accept_events(self):
        base.accept("c", self.changeView)
        base.accept("q", self.turn_left)
        base.accept("q" + "-repeat", self.turn_left)
        base.accept("e", self.turn_right)
        base.accept("e" + "-repeat", self.turn_right)
        base.accept("w", self.forward)
        base.accept("w" + '-repeat', self.forward)
        base.accept("s", self.back)
        base.accept("s" + '-repeat', self.back)
        base.accept("a", self.left)
        base.accept("a" + '-repeat', self.left)
        base.accept("d", self.right)
        base.accept("d" + '-repeat', self.right)
        base.accept("space", self.up)
        base.accept("space" + '-repeat', self.up)
        base.accept("shift", self.down)
        base.accept("shift" + '-repeat', self.down)
        base.accept("c", self.changeView)
        base.accept("v", self.changeMode)
        base.accept("r", self.build)
        base.accept("1", self.setBuild, [1])
        base.accept("2", self.setBuild, [4])
        base.accept("3", self.setBuild, [2])
        base.accept("4", self.setBuild, [5])
        base.accept("5", self.setBuild, [3])
        base.accept("f", self.destroy)
        '''base.accept("f5", self.land.saveMap)
        base.accept("f6", self.land.loadMap)'''

    

