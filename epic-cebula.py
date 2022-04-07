import time
import subprocess
import logging
import button as bt
import functions as func
import conf
try:
    import pyautogui as gui
except ImportError:
    func.import_message('pyautogui')
    exit()


def locate_free_games(game_count):
    direc = -1
    while True:
        pos = gui.locateOnScreen('Pics/free_now.png')
        if pos:
            break
        gui.scroll(direc * roll)
        if sum(gui.pixel(scrollbar_x, scrollbar_down)) > scroll_color:
            direc = 1
        elif sum(gui.pixel(scrollbar_x, scrollbar_up)) > scroll_color:
            direc = -1
    pos = func.safe_click('Pics/free_now.png', do_press=False)
    if not pos:
        logging.info('FAIL TO LOCATE free_now BUTTON')
        return -1, -1
    x = pos[0] + pos[2] + game_count * int(width / 5.2)
    y = pos[1] + int(height / 100)
    if gui.pixel(x, y)[2] > 128:
        return x, y
    else:
        return -1, -1


def add_to_cart(tile_pos):
    gui.click(tile_pos)
    pos = func.safe_click('Pics/add_to_cart.png')
    ret = func.safe_click('Pics/store.png')
    if not ret:
        func.safe_click('Pics/back.png')
    time.sleep(2)  # WAIT
    return bool(pos)


# buy screen
def buy_games():
    if not func.safe_click('Pics/cart.png'):
        return False
    if not func.safe_click('Pics/checkout.png'):
        return False
    # order screen loads long, more time and reps
    if not func.safe_click('Pics/place_order.png', reps=5, countdown=2):
        return False
    if not func.safe_click('Pics/agree.png'):
        return False
    return True


def main():
    game_count = 0
    func.launch_app()
    tile_pos = locate_free_games(game_count)
    while tile_pos[0] > 0:
        add_to_cart(tile_pos)
        game_count += 1
        tile_pos = locate_free_games(game_count)
    if buy_games():
        logging.info('Games were successfully obtained! Enjoy!')
    else:
        logging.info('Something went wrong, no games obtained')
    if conf.kill_app:
        out = subprocess.run(['taskkill', '/IM', conf.app_name], capture_output=True)
        logging.debug(out)


if __name__ == '__main__':
    level = logging.INFO
    logging.basicConfig(level=level)

    # global variables
    width, height = gui.size()
    roll = int(height / 3)
    freegame_offset = int(height / 5)
    nextgame_offset = int(width / 5.2)
    scrollbar_x = 1915
    scrollbar_up = 152
    scrollbar_down = 900
    scroll_color = 400  # RGB sum

    main()
