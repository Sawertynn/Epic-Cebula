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


def launch_app():
    subprocess.run(app_path)
    x = subprocess.run('tasklist', capture_output=True)
    while app_name not in str(x.stdout):
        pass


def locate_free_games(game_count):
    while True:
        pos = gui.locateOnScreen('Pics/free_now.png')
        if pos:
            break
        gui.scroll(-roll)
    pos = gui.locateOnScreen('Pics/free_now.png')
    x = pos[0] + pos[2] + game_count * int(width / 5.2)
    y = pos[1] + int(height / 100)
    if gui.pixel(x, y)[2] > 128:
        return x, y
    else:
        return -1, -1


# add game to cart
def add_to_cart(tile_pos):
    gui.click(tile_pos)
    time.sleep(2)
    pos = gui.locateOnScreen('Pics/add_to_cart.png')
    if pos:
        gui.click(gui.center(pos))
    back = gui.locateOnScreen('Pics/back.png')
    if not back:
        back = gui.locateOnScreen('Pics/store.png')
    gui.click(back)
    return bool(pos)


# buy screen
def buy_games():
    order_pos = 1432, 970
    order_color = 39, 140, 242
    min_color = 220
    max_color = 560

    while True:
        color = sum(gui.pixel(order_pos[0], order_pos[1]))
        if color in range(min_color, max_color):
            break
        time.sleep(.2)

    gui.moveTo(order_pos)
    gui.click(order_pos)

    # agree
    agree_pos = 1250, 758
    gui.moveTo(agree_pos)


def main():
    game_count = 0
    launch_app()
    tile_pos = locate_free_games(game_count)
    logging.info(f'{tile_pos=}')
    while tile_pos[0] > 0:
        add_to_cart(tile_pos)
        game_count += 1
        logging.info(f'gc={game_count}, pos={tile_pos}')
        locate_free_games(game_count)


if __name__ == '__main__':
    level = logging.INFO
    logging.basicConfig(level=level)
    main()

