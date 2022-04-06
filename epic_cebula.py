import time
import os
from pathlib import Path
import subprocess
import logging
from conf import *

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
nextgame_offset = int(width / 5.2)

# open epic game launcher app
subprocess.run(app_path)
x = subprocess.run('tasklist', capture_output=True)
while app_name not in str(x.stdout):
    pass

# locate free games
while True:
    pos = gui.locateOnScreen('Pics/free_now.png')
    if pos:
        break
    gui.scroll(-roll)
game_count = 0
pos = gui.locateOnScreen('Pics/free_now.png')
x = pos[0] + pos[2] + game_count * nextgame_offset + int(height / 100)
y = pos[1] + int(height / 100)
if gui.pixel(x, y)[2] > 128:
    gui.click(x, y)
else:
    pass  # not available


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
        break
gui.click(gui.center(pos))

# buy screen
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
    pass


if __name__ == '__main__':
    main()


