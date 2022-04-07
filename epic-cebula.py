import subprocess
import logging
import functions as func
import conf
try:
    import pyautogui as gui
except ImportError:
    func.import_message('pyautogui')
    exit()


def main():
    logging.basicConfig(level=logging.INFO)
    game_count = 1
    func.launch_app()
    while True:
        tile_pos = func.locate_free_games(game_count, gui.size())
        if tile_pos[0] < 0:  # game not available
            break
        func.add_to_cart(tile_pos)
        game_count += 1

    if func.buy_games():
        logging.info('Games were successfully obtained! Enjoy!')
    else:
        logging.info('Something went wrong, no games obtained')

    if conf.kill_app:
        out = subprocess.run(['taskkill', '/IM', conf.app_name], capture_output=True)
        logging.debug(out)


if __name__ == '__main__':
    main()
