import warnings
import requests
import click
import pyautogui
import json
from time import sleep
import sys

SERVER_URL = "http://elevenlogcollector-env.js6z6tixhb.us-west-2.elasticbeanstalk.com/ElevenServerLiteSnapshot"
INTERVAL = 1  # slows down clicking around


def retrieve_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


mappings = {
    'HOME': Position(600, 900),
    'JOINROOM': Position(1850, 470),
    'EXITROOM': Position(1217, 974),
}


def before_and_after_click(func):
    def wrapper(*args, **kwargs):
        type("M")
        sleep(INTERVAL)
        type("0")
        sleep(INTERVAL)
        func(*args, **kwargs)
        type("M")
        return
    return wrapper


def clickButton(button, move_only=False):
    x, y = mappings[button].x, mappings[button].y
    pyautogui.moveTo(x, y)
    if not move_only:
        # pyautogui.click()
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()
        print(f"Clicked {button}")
    else:
        print(f"Moved to {x, y}")
        sleep(0.3)


@before_and_after_click
def clickListOfButtons(list_of_buttons, move_only=False):
    for button in list_of_buttons if isinstance(list_of_buttons, list) else [list_of_buttons]:
        clickButton(button, move_only=move_only)
        sleep(INTERVAL)


def joinRoom(test):
    clickListOfButtons("HOME JOINROOM".split())


def exitRoom(test):
    clickListOfButtons("HOME EXITROOM".split())


def type(str):
    print(f"Pressed {str}")
    pyautogui.write(str)


def retrieve_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def isInRoom(user):
    try:
        content = json.loads(retrieve_url(SERVER_URL))
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        warnings.warn("Failed to retrieve data from server.")
        return None
    users = [x for x in content['UsersInRooms'] if x['UserName'] == user]
    if (len(users) > 0):
        sys.stdout.flush()
        return True

    sys.stdout.flush()
    return False


def print_mouse():
    mouse_position = pyautogui.position()
    print(
        f"Mouse position: {mouse_position[0]:04d}, {mouse_position[1]:04d}", end='')
    sys.stdout.write('\r')


@click.command()
@click.option('--test', '-t', is_flag=True, default=False, help='Whether to avoid clicks')
@click.option('--user', '-u', help='Username', required=True)
def main(user, test):

    # it assumes that menu is off in the UI

    while True:
        print(f"Waiting until {user} is in a room...")
        inRoom = False
        while not inRoom or inRoom is None:
            inRoom = isInRoom(user)
            print_mouse()
            sleep(INTERVAL)
        print(f"User {user} is in a room!",  end='')
        print(f"Joining room.")
        joinRoom(test)

        while inRoom or inRoom is None:
            inRoom = isInRoom(user)
            print_mouse()
            sleep(INTERVAL)
        print(f"User {user} is no longer in a room.")
        print(f"Leaving room.")
        exitRoom(test)


if __name__ == '__main__':
    main(sys.argv[1:])
