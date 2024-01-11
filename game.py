import easygame, uihelper, pyglet

window = easygame.open_window('window', None, None, False, resizable=True)

def testCallback(button):
    print(button)

mapi = easygame.load_image("Assets/Tileset/map.png")
offset = -(mapi.width*0.2 - window.width*2)
group1 = uihelper.uiGroup()
group2 = uihelper.uiGroup()
group3 = uihelper.uiGroup()
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Buttons/Rect-Icon-Blue/Play-Idle.png"),(100,100),group=group1,scale=2,callback=testCallback,ui=True)
enemy = uihelper.enemyElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(1362,495),group=group2,scale=0.3)

mousex = (0,0)
mousey = (0,0)
placetower = False
downrm = False
downl = False
fullscreen = True
should_quit = False
while not should_quit:
    camera=easygame.get_camera()
    for event in easygame.poll_events():
        evtype = type(event)
        if evtype is easygame.CloseEvent:
            should_quit = True
        elif evtype is easygame.MouseDownEvent:
            group1.checkGroup(event)
            if event.button != "LEFT":
                downrm = True
            else:
                downl = True
        elif evtype is easygame.MouseUpEvent:
            if event.button != "LEFT":
                downrm = False
            else:
                downl = False
        elif evtype is easygame.MouseMoveEvent:
            mousex = event.x
            mousey = event.y
            if downrm:
                easygame.move_camera((-event.dx,-event.dy))
        elif evtype is easygame.KeyDownEvent:
            if event.key == "F11":
                fullscreen = not fullscreen
                window.set_fullscreen(fullscreen)
            elif event.key == "E":
                print("pos", mousex, camera.position)
                tower = uihelper.archerTowerElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(mousex+camera.position[0], mousey+camera.position[1]),group=group3,scale=0.3)
                placetower = True
        elif evtype is easygame.MouseScrollEvent:
            if event.scroll_y > 0:
                easygame.move_camera(zoom=1.2)
            else:
                easygame.move_camera(zoom=0.8)

    easygame.fill(0.200, 0.230, 0.245)
    uihelper.drawCentered(mapi,scale=0.15,position=(offset,0),window=window)

    enemy.move()
    if placetower:
        if uihelper.placeTower(tower,mousex+camera.position[0],mousey+camera.position[1],downl):
            placetower = False
            tower = None
    
    group1.renderGroup(window)
    group3.renderGroup(window)
    group2.renderGroup(window)
    easygame.next_frame()
 
easygame.close_window()