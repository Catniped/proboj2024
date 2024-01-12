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
difficultyModifier = 1

window = easygame.open_window('window', 1600, 900, False, resizable=False)

def spawnTestEnemy(buttons):
    uihelper.enemyElement(easygame.load_image("Assets/Sprites/UFO/UFO(3).png"),(1362,495),group=enemies,scale=0.3)
    playButton.image=playIconClick

def toggleShop(buttons):
    if not shopui.enabled:
        cartIcon.image = cartIconActive
        shopui.visible = True
        shopui.enabled = True
    else:
        cartIcon.image = cartIconIdle
        shopui.visible = False
        shopui.enabled = False

def buyArcherTower(buttons):
    global tower
    global placetower
    tower = uihelper.archerTowerElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(mousex+camera.position[0], mousey+camera.position[1]),group=towers,scale=0.3,price=100*difficultyModifier)
    placetower = True

def buyMageTower(buttons):
    global tower
    global placetower
    tower = uihelper.mageTowerElement(easygame.load_image("Assets/Sprites/Towers/Wizard/wizard_level_1.png"),(mousex+camera.position[0], mousey+camera.position[1]),group=towers,scale=0.3,price=100*difficultyModifier)
    placetower = True
    
mapi = easygame.load_image("Assets/Tileset/map.png")
offset = -(mapi.width*0.2 - window.width*2)
# print(offset)
xs=x_scale
if x_scale==1:
    xs=0

if y_scale==1:
    y_scale=0

offset=-76.8*x_scale+100*xs
offsetY=((116)*(y_scale))

ui1 = uihelper.uiGroup()
shopui = uihelper.uiGroup(visible=False,enabled=False)
enemies = uihelper.uiGroup()
towers = uihelper.uiGroup()
projectiles = uihelper.uiGroup()

cartIconIdle = easygame.load_image("Assets/Buttons/png/Buttons/Square-Icon-Blue/Cart-Idle.png")
cartIconActive = easygame.load_image("Assets/Buttons/png/Buttons/Square-Icon-Blue/Cart-Click.png")

playIconIdle = easygame.load_image("Assets/Buttons/png/Buttons/Rect-Icon-Blue/Play-Idle.png")
playIconClick = easygame.load_image("Assets/Buttons/png/Buttons/Rect-Icon-Blue/Play-Click.png")

cartIcon = uihelper.uiElement(cartIconIdle,(50,window.height-105),group=ui1,scale=1,callback=toggleShop,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle.png"),(window.width-150,window.height-105),group=ui1,scale=1,enabled=False,ui=True)
playButton=uihelper.uiElement(playIconIdle,(100,100),group=ui1,scale=1,callback=spawnTestEnemy,ui=True)
balanceDisplay = uihelper.textElement(str(balance),"Poppins",30,(window.width-140,window.height-96),ui=True,group=ui1)

uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle_big.png"),(225,595),group=shopui,scale=1,enabled=False,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(275,660),group=shopui,scale=1.1,enabled=True,callback=buyArcherTower,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Wizard/wizard_level_1.png"),(475,660),group=shopui,scale=1.1,enabled=True,callback=buyMageTower,ui=True)
uihelper.textElement(str(100*difficultyModifier),"Poppins",30,((315,610)),ui=True,group=shopui)


while not should_quit:
    camera=easygame.get_camera()
    if playButton.image is playIconClick:
        playButton.image=playIconIdle
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
    uihelper.drawCentered(mapi,scale=0.15,position=(offset,offsetY),window=window)

    """logic"""
    for enemy in enemies.elements:
        enemy.move()

    if placetower:
        if cancel:
            towers.kill(tower)
            placetower = False
            tower = None
        elif uihelper.placeTower(tower,mousex+camera.position[0]*2,mousey+camera.position[1]*2,downrm,balance):
            balance-=tower.price
            placetower = False
            tower = None

    for tower in towers.elements:
        r=tower.cooldownCheck(enemies, projectiles)
        if r:
            killcounter+=1
            balance+=r

    balanceDisplay.text = str(balance)

    """rendering"""
    towers.renderGroup(window)
    enemies.renderGroup(window)
    projectiles.renderGroup(window)
    ui1.renderGroup(window)
    shopui.renderGroup(window)
    easygame.next_frame()
 
easygame.close_window()