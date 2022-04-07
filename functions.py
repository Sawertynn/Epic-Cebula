import subprocess
import conf
import pyautogui as gui
import time


# store screen
def locate_free_games(game_count, s_size):
    direc = -1
    width, height = s_size
    while True:
        pos = locate_multi(conf.free_now)
        if pos:
            break
        gui.scroll(direc * int(height * conf.roll_mlt))
        if sum(gui.pixel(conf.scrollbar_x, conf.scrollbar_down)) > conf.scroll_color:
            direc = 1
        elif sum(gui.pixel(conf.scrollbar_x, conf.scrollbar_up)) > conf.scroll_color:
            direc = -1
    pos = locate_multi(conf.free_now, click=True)
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
    pos = locate_multi(conf.add_to_cart, click=True)
    locate_multi((conf.store, conf.back), reps=2, click=True)
    time.sleep(2)  # WAIT for store screen
    return bool(pos)


# buy screen
def buy_games():
    if not safe_click(conf.cart):
        return False
    if not safe_click(conf.checkout):
        return False
    # order screen loads long, more time and reps
    if not safe_click(conf.place_order, reps=5):
        return False
    if not safe_click(conf.agree):
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


def locate_multi(*targets, reps=1, click=False):
    pos = None
    for _ in range(reps):
        if pos:
            break
        for target in targets:
            if not isinstance(target, tuple):
                pos = gui.locateOnScreen(target)
                if pos:
                    break
            for tar in target:
                pos = gui.locateOnScreen(tar)
                if pos:
                    break
            if pos:
                break
    if pos and click:
        gui.click(pos)
    return pos


def safe_click(target, reps=3, do_press=True):
    x = locate_multi(target, reps=reps, click=do_press)
    return x

def cast(point: (int, int), size: (int, int)):
    x = point[0] * size[0] / conf.rel_width
    y = point[1] * size[1] / conf.rel_height
    return int(x), int(y)
