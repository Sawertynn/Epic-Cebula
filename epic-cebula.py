#!python3
import time
import subprocess
import logging
import button as bt
import conf


def launch_app():
    subprocess.run(conf.app_path)
    x = subprocess.run('tasklist', capture_output=True)
    while conf.app_name not in str(x.stdout):
        pass


def safe_click(target, reps=3, countdown=0, *, do_press=True):
    if countdown > 0:
        time.sleep(countdown)
    pos = None
    for _ in range(reps):
        pos = gui.locateOnScreen(target)
        if pos:
            break
    if not pos:
        logging.info(f'FAIL: safe_click, {target=}')
        return None
    if do_press:
        gui.click(gui.center(pos))
    return pos


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
    pos = safe_click('Pics/free_now.png', do_press=False)
    if not pos:
        logging.info('FAIL TO LOCATE free_now BUTTON')
        return -1, -1
    x = pos[0] + pos[2] + game_count * int(width / 5.2)
    y = pos[1] + int(height / 100)
    if gui.pixel(x, y)[2] > 128:
        return x, y
    else:
        return -1, -1


# add game to cart
def add_to_cart(tile_pos):
    gui.click(tile_pos)
    pos = safe_click('Pics/add_to_cart.png')
    ret = safe_click('Pics/store.png')
    if not ret:
        safe_click('Pics/back.png')
    time.sleep(2)  # WAIT
    return bool(pos)


# buy screen
def buy_games():
    if not safe_click('Pics/cart.png'):
        return False
    if not safe_click('Pics/checkout.png'):
        return False
    # order screen loads long, more time and reps
    if not safe_click('Pics/place_order.png', reps=5, countdown=2):
        return False
    if not safe_click('Pics/agree.png'):
        return False
    return True


def main():
    game_count = 0
    launch_app()
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
    try:
        import pyautogui as gui
    except ImportError:
        gui = None
        print('''
            Please import pyautogui module, it\'s essential for this script to run
            Run command below to install it on your computer:
            python -m pip install pyautogui''')
        exit()

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