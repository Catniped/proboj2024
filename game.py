from easygame import *
 
# Otvor okno s nadpisom "Panda simulator"
# vo veľkosti 800px na šírku a 600px na výšku
open_window('Panda simulator', 800, 600)
 
# Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
should_quit = False
while not should_quit:
 
    # Načítaj udalosti pre aktuálnu snímku
    for event in poll_events():
        # Napríklad ak hráč spustí CloseEvent
        # prestaň ďalej vykreslovať snímky a zatvor okno 
        if type(event) is CloseEvent:
            should_quit = True
    
    ###
    # Tu patrí logika hry, ktorá na obrazovku niečo vykreslí
    ###
 
    draw_polygon((0, 0), (500, 300), (200, 0))

    # Pokračuj na ďalšiu snímku (a všetko opať prekresli)
    next_frame()
 
close_window()