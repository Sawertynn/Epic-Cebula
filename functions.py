import subprocess
import conf
import pyautogui as gui
import time


# store screen
def locate_free_games(game_count, s_size):
    direc = -1
    width, height = s_size
    while True:
        pos = gui.locateOnScreen('Pics/free_now.png')
        if pos:
            break
        gui.scroll(direc * int(height * conf.roll_mlt))
        if sum(gui.pixel(conf.scrollbar_x, conf.scrollbar_down)) > conf.scroll_color:
            direc = 1
        elif sum(gui.pixel(conf.scrollbar_x, conf.scrollbar_up)) > conf.scroll_color:
            direc = -1
    pos = safe_click('Pics/free_now.png', do_press=False)
    if not pos:
        return -1, -1
    x = pos[0] + pos[2] + game_count * int(width * conf.next_game_mlt)
    y = pos[1] + int(height / 100)
    if gui.pixel(x, y)[2] > 128:
        return x, y
    else:
        return -1, -1


# game screen
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


def import_message(module):
    print(f'Please import {module} module, it\'s essential for this script to run')
    print(f'Run command below to install it on your computer:')
    print(f'python -m pip install {module}')
    print('To install it now, type yes, otherwise press Enter to exit')
    resp = input('> ')
    if 'yes' in resp.lower():
        subprocess.run(['python', '-m', 'pip', 'install', module])
        print('Run script again, should work now')
        input('Press Enter')


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
        return None
    if do_press:
        gui.click(gui.center(pos))
    return pos


def cast(point: (int, int), size: (int, int)):
    x = point[0] * size[0] / conf.rel_width
    y = point[1] * size[1] / conf.rel_height
    return int(x), int(y)
