import pickle
class Mapmanager():
    def __init__(self):
        self.model = "block"
        self.textures = ["block1.png", "block2.png", "block3.png", "block4.png", "block5.png", "block6.png"]
        self.createSamples(self.model, self.textures)
        self.color = [
            (0.5, 0.5, 0.5, 1),
            (0.3, 0.3, 0.3, 1),
            (0.3, 0.3, 0.3, 1),
            (0.3, 0.3, 0.3, 1),
        ]
        self.startNew()
        self.getColor
    def startNew(self):
        self.land = render.attachNewNode("Land")
    def createSamples(self, model, textures):
        self.samples = list()
        for tname in textures:
            block = loader.loadModel(model)
            block.setTexture(loader.loadTexture(tname))
            self.samples.append(block)
    def getColor(self, z):
        if z < len(self.color):
            return self.color[z]
        else:
            return self.color[-1]
    '''def getTexture(self, z):
        if z < len(self.textures):
            return self.textures[z]
        else:
            return self.textures[-1]'''
    def addBlock(self, position, type=0):
        '''block = loader.loadModel(self.model)
        self.texture1 = self.getTexture(int(position[2]))
        block.setTexture(loader.loadTexture(self.texture1))'''
        if type >= len(self.samples):
            type = 0
        block = self.samples[type].copyTo(self.land)
        block.setPos(position)
        if type == 0:
            color = self.getColor(int(position[2]))
            block.setColor(color)
        block.setTag("type", str(type))
        block.setTag("at", str(position))
        block.reparentTo(self.land)
    def addCol(self, x, y, z):
        for z0 in range(z+1):
            self.block = self.addBlock((x, y, z0))
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
           self.addBlock(new, type)
    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
           block.removeNode()
    def delBlockFrom(self, pos):
        x, y, z = pos
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z - 1
        for self.block in self.findBlocks(pos):
            if int(block.getTag("type")) > 0:
                block.removeNode()
    def clear(self):
        self.land.removeNode()
        self.startNew()
    def getRoot(self):
        return self.land
    def getAll(self):
        return self.land.getChildren()
    def planeLand(self, width=20, length=20):
        self.clear()
        z = 0
        for x in range(width):
            for y in range(length):
                pos = (x, y, z) 
                self.addBlock(pos)
    def loadLand(self, filename):
        self.clear()
        with open(filename) as f:
            y = 0
            for line in f:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
            '''y = 0
            firstline = True
            for s in f:
                if firstline:
                    maxY = int(s)
                    firstline = False
                else:
                    line = map(int, s.split())
                    x = 0
                    for z in line:
                        self.addCol(x, maxY-y, z)
                        x += 1
                    y += 1
        return x, maxY'''
    def saveMap(self, filename):
        blocks = self.getAll()
        fout = open(filename, 'wb')
        pickle.dump(len(blocks), fout)                 
        for block in blocks:
            x, y, z = block.getPos()
            pos = (int(x), int(y), int(z))
            pickle.dump(pos, fout)
            pickle.dump(int(block.getTag("type")), fout)
        fout.close()
    def loadMap(self, filename):
        self.clear()
        fin = open(filename, 'rb')
        lenght = pickle.load(fin)

        for i in range(lenght):
            pos = pickle.load(fin)
            type = pickle.load(fin)
            self.addBlock(pos, type)
        fin.close()

