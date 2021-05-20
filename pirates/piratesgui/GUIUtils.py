from panda3d.core import CardMaker, LVector4f, NodePath, PNMImage, TextNode, Texture, Xel
import colorsys, random, math

def loadGradientTexture(hue, minSat, maxSat, minVal, maxVal):
    image = PNMImage(int((maxSat - minSat) * 100), int((maxVal - minVal) * 100))
    
    for x in xrange(image.getXSize()):
        for y in xrange(image.getYSize()):
            image.setXel(x, y, colorsys.hsv_to_rgb(hue, (y / 100.0) + minVal, (x / 100.0) + minSat))
    
    texture = Texture()
    texture.load(image)
    
    return texture

def loadGradient(parent, frame, hue, minSat, maxSat, minVal, maxVal):
    model = loadTextureModel(loadGradientTexture(hue, minSat, maxSat, minVal, maxVal), 'gradient', frame)
    model.reparentTo(parent)
    
    return model

def loadTextureModel(texture, name='card', frame=(-1, 1, -1, 1), transparency=False):
    card = CardMaker(name)
    card.setFrame(*frame)
    
    card = NodePath(card.generate())
    card.setTexture(texture, 1)
    
    if transparency:
        card.setTransparency(True)
    
    return card

def getRandomSatVal(startSat, startVal):
    return startSat + random.uniform(min(1.0 - startSat, 0.1), 1.0 - startSat), startVal + random.uniform(min(1.0 - startVal, 0.1), 1.0 - startVal)

def loadRandomGradient(parent, frame, hue, startSat, startVal):
    maxSat, maxVal = getRandomSatVal(startSat, startVal)

    return loadGradient(parent, frame, hue, startSat, maxSat, startVal, maxVal)

def packText(text, name='textRoot', color=LVector4f(1, 1, 1, 1), font=None, scale=1, stumble=0, stomp=0, wiggle=0, kern=0, indent=0, height=0, width=0):
    root = NodePath(name)
    x = 0.0
    
    for index, letter in enumerate(text):
        tn = TextNode('text')
        tn.setText(letter)
        tn.setTextColor(color)
        tn.setShadowColor(0, 0, 0, 1)
        
        if font:
            tn.setFont(font)
        
        np = root.attachNewNode(tn)
        np.setScale(scale)
        np.setDepthWrite(False)
            
        if (index % 2):
            np.setPos(x + stumble, 0, stomp)
            np.setR(-wiggle)     
        else:
            np.setPos(x - stumble, 0, -stomp)
            np.setR(wiggle)
                
        x += tn.getWidth() * np.getSx() + kern
            
    map(lambda c: c.setX(c.getX() - x / 2), root.getChildren())
    
    if (width != 0) and (height != 0):
        for node in root.getChildren():
            theta = (node.getX() / (height / 2.)) + (indent * math.pi / 180)
            d = node.getY()

            x = math.sin(theta) * (width / 2.)
            y = (math.cos(theta) - 1) * (height / 2.)
                
            radius = math.hypot(x, y)
                
            if radius != 0:
                j = (radius + d) / radius
                x *= j
                y *= j
            
            node.setPos(x, 0, y)
            node.setR(node, theta * 180 / math.pi)

    for np in root.findAllMatches('**/+TextNode'):
        np2 = np.getParent().attachNewNode(np.node().generate())
        np2.setTransform(np.getTransform())
        np.removeNode()
            
    root.flattenStrong()
    return root
