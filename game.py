import easygame, uihelper, pyglet

balance = 1000
cooldown = 0
arrows = []
mousex = (0,0)
mousey = (0,0)
cancel = False
downrm = False
downl = False
fullscreen = False
should_quit = False
tower = None
placetower = False
killcounter = 0

window = easygame.open_window('window', 1600, 900, fullscreen=fullscreen, resizable=True)

@window.event
def on_resize(width, height):
    global x_scale, y_scale
    x_scale=width/1600
    y_scale=height/900


x_scale=window.width/1600
y_scale=window.height/900

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
        toggleShop(None)
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

cartIcon = uihelper.uiElement(cartIconIdle,(50,window.height-105),group=ui1,scale=1,callback=toggleShop,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle.png"),(window.width-150,window.height-105),group=ui1,scale=1,enabled=False,ui=True)
balanceDisplay = uihelper.textElement(str(balance),"Poppins",30,(window.width-140,window.height-96),ui=True,group=ui1)

uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle_big.png"),(225*x_scale,window.height-305),group=shopui,scale=1*x_scale,enabled=False,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(275,window.height-240),group=shopui,scale=1.1*x_scale,enabled=True,callback=buyTower,ui=True)
uihelper.textElement("100","Poppins",30,((315,window.height-290)),ui=True,group=shopui)


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
                easygame.move_camera((-event.dx/camera.zoom,-event.dy/camera.zoom))
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