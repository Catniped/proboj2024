import easygame, uihelper, pyglet, random

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
damageUpgrade = 1
damageUpgradePrice = 1000
speedUpgrade = 1
speedUpgradePrice = 1000

window = easygame.open_window('window', 1600, 900, False, resizable=False)

def spawnEnemies():
    chanceModifier = round(35/difficultyModifier*2,0)
    if not random.randint(0,chanceModifier):
        uihelper.enemyElement(easygame.load_image("Assets/Sprites/UFO/UFO(3).png"),(1362,495),group=enemies,scale=0.3,reward=5*difficultyModifier*1.5,health=5*difficultyModifier*3)

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
    tower = uihelper.mageTowerElement(easygame.load_image("Assets/Sprites/Towers/Wizard/wizard_level_1.png"),(mousex+camera.position[0], mousey+camera.position[1]),group=towers,scale=0.3,price=200*difficultyModifier)
    placetower = True

def buyDamageUpgrade(buttons):
    global balance
    global damageUpgradePrice
    global damageUpgrade
    if balance >= damageUpgradePrice:
        balance-=damageUpgradePrice
        damageUpgradePrice*=2
        damageUpgrade+=0.1

def buySpeedUpgrade(buttons):
    global balance
    global speedUpgradePrice
    global speedUpgrade
    if balance >= speedUpgradePrice:
        balance-=speedUpgradePrice
        speedUpgradePrice*=2
        speedUpgrade*=0.9
    
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
"""uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Buttons/Rect-Icon-Blue/Play-Idle.png"),(100,100),group=ui1,scale=1,callback=spawnTestEnemy,ui=True)"""
balanceDisplay = uihelper.textElement(str(balance),"Poppins",30,(window.width-135,window.height-96),ui=True,group=ui1)

uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle_big.png"),(225,595),group=shopui,scale=1,enabled=False,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(275,660),group=shopui,scale=1.1,enabled=True,callback=buyArcherTower,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Wizard/wizard_level_1.png"),(475,660),group=shopui,scale=1.1,enabled=True,callback=buyMageTower,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Barrack/sword.png"),(715,665),group=shopui,scale=2.5,enabled=True,callback=buyDamageUpgrade,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/bow_animation(3).png"),(900,665),group=shopui,scale=2.5,enabled=True,callback=buySpeedUpgrade,ui=True)
archerPriceDisplay = uihelper.textElement(str(100*difficultyModifier),"Poppins",30,((315,610)),ui=True,group=shopui)
magePriceDisplay = uihelper.textElement(str(200*difficultyModifier),"Poppins",30,((515,610)),ui=True,group=shopui)
damageUpgradePriceDisplay = uihelper.textElement(str(damageUpgradePrice),"Poppins",30,((705,610)),ui=True,group=shopui)
damageUpgradeDisplay = uihelper.textElement(str(damageUpgrade) + "x","Poppins",30,((730,775)),ui=True,group=shopui)
speedUpgradePriceDisplay = uihelper.textElement(str(speedUpgradePrice),"Poppins",30,((905,610)),ui=True,group=shopui)
speedUpgradeDisplay = uihelper.textElement(str(speedUpgrade) + "x","Poppins",30,((920,775)),ui=True,group=shopui)


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

    spawnEnemies()
    
    """logic"""
    for enemy in enemies.elements:
        enemy.move()

    if placetower:
        if cancel:
            towers.kill(tower)
            placetower = False
            tower = None
        elif uihelper.placeTower(tower,mousex+camera.position[0],mousey+camera.position[1],downrm,balance):
            balance-=tower.price
            placetower = False
            tower = None

    for tower in towers.elements:
        r=tower.cooldownCheck(enemies, projectiles, damageUpgrade, speedUpgrade)
        if r:
            killcounter+=1
            balance+=r
        
    difficultyModifier = 1+killcounter/2000

    balanceDisplay.text = str(round(balance,1))
    archerPriceDisplay.text = str(round(100*difficultyModifier,1))
    magePriceDisplay.text = str(round(200*difficultyModifier,1))
    damageUpgradeDisplay.text = str(round(damageUpgrade,1)) + "x"
    damageUpgradePriceDisplay.text = str(damageUpgradePrice)
    speedUpgradeDisplay.text = str(round(speedUpgrade,2)) + "x"
    speedUpgradePriceDisplay.text = str(speedUpgradePrice)

    """rendering"""
    towers.renderGroup(window)
    enemies.renderGroup(window)
    projectiles.renderGroup(window)
    ui1.renderGroup(window)
    shopui.renderGroup(window)
    easygame.next_frame()
 
easygame.close_window()