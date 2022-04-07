import time
import os
from pathlib import Path
import subprocess
import logging
from conf import *
import pyautogui as gui

# try:
#     import pyautogui as gui
# except ImportError:
#     print('''
#         Please import pyautogui module, it\'s essential for this script to run
#         Run command below to install it on your computer:
#         python -m pip install pyautogui''')
#     exit()

# global variables
width, height = gui.size()
roll = int(height / 3)
freegame_offset = int(height / 5)
nextgame_offset = int(width / 5.2)
scrollbar_x = 1915
scrollbar_up = 152
scrollbar_down = 900
scroll_color = 400  # RGB sum


def launch_app():
    subprocess.run(app_path)
    x = subprocess.run('tasklist', capture_output=True)
    while app_name not in str(x.stdout):
        pass


def safe_click(target, reps=3, countdown=0):
    if countdown > 0:
        time.sleep(countdown)
    for _ in range(reps):
        pos = gui.locateOnScreen(target)
        if pos:
            break
    if not pos:
        return False
    gui.click(gui.center(pos))
    return True


def locate_free_games(game_count):
    direc = -1;
    while True:
        pos = gui.locateOnScreen('Pics/free_now.png')
        if pos:
            break
        gui.scroll(direc * roll)
        if sum(gui.pixel(scrollbar_x, scrollbar_down)) > scroll_color:
            direc = 1
        elif sum(gui.pixel(scrollbar_x, scrollbar_up)) > scroll_color:
            direc = -1
    for _ in range(3):
        pos = gui.locateOnScreen('Pics/free_now.png')
        if pos:
            break
    if not pos:
        print('HEAVY ERROR')
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
    for _ in range(3):
        pos = gui.locateOnScreen('Pics/add_to_cart.png')
        if pos:
            break
        if gui.locateOnScreen('Pics/view_in_chart.png'):  # already in chart
            break
    if pos:
        gui.click(gui.center(pos))
    back = gui.locateOnScreen('Pics/back.png')
    if not back:
        back = gui.locateOnScreen('Pics/store.png')
    gui.click(back)
    time.sleep(2)
    return bool(pos)


# buy screen
def buy_games():
    for _ in range(3):
        pos = gui.locateOnScreen('Pics/cart.png')
        if pos:
            break
    if not pos:
        return
    gui.click(gui.center(pos))

    for _ in range(3):
        pos = gui.locateOnScreen('Pics/checkout.png')
        if pos:
            break
    if not pos:
        return
    gui.click(gui.center(pos))

    for _ in range(5):
        pos = gui.locateOnScreen('Pics/place_order.png')
        if pos:
            break
    if not pos:
        return
    gui.click(gui.center(pos))

    for _ in range(3):
        pos = gui.locateOnScreen('Pics/agree.png')
        if pos:
            break
    if not pos:
        return
    gui.click(gui.center(pos))


def main():
    # game_count = 0
    # launch_app()
    # tile_pos = locate_free_games(game_count)
    # logging.info(f'{tile_pos=}')
    # while tile_pos[0] > 0:
    #     add_to_cart(tile_pos)
    #     game_count += 1
    #     logging.info(f'before -- gc={game_count}, pos={tile_pos}')
    #     tile_pos = locate_free_games(game_count)
    #     logging.info(f'after -- gc={game_count}, pos={tile_pos}')
    gui.hotkey('alt', 'tab')
    buy_games()
    subprocess.run(['taskkill', app_name], capture_output=True)


if __name__ == '__main__':
    level = logging.INFO
    logging.basicConfig(level=level)
    main()

