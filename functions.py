import subprocess
import conf
import pyautogui as gui
import time


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
        # logging.info(f'FAIL: safe_click, {target=}')
        return None
    if do_press:
        gui.click(gui.center(pos))
    return pos


