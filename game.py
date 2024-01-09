import easygame, uihelper

easygame.open_window('window', 800, 600)

def testCallback(button):
    print(button)

group1 = uihelper.uiGroup()
uihelper.uiElement(easygame.load_image("testbutton.png"),(400,300),group=group1,callback=testCallback)

should_quit = False
while not should_quit:

    for event in easygame.poll_events():
        evtype = type(event)
        if evtype is easygame.CloseEvent:
            should_quit = True
        if evtype is easygame.MouseDownEvent:
            group1.checkGroup(event)

    group1.renderGroup()

    easygame.next_frame()
 
easygame.close_window()