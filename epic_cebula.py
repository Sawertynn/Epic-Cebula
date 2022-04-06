import time
import os
from pathlib import Path
import subprocess
import logging
from conf import *

# future main() config and all

level = logging.DEBUG
logging.basicConfig(level=level)
logging.info('Hello!')
try:
    import pyautogui as gui
except ImportError:
    print('''
        Please import pyautogui module, it\'s essential for this script to run
        Run command below to install it on your computer:
        python -m pip install pyautogui''')
    exit()

# main variables
width, height = gui.size()
roll = int(height / 3)
freegame_offset = int(height / 5)
nextgame_offset = int(width / 5)

# open epic game launcher app
subprocess.run(app_path)
x = subprocess.run('tasklist', capture_output=True)
while app_name not in str(x.stdout):
    pass


# # switch to app
# startup = 2  #seconds
# start = time.perf_counter()
#
# while time.perf_counter() - start < startup:
#     if gui.locateOnScreen('epic_launcher_windows_max.png'):
#         logging.debug('app opened maximized, no switch')
#         break
#     pos = gui.locateOnScreen('epic_launcher_windows_mini.png')
#     if pos:
#         logging.debug('switched to app')
#         x, y, w, h = pos
#         gui.click(x + w // 2, y + h // 2)


# locate free games
while True:
    pos = gui.locateOnScreen('Pics/free_games.png')
    if pos:
        if pos[1] > 2 * roll:
            gui.scroll(-roll)
        break
    gui.scroll(-roll)

print(pos)
pos = gui.locateOnScreen('Pics/free_games.png')
gui.moveTo(pos[0], pos[1] + freegame_offset)
time.sleep(1)
gui.move(nextgame_offset, 0)
time.sleep(1)
gui.move(nextgame_offset, 0)
exit()

games_gotten = 1  # starting with 0
offset_x = games_gotten * 350
pos = gui.locateOnScreen('Pics/free_now.png')

logging.debug(f'{pos=}')
x = pos[0] + offset_x
y = pos[1]
gui.click(x, y)

# add game to cart

pos = None
while True:
    pos = gui.locateOnScreen('Pics/add_to_cart.png')
    if pos:
        break;
gui.click(gui.center(pos))

# buy screen
order_pos = 1432,970
order_color = 39,140,242
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
agree_pos = 1250,758
gui.moveTo(agree_pos)


