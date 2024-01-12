import easygame, uihelper, pyglet

window = easygame.open_window('window', 1600, 900, False, resizable=False)

res_scale_x=(window.width/1600)
res_scale_y=(window.height/900)

uihelper.x_scale=res_scale_x
uihelper.y_scale=res_scale_y

def testCallback(button):
    uihelper.enemyElement(easygame.load_image("Assets/Sprites/UFO/UFO(3).png"),(1362,495),group=enemies,scale=0.3,health=100)

mapi = easygame.load_image("Assets/Tileset/map.png")
# offset = (window.width - mapi.width) / 2
offset = -(mapi.width*0.2 - window.width*2)


print(offset, window.width/1600)
# offset = offset*res_scale_x
print(offset)

# if (offset > window.width/2):
#     offsetX = -(mapi.width - window.width/2)
# elif (offset + mapi.width < window.width/2):
#     offsetX = window.width/2 - (offset + mapi.width)

# if (mapi.center[0] > window.width/2):
#     offsetX = (mapi.center[0] - window.width/2)
#     print("hi", offsetX)
# elif (mapi.center[0] + mapi.width < window.width/2):
#     offsetX = window.width/2 - (mapi.center[0] + mapi.width)
#     print("hi2")

ui1 = uihelper.uiGroup()
enemies = uihelper.uiGroup()
towers = uihelper.uiGroup()
projectiles = uihelper.uiGroup()

uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Buttons/Rect-Icon-Blue/Play-Idle.png"),(100,100),group=ui1,scale=1,callback=testCallback,ui=True)

balance = 1000
cooldown = 0
arrows = []
mousex = (0,0)
mousey = (0,0)
cancel = False
downrm = False
downl = False
fullscreen = True
should_quit = False
tower = None
placetower = False
killcounter = 0

window = easygame.open_window('window', 1600, 900, False, resizable=False)

def toggleShop(buttons):
    if not shopui.enabled:
        cartIcon.image = cartIconActive
        shopui.visible = True
        shopui.enabled = True
    else:
        cartIcon.image = cartIconIdle
        shopui.visible = False
        shopui.enabled = False

def buyTower(buttons):
    global tower
    global placetower
    global downl
    global balance
    if balance-100 >= 0:
        tower = uihelper.archerTowerElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(mousex+camera.position[0], mousey+camera.position[1]),group=towers,scale=0.3)
        placetower = True
    
mapi = easygame.load_image("Assets/Tileset/map.png")
offset = -(mapi.width*0.2 - window.width*2)

ui1 = uihelper.uiGroup()
shopui = uihelper.uiGroup(visible=False,enabled=False)
enemies = uihelper.uiGroup()
towers = uihelper.uiGroup()
projectiles = uihelper.uiGroup()

cartIconIdle = easygame.load_image("Assets/Buttons/png/Buttons/Square-Icon-Blue/Cart-Idle.png")
cartIconActive = easygame.load_image("Assets/Buttons/png/Buttons/Square-Icon-Blue/Cart-Click.png")

cartIcon = uihelper.uiElement(cartIconIdle,(50,795),group=ui1,scale=1,callback=toggleShop,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle.png"),(1450,795),group=ui1,scale=1,enabled=False,ui=True)
balanceDisplay = uihelper.textElement(str(balance),"Poppins",30,(1469,804),ui=True,group=ui1)

uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle_big.png"),(225,595),group=shopui,scale=1,enabled=False,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(275,660),group=shopui,scale=1.1,enabled=True,callback=buyTower,ui=True)
uihelper.textElement("100","Poppins",30,((315,610)),ui=True,group=shopui)


while not should_quit:
    camera=easygame.get_camera()
    for event in easygame.poll_events():
        evtype = type(event)
        if evtype is easygame.CloseEvent:
            should_quit = True
        elif evtype is easygame.MouseDownEvent:
            ui1.checkGroup(event)
            shopui.checkGroup(event)
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
            mousex = event.x-camera.position[0]
            mousey = event.y-camera.position[1]
            if downrm:
                easygame.move_camera((-event.dx,-event.dy))
        elif evtype is easygame.KeyDownEvent:
            if event.key == "F11":
                fullscreen = not fullscreen
                window.set_fullscreen(fullscreen)
            elif event.key == "ESC":
                cancel = True
        elif evtype is easygame.KeyUpEvent:
            if event.key == "ESC":
                cancel = False
        elif evtype is easygame.MouseScrollEvent:
            if event.scroll_y > 0:
                easygame.move_camera(zoom=1.2)
            else:
                easygame.move_camera(zoom=0.8)

    """scene prep"""
    easygame.fill(0.200, 0.230, 0.245)
    uihelper.drawCentered(mapi,scale=0.15,position=(offset,0),window=window)

    """logic"""
    for enemy in enemies.elements:
        enemy.move()

    if placetower:
        if cancel:
            towers.kill(tower)
            placetower = False
            tower = None
        elif uihelper.placeTower(tower,mousex+camera.position[0],mousey+camera.position[1],downrm):
            balance-=tower.price
            placetower = False
            tower = None

    for tower in towers.elements:
        r=tower.cooldownCheck(enemies, balance)
        if r:
            killcounter+=1
            balance+=r

    balanceDisplay.text = str(balance)

    """rendering"""
    towers.renderGroup(window)
    enemies.renderGroup(window)
    ui1.renderGroup(window)
    shopui.renderGroup(window)
    easygame.next_frame()
 
easygame.close_window()