from easygame import draw_image, load_sheet, draw_circle

class uiGroup:
    def __init__(self):
        self.elements = []
        self.visible = True
        self.enabled = True

    def changeElementVisibility(self, visible):
        self.visible = visible
        for element in self.elements:
            element.visible = visible

    def changeElementState(self, enabled):
        self.enabled = enabled
        for element in self.elements:
            element.enabled = enabled
    
    def renderElements(self):
        for element in self.elements:
            if element.visible:
                draw_image(element.image, element.position, element.anchor, element.rotation, element.scale, element.scale_x, element.scale_y, element.opacity, element.pixelated, element.ui)

    def renderGroup(self):
        if self.visible:
            for element in self.elements:
                draw_image(element.image, element.position, element.anchor, element.rotation, element.scale, element.scale_x, element.scale_y, element.opacity, element.pixelated, element.ui)

    def checkGroup(self, event):
        if self.enabled:
            for element in self.elements:
                if checkIntersection(element.position, element.width, element.height, (event.x, event.y)):
                    element.clicked(event.button)

class uiElement:
    def __init__(self, image=None, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None):
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
        self.ui = False

        group.elements.append(self)
    
    def clicked(self, button):
        self.callback(button)

"""def loadSheetOOP(path, frame_width, frame_height, position=(0, 0), anchor=None, rotation=0, scale=1, scale_x=1, scale_y=1, opacity=1, pixelated=False, group=uiGroup, callback=None):
    for i in load_sheet(path, frame_width, frame_height):
        yield(uiElement(i, position, anchor, rotation, scale, scale_x, scale_y, opacity, pixelated, group, callback))"""

def checkIntersection(position: tuple, width, height, point: tuple):
    """ASSUMES RECTANGLE WITH ROTATION = 0"""
    cx, cy = position
    px, py = point

    minx = cx
    maxx = cx+width
    miny = cy
    maxy = cy+height

    if px >= minx and px <= maxx and py >= miny and py <= maxy:
        return True
    
    return False