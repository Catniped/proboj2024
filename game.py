import easygame, uihelper, pyglet, random, sys

SPAWNRATE = int(sys.argv[1]) if len(sys.argv) >= 2 else 25
BALANCE = 1000
CASTLEHEALTH = 100
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
placebomb = False
killcounter = 0
difficultyModifier = 1
damageUpgrade = 1
damageUpgradePrice = 1000
speedUpgrade = 1
speedUpgradePrice = 1000

window = easygame.open_window('Rieka', 1600, 900, False, resizable=True)

palace = easygame.load_image("Assets/Sprites/chineees_castle.png")

palace = easygame.load_image("Assets/Sprites/chineees_castle.png")

def spawnEnemies():
    chanceModifier = round(SPAWNRATE/difficultyModifier*2,0)
    if not random.randint(0,chanceModifier):
        uihelper.enemyElement(easygame.load_image("Assets/Sprites/UFO/UFO(3).png"),(1362,495),group=enemies,scale=0.3,reward=5*difficultyModifier*1.5,health=10*difficultyModifier*3, speed=1*difficultyModifier)

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
    tower = uihelper.mageTowerElement(easygame.load_image("Assets/Sprites/Towers/Wizard/wizard_level_3.png"),(mousex+camera.position[0], mousey+camera.position[1]),group=towers,scale=0.3,price=200*difficultyModifier)
    placetower = True

def buyDamageUpgrade(buttons):
    global BALANCE
    global damageUpgradePrice
    global damageUpgrade
    if BALANCE >= damageUpgradePrice:
        BALANCE-=damageUpgradePrice
        damageUpgradePrice*=2
        damageUpgrade+=0.1

def buySpeedUpgrade(buttons):
    global BALANCE
    global speedUpgradePrice
    global speedUpgrade
    if BALANCE >= speedUpgradePrice:
        BALANCE-=speedUpgradePrice
        speedUpgradePrice*=2
        speedUpgrade*=0.9

def buyBomb(buttons):
    global placebomb
    placebomb = True
    
mapi = easygame.load_image("Assets/Tileset/map.png")
offset = -(mapi.width*0.2 - window.width*2)

x_scale=window.width/1600
y_scale=window.height/900

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

cartIcon = uihelper.uiElement(cartIconIdle,(50,window.height-105),group=ui1,scale=1,callback=toggleShop,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle.png"),(window.width-150,window.height-105),group=ui1,scale=1,enabled=False,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle.png"),(50,50),group=ui1,scale=1,ui=True,enabled=False)
BALANCEDisplay = uihelper.textElement(str(BALANCE),"Poppins",30,(window.width-140,window.height-96),ui=True,group=ui1)
CASTLEHEALTHDisplay = uihelper.textElement(str(CASTLEHEALTH),"Poppins",30,(80,57),ui=True,group=ui1)

uihelper.uiElement(easygame.load_image("Assets/Buttons/png/Dummy/Rect-Icon-Blue/Idle_big.png"),(225*x_scale,window.height-305),group=shopui,scale=1*x_scale,enabled=False,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/archer_level_1.png"),(275*x_scale,window.height-240),group=shopui,scale=1.1*x_scale,enabled=True,callback=buyArcherTower,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Wizard/wizard_level_3.png"),(475*x_scale,window.height-240),group=shopui,scale=1.1*x_scale,enabled=True,callback=buyMageTower,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Barrack/sword.png"),(715*x_scale,window.height-235),group=shopui,scale=2.5*x_scale,enabled=True,callback=buyDamageUpgrade,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Archer/bow_animation(3).png"),(900*x_scale,window.height-235),group=shopui,scale=2.5*x_scale,enabled=True,callback=buySpeedUpgrade,ui=True)
uihelper.uiElement(easygame.load_image("Assets/Sprites/Towers/Wizard/stick.png"),(1125*x_scale,window.height-235),group=shopui,scale=2.5*x_scale,enabled=True,callback=buyBomb,ui=True)
archerPriceDisplay = uihelper.textElement(str(100*difficultyModifier),"Poppins",30,((315*x_scale,window.height-290)),ui=True,group=shopui)
magePriceDisplay = uihelper.textElement(str(200*difficultyModifier),"Poppins",30,((515*x_scale,window.height-290)),ui=True,group=shopui)
bombPriceDisplay = uihelper.textElement(str(1000*difficultyModifier),"Poppins",30,((1110*x_scale,window.height-290)),ui=True,group=shopui)
damageUpgradePriceDisplay = uihelper.textElement(str(damageUpgradePrice),"Poppins",30,((705*x_scale,window.height-290)),ui=True,group=shopui)
damageUpgradeDisplay = uihelper.textElement(str(damageUpgrade) + "x","Poppins",30,((730,window.height-125)),ui=True,group=shopui)
speedUpgradePriceDisplay = uihelper.textElement(str(speedUpgradePrice),"Poppins",30,((905*x_scale,window.height-290)),ui=True,group=shopui)
speedUpgradeDisplay = uihelper.textElement(str(speedUpgrade) + "x","Poppins",30,((920,window.height-125)),ui=True,group=shopui)

easygame.play_audio(easygame.load_audio("Assets/Audio/background_music.mp3"), 0, True)

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
            elif event.key == "E":
                toggleShop(None)
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
    easygame.draw_image(palace, (461,684), scale=0.3)

    spawnEnemies()
    
    """logic"""
    for enemy in enemies.elements:
        if enemy.move():
            CASTLEHEALTH-=1
    
    if CASTLEHEALTH <= 0:
        print("You lost! Try again!")
        exit()

    if placetower:
        if cancel:
            towers.kill(tower)
            placetower = False
            tower = None
        elif uihelper.placeTower(tower,mousex+camera.position[0]*2,mousey+camera.position[1]*2,downrm,BALANCE):
            BALANCE-=tower.price
            placetower = False
            tower = None
        
    if placebomb:
        if cancel:
            placebomb = False
        elif uihelper.placeBomb(enemies,mousex+camera.position[0]*2,mousey+camera.position[1]*2,downrm,BALANCE,difficultyModifier):
            BALANCE-=1000*difficultyModifier
            placebomb = False

    for tower in towers.elements:
        r=tower.cooldownCheck(enemies, projectiles, damageUpgrade, speedUpgrade)
        if r:
            killcounter+=1
            BALANCE+=r
        
    difficultyModifier = 1+killcounter/2000

    BALANCEDisplay.text = str(round(BALANCE,1))
    CASTLEHEALTHDisplay.text = str(CASTLEHEALTH)
    archerPriceDisplay.text = str(round(100*difficultyModifier,1))
    magePriceDisplay.text = str(round(200*difficultyModifier,1))
    bombPriceDisplay.text = str(round(1000*difficultyModifier,1))
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