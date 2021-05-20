from panda3d.core import VBase4
# File: R (Python 2.4)

from direct.gui.DirectButton import *

class RadioButton(DirectButton):

    def __init__(self, parent = None, **kw):
        gui_main = loader.loadModel('models/gui/gui_main')
        icon_sphere = gui_main.find('**/icon_sphere')
        icon_torus = gui_main.find('**/icon_torus')
        icon_torus_over = gui_main.find('**/icon_torus_over')
        gui_main.remove_node()
        optiondefs = (('geom', None, None), ('checkedGeom', icon_sphere, None), ('image', (icon_torus, icon_torus, icon_torus_over, icon_torus), None), ('geom_color', VBase4(1, 1, 1, 1), None), ('image_scale', 1.39, None), ('variable', [], None), ('value', [], None), ('others', [], None), ('relief', None, None), ('isChecked', False, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(RadioButton)
        needToCheck = True
        if len(self['value']) == len(self['variable']):
            pass
        len(self['variable']) != 0
        if 1:
            for i in xrange(len(self['value'])):
                if self['variable'][i] != self['value'][i]:
                    needToCheck = False
                    break
                    continue


        if needToCheck:
            self.check(False)



    def commandFunc(self, event):
        self.check()


    def check(self, fCommand = True):
        if len(self['value']) == len(self['variable']):
            pass
        len(self['variable']) != 0
        if 1:
            for i in xrange(len(self['value'])):
                self['variable'][i] = self['value'][i]


        self['isChecked'] = True
        self['geom'] = self['checkedGeom']
        for other in self['others']:
            if other != self:
                other.uncheck()
                continue

        if fCommand and self['command']:
            apply(self['command'], [
                self['value']] + self['extraArgs'])



    def setOthers(self, others):
        self['others'] = others


    def uncheck(self):
        self['isChecked'] = False
        self['geom'] = None
