from panda3d.core import TextNode, Vec4
from direct.showbase.PythonUtil import lerp
from pirates.piratesbase.PythonUtil import clampScalar
from direct.gui.DirectGui import DGG, DirectFrame, DirectLabel, DirectSlider, DirectEntry, DirectButton
from direct.gui.OnscreenText import OnscreenText
import sys

class RangeSlider(DirectFrame):

    def __init__(self, label = '', range = (0, 1), command = None, value = 0.0, orientation = DGG.HORIZONTAL, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.initialiseoptions(self.__class__)
        self.setup(label, range, value, orientation, *args, **kwargs)
        self['command'] = command


    def __setitem__(self, key, value):
        if key == 'command':

            def finalCommand():
                val = self.slider['value']
                self.slider['text'] = '%1.3f' % val
                if value:
                    value(val)


            self.slider['command'] = finalCommand
        elif key == 'value':
            self.slider['value'] = value
        elif key == 'range':
            self.slider['range'] = value
        else:
            super(self.__class__, self).__setitem__(key, value)


    def __getitem__(self, key):
        if key == 'command':
            return self.slider['command']
        elif key == 'value':
            return self.slider['value']
        elif key == 'range':
            return self.slider['range']
        else:
            return super(self.__class__, self).__getitem__(key)


    def setup(self, label, range, value, orientation, *args, **kwargs):

        def updateField(widget, field, value):
            widget[field] = value


        def finalCommand():
            val = self.slider['value']
            updateField(self.slider, 'text', '%1.3f' % val)

        self.slider = DirectSlider(parent = self, relief = DGG.FLAT, range = range, value = value, orientation = orientation, scale = 0.25, thumb_relief = DGG.FLAT, thumb_color = (0, 1, 1, 1), pos = (0, 0, 0), text = '0.0', text_scale = 0.200, text_pos = (0, 0.100, 0))
        updateField(self.slider, 'command', finalCommand)
        width = 3
        if orientation == DGG.HORIZONTAL:
            pos = (-0.275 - width * 0.050000, 0, -0.02)
        else:
            pos = (-0.0250 * width, 0, -0.348)
        self.min = DirectEntry(parent = self, initialText = `float(self.slider['range'][0])`, scale = 0.050000, width = width, pos = pos)
        updateField(self.min, 'command', lambda x: updateField(self.slider, 'range', (float(x), self.slider['range'][1])))
        if orientation == DGG.HORIZONTAL:
            pos = (0.275, 0, -0.02)
        else:
            pos = (-0.0250 * width, 0, 0.299)
        self.max = DirectEntry(parent = self, initialText = `float(self.slider['range'][1])`, scale = 0.050000, width = width, pos = pos)
        updateField(self.max, 'command', lambda x: updateField(self.slider, 'range', (self.slider['range'][0], float(x))))
        self.label = DirectLabel(parent = self, relief = None, text = label, text_scale = 0.050000, text_pos = (0.0299 - 0.395, 0.348 - 0.239, 0), text_align = TextNode.ALeft)



class MapConfig(DirectFrame):

    def __init__(self, *args, **kwargs):
        kwargs['suppressMouse'] = 0
        super(self.__class__, self).__init__(*args, **kwargs)
        self.initialiseoptions(self.__class__)
        self.setTransparency(1)
        self.setup()


    def setup(self):
        if hasattr(self, 'mainFrame'):
            self.mainFrame.destroy()

        self.mainFrame = DirectFrame(parent = self, relief = None)

        def setVisibility():
            value = self.visSlider['value']
            self.setColorScale(Vec4(1, 1, 1, value))

        self.visSlider = DirectSlider(guiId = 'visSlider', parent = self.mainFrame, scale = 0.4, thumb_relief = DGG.FLAT, thumb_color = (0.25, 1.0, 0.25, 1), pos = (0.4, 0, -0.848), text = 'Visibility', text_scale = 0.200, text_pos = (0, 0.100, 0), text_bg = (0.800000, 0.800000, 0.800000, 1), value = 1.0, command = setVisibility)
        self.visSlider.getChild(0).setTransparency(0)
        self.camFrame = DirectFrame(guiId = 'camFrame', parent = self.mainFrame, relief = DGG.RIDGE, frameSize = (0.0, 0.800000, 0.0, 0.320), frameColor = (1, 1, 0.75, 1), borderWidth = (0.00500, 0.00500), pos = (0, 0, 0.598), text = 'Camera', text_fg = (0, 0, 0, 1), text_scale = 0.050000, text_pos = (0.100, 0.260, 0))
        self.camSlider = RangeSlider(guiId = 'zoom', label = 'Zoom (Y-axis)', range = (-0.75, 0.25), value = 0, parent = self.camFrame, pos = (0.395, 0, 0.070))
        self.worldFrame = DirectFrame(guiId = 'worldFrame', parent = self.mainFrame, relief = DGG.RIDGE, frameSize = (0.0, 0.800000, -0.550000, 0.5), frameColor = (1, 0.75, 0.75, 1), borderWidth = (0.00500, 0.00500), pos = (0.0, 0, 0), text = 'World', text_fg = (0, 0, 0, 1), text_scale = 0.050000, text_pos = (0.100, 0.429, 0))
        self.worldPSlider = RangeSlider(guiId = 'worldP', label = 'World P', range = (-90, 0), value = 0.0, parent = self.worldFrame, pos = (0.395, 0, 0.239))
        self.worldDecorScaleSlider = RangeSlider(guiId = 'worldP', label = 'World Decor Scale', range = (0.200, 0.299), value = 0.25, parent = self.worldFrame, pos = (0.395, 0, 0.0))
        self.finalSlider = RangeSlider(guiId = 'final', label = 'Final', range = (0, 1), value = 0, parent = self.worldFrame, pos = (0.395, 0, -0.478))
        self.saveState0Button = DirectButton(guiId = 'save0Button', parent = self.mainFrame, scale = 0.100, pos = (0.200, 0, -0.65), borderWidth = (0.100, 0.100), text = 'save pt0')
        self.saveState1Button = DirectButton(guiId = 'save1Button', parent = self.mainFrame, scale = 0.100, pos = (0.598, 0, -0.65), borderWidth = (0.100, 0.100), text = 'save pt1')
