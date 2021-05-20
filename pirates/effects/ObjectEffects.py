from panda3d.core import ColorBlendAttrib, Light
# File: O (Python 2.4)


def Defaults(objectNode):
    objectNode.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
    objectNode.setColorScale(1.0, 1.0, 1.0, 1.0)
    objectNode.setTransparency(0, 1)
    objectNode.setDepthWrite(1)
    objectNode.clearLight()


def Ghost_Effect(objectNode):
    objectNode.setTransparency(1, 1)
    objectNode.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
    objectNode.setColorScale(0.299, 0.598, 0.100, 0.598)
    objectNode.setDepthWrite(0)
    objectNode.setLightOff()
    objectNode.setFogOff()

OBJECT_EFFECTS = {
    'None': Defaults,
    'Ghost': Ghost_Effect }
