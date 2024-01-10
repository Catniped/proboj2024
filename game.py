import easygame, uihelper, time

x = 1

window = easygame.open_window('window', None, None, True, resizable=True)

@window.event
def on_resize(width, height):
    print("new window size:", width, height)

def testCallback(button):
    print(button)

mapi = easygame.load_image("Assets/Tileset/map.png")
offset = -(mapi.width*0.2 - window.width*2)
group1 = uihelper.uiGroup()
group2 = uihelper.uiGroup()
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Buttons/Rect-Icon-Blue/Play-Idle.png"),(100,100),group=group1,callback=testCallback,ui=True)
enemy = uihelper.enemyElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(1362,495),group=group2,scale=0.3)

"""
(1362,495)
(1362-342,495-195)


"""

down = False
fullscreen = True
should_quit = False
while not should_quit:
    for event in easygame.poll_events():
        evtype = type(event)
        if evtype is easygame.CloseEvent:
            should_quit = True
        elif evtype is easygame.MouseDownEvent:
            group1.checkGroup(event)
            if event.button != "LEFT":
                down = True
        elif evtype is easygame.MouseUpEvent:
            if event.button != "LEFT":
                down = False
        elif evtype is easygame.MouseMoveEvent:
            if down:
                easygame.move_camera((-event.dx,-event.dy))
        elif evtype is easygame.KeyDownEvent:
            if event.key == "F11":
                fullscreen = not fullscreen
                window.set_fullscreen(fullscreen)
        elif evtype is easygame.MouseScrollEvent:
            if event.scroll_y > 0:
                easygame.move_camera(zoom=1.2)
            else:
                easygame.move_camera(zoom=0.8)


    easygame.fill(0.200, 0.230, 0.245)
    uihelper.drawCentered(mapi,scale=0.15,position=(offset,0),window=window)
    group1.renderGroup(window)

    """ex, ey = enemy.position 
    if ex > 1020 and ey > 300:
        enemy.position = (ex-1.753,ey-1)"""
    
    enemy.move()
    group2.renderGroup(window)
    delta = x - time.time()
    x = time.time()
    easygame.next_frame()
 
easygame.close_window()