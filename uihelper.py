from easygame import draw_image
import easygame, numpy
from math import isclose

class uiGroup:
    """Object which groups together multiple UI Elements (images) and manages their rendering and callbacks"""
    def __init__(self):
        self.elements = []
        self.visible = True
        self.enabled = True

    def changeElementVisibility(self, visible):
        """Changes visibility property of the group and all elements"""
        self.visible = visible
        for element in self.elements:
            element.visible = visible

    def changeElementState(self, enabled):
        """Changes enabled property of the group and all elements"""
        self.enabled = enabled
        for element in self.elements:
            element.enabled = enabled
    
    def renderElements(self):
        """Renders all elements in UI Group, only considers element visibility"""
        for element in self.elements:
            if element.visible:
                draw_image(element.image, element.position, element.anchor, element.rotation, element.scale, element.scale_x, element.scale_y, element.opacity, element.pixelated, element.ui)

    def renderGroup(self, window):
        """Renders all elements in UI Group, only considers parent group visibility"""
        if self.visible:
            for element in self.elements:
                draw_image(element.image, element.position, element.anchor, element.rotation, element.scale, element.scale_x, element.scale_y, element.opacity, element.pixelated, element.ui)

    def checkGroup(self, event):
        """Checks whether an element in the group was clicked by the event passed, if true activates callback of the element"""
        if self.enabled:
            for element in self.elements:
                if checkIntersection(element.position, element.width, element.height, (event.x, event.y)):
                    element.clicked(event.button)

class uiElement:
    """Image used in the UI"""
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False):
        self.image = image
        self.width = image.width
        self.height = image.height
        self.center = image.center
        self.position = position
        self.anchor = anchor
        self.rotation = rotation
        self.scale = scale
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.opacity = opacity
        self.pixelated = pixelated
        self.enabled = True
        self.visible = True
        self.callback = callback
        self.ui = ui

        group.elements.append(self)
    
    def clicked(self, button):
        self.callback(button)

class enemyElement:
    """Image used in the UI"""
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, health=10, speed=1):
        self.image = image
        self.width = image.width
        self.height = image.height
        self.center = image.center
        self.position = position
        self.anchor = anchor
        self.rotation = rotation
        self.scale = scale
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.opacity = opacity
        self.pixelated = pixelated
        self.enabled = False
        self.visible = True
        self.callback = callback
        self.ui = ui

        self.health = health
        self.speed = speed
        self.routeto = None
        self.velocity = (0,0)
        self.waypoints = [(1020, 300),(594,540),(731,615),(595,693)]

        group.elements.append(self)
    
    def clicked(self, button):
        self.callback(button)
    
    def move(self):
        x,y = self.position
        if self.routeto:
            rx,ry = self.routeto
            if not isclose(x, rx, abs_tol=2) and not isclose(y, ry, abs_tol=2):
                xv, yv = self.velocity
                self.position = (x-xv,y-yv)
            else:
                self.routeto = None
        elif self.waypoints:
            self.routeto = self.waypoints.pop(0)
            rx,ry = self.routeto
            ys = ((ry - y)/-abs(rx - x))*self.speed
            self.velocity = (self.speed if rx < x else -self.speed, ys if ry < y else ys)

class archerTowerElement:
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, damage=10, speed=1, radius=100):
        self.image = image
        self.width = image.width
        self.height = image.height
        self.center = image.center
        self.position = position
        self.anchor = anchor
        self.rotation = rotation
        self.scale = scale
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.opacity = opacity
        self.pixelated = pixelated
        self.enabled = True
        self.visible = True
        self.callback = callback
        self.ui = ui
        self.damage = damage
        self.speed = speed
        self.radius = radius

        group.elements.append(self)

    def target(self,enemyxy,enemyspeed,enemyvector):
        target = (enemyxy[0] + enemyspeed * self.speed * enemyvector[0], enemyxy[1] + enemyspeed * self.speed * enemyvector[1])
        return target
    def move_arrow(self,pos,target):
        pos += target/30
        return pos
    
class mageTowerElement:
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, damage=10, speed=1, radius=10):
        self.image = image
        self.width = image.width
        self.height = image.height
        self.center = image.center
        self.position = position
        self.anchor = anchor
        self.rotation = rotation
        self.scale = scale
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.opacity = opacity
        self.pixelated = pixelated
        self.enabled = True
        self.visible = True
        self.callback = callback
        self.ui = ui

        self.damage = damage
        self.speed = speed
        self.radius = radius
        
        group.elements.append(self)
        
    def shoot(self,enemyxy):
        self.placement += enemyxy[0] - self.placement[0],enemyxy[1] - self.placement[1]

"""def loadSheetOOP(path, frame_width, frame_height, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None):
    for i in load_sheet(path, frame_width, frame_height):
        yield(uiElement(i, position, anchor, rotation, scale, scale_x, scale_y, opacity, pixelated, group, callback))"""

def placeTower(tower, mousex, mousey, down):
    tower.position = (mousex,mousey)
    tower.opacity = 0.8
    easygame.draw_circle((mousex,mousey),tower.radius,color=(1,0,0,0.2))
    if down:
        tower.opacity = 1
        return True
    return False


def checkIntersection(position: tuple, width, height, point: tuple):
    """ASSUMES RECTANGLE WITH ROTATION = 0
    Function which checks whether point is inside rectangle"""
    cx, cy = position
    px, py = point

    minx = cx
    maxx = cx+width
    miny = cy
    maxy = cy+height

    if px >= minx and px <= maxx and py >= miny and py <= maxy:
        return True
    
    return False

def drawCentered(image, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, ui=False, window=None):
    x,y = position

    position_e = (x-((((image.width-1400)*scale)/2)-(window.width/2)),y-(((image.height*scale)/2)-(window.height/2)))

    draw_image(image, position_e, anchor, rotation, scale, scale_x, scale_y, opacity, pixelated, ui)