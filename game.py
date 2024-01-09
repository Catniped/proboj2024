import easygame, uihelper

window = easygame.open_window('window', None, None, True)
"""fsh = window.height
window.set_fullscreen(False)"""

def testCallback(button):
    print(button)

group1 = uihelper.uiGroup()
uihelper.uiElement(easygame.load_image("testbutton.png"),(400,300),group=group1,callback=testCallback)

fullscreen = False
should_quit = False
while not should_quit:

    for event in easygame.poll_events():
        evtype = type(event)
        if evtype is easygame.CloseEvent:
            should_quit = True
        if evtype is easygame.MouseDownEvent:
            group1.checkGroup(event)
        if evtype is easygame.KeyDownEvent:
            if event.key == "9":
                fullscreen = not fullscreen
                window.set_fullscreen(fullscreen)

    group1.renderGroup()

    easygame.next_frame()
 
easygame.close_window()