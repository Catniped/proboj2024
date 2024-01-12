from easygame import draw_image, draw_text
import easygame, numpy
from math import isclose, atan

x_scale=0
y_scale=0

class uiGroup:
    """Object which groups together multiple UI Elements (images) and manages their rendering and callbacks"""
    def __init__(self, visible=True, enabled=True):
        self.elements = []
        self.visible = visible
        self.enabled = enabled

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
                if type(element) != textElement:
                    draw_image(element.image, element.position, element.anchor, element.rotation, element.scale, element.scale_x, element.scale_y, element.opacity, element.pixelated, element.ui)
                elif type(element) == textElement:
                    draw_text(element.text, element.font, element.size, element.position, element.anchor, element.color, element.bold, element.italic, element.ui)

    def checkGroup(self, event):
        """Checks whether an element in the group was clicked by the event passed, if true activates callback of the element"""
        if self.enabled:
            for element in self.elements:
                if type(element) == uiElement:
                    if element.enabled:
                        if checkIntersection(element.position, element.width*element.scale, element.height*element.scale, (event.x, event.y)):
                            element.clicked(event.button)
    
    def kill(self, obj):
        try:
            self.elements.remove(obj)
            return True
        except ValueError:
            return False

class uiElement:
    """Image used in the UI"""
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, enabled=True, visible=True):
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
        self.enabled = enabled
        self.visible = visible
        self.callback = callback
        self.ui = ui

        group.elements.append(self)
    
    def clicked(self, button):
        self.callback(button)

class textElement:
    """Image used in the UI"""
    def __init__(self, text, font, size, position=(0, 0), anchor=("left", "bottom"), color=(1, 1, 1, 1), bold=False, italic=False, ui=False, group=uiGroup, visible=True):
        self.text = text
        self.font = font
        self.size = size
        self.position = position
        self.anchor = anchor
        self.color = color
        self.bold = bold
        self.italic = italic
        self.ui = ui
        self.visible = visible

        group.elements.append(self)
    
    def clicked(self, button):
        self.callback(button)

class enemyElement:
    """Image used in the UI"""
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, health=10, speed=1, reward=1):
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

        self.reward = reward
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
            rx, ry = self.waypoints.pop(0)
            # self.routeto = self.waypoints.pop(0)
            # rx,ry = self.routeto
            # rx*=x_scale
            # ry*=y_scale
            self.routeto=(rx, ry)
            ys = ((ry - y)/-abs(rx - x))*self.speed
            self.velocity = (self.speed if rx < x else -self.speed, ys if ry < y else ys)

class archerTowerElement:
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, damage=10, speed=30, radius=100, price=100):
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

        self.damage = damage
        self.speed = speed
        self.radius = radius
        self.price = price
        self.cooldown = 0
        self.target = None
        self.arrows = []
        self.arrowcache = easygame.load_image("Assets/Sprites/Towers/Archer/arrow.png")

        group.elements.append(self)
    
    def cooldownCheck(self, enemygroup, projectilegroup):
        for arrow in self.arrows:
            arrow.rotate_arrow(self.get_velocity((self.ex,self.ey),(1,1)))
            return arrow.tick(self.target, enemygroup, projectilegroup, self)
        if self.cooldown > 0:
            self.cooldown-=1
        else:
            if self.enabled:
                if self.target:
                    self.cooldown = self.speed
                    self.arrows.append(projectileElement(self.arrowcache,(self.position[0],self.position[1]),group=projectilegroup,damage=self.damage)) 
                else:
                    for enemy in enemygroup.elements:
                        self.ex,self.ey = enemy.position
                        px,py = self.position

                        if (self.ex - px)**2 + (self.ey - py)**2 < self.radius**2:
                            self.target = enemy
                            break


    def get_velocity(self,enemyxy,enemyspeed):
        velocity1 = (enemyxy[0] + enemyspeed[0] * self.speed - self.position[0])/self.speed
        velocity2 = (enemyxy[1] + enemyspeed[1] * self.speed - self.position[1])/self.speed
        return (velocity1, velocity2)
    
    def kill(self, obj):
        try:
            self.arrows.remove(obj)
            return True
        except ValueError:
            return False
    
class projectileElement:
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None, ui=False, velocity=(0,0), damage=10):
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

        self.velocity = velocity
        self.damage = damage
        self.lifetime = 0
        self.maxlifetime = 60

        group.elements.append(self)

    def move_arrow(self,pos):
        pos[0] += self.velocity
        pos[1] += self.velocity
        return pos
    
    def rotate_arrow(self,velocity):
        self.rotation = atan(velocity[1]/velocity[0])

    def tick(self, enemy, enemygroup, projectilegroup, tower):
        if self.lifetime < self.maxlifetime:
            self.lifetime+=1
        else:
            if enemy:
                enemy.health-=self.damage
                if enemy.health <= 0:
                    i = enemy
                    r = i.reward
                    tower.target = None
                    if enemygroup.kill(i): return r
            projectilegroup.kill(self)
            tower.kill(self)

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

def placeTower(tower, umousex, umousey, down):
    scale = easygame.get_camera().zoom
    mousex = umousex/scale
    mousey = umousey/scale
    tower.position = (mousex,mousey)
    tower.opacity = 0.8
    easygame.draw_circle((mousex,mousey),tower.radius,color=(1,0,0,0.2))
    if down:
        tower.opacity = 1
        tower.enabled = True
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