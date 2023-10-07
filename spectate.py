import click
import pyautogui
import urllib.request
import json
from time import sleep
import sys

SERVER_URL = "http://elevenlogcollector-env.js6z6tixhb.us-west-2.elasticbeanstalk.com/ElevenServerLiteSnapshot"
import requests

def retrieve_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
INTERVAL = 1  # in s
neutralCamNr = 0
homeCamNr = 8
awayCamNr = 9
firstMatch = True


class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


mappings = {
        # { width: 1920, height: 1080 },
        'ACTIVATEWINDOW': Position(10, 10),
        'HOME': Position(600, 900),
        'USERPROFILE': Position(1521, 488),
        # 'JOINROOM': Position(900, 430),
        'JOINROOM': Position(1850, 470),
        'HIDEMOUSE': Position(1920-10, 1080-10),
        'EXITROOM': Position(1217, 974),
    }

@click.command()
@click.argument('test', type=bool)
def _clickPos(x, y, test=False):
    pyautogui.moveTo(x, y)
    # pyautogui.click()
    pyautogui.mouseDown()
    sleep(0.05)
    pyautogui.mouseUp()

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

def type(str):
    print(f"Pressed {str}")
    pyautogui.write(str)


def joinRoom(test):
    type("M")
    type("0")
    # clickButton("ACTIVATEWINDOW", move_only=test)
    clickButton("HOME", move_only=test)
    sleep(1)
    clickButton("USERPROFILE", move_only=test)
    sleep(1)
    clickButton("JOINROOM", move_only=test)
    sleep(1)
    clickButton("HIDEMOUSE", move_only=test)
    type("M")


def exitRoom(test):
    type("M")
    type("0")
    clickButton("HOME", move_only=test)
    sleep(1)
    clickButton("EXITROOM", move_only=test)
    type("M")


def retrieve_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Usage

def isInRoom(user):
    # TODO: This can be done via OCR instead, to minimize server load
    # OR....can also get it from the logs
    content = json.loads(retrieve_url(SERVER_URL))
    users = [x for x in content['UsersInRooms'] if x['UserName'] == user]
    if (len(users) > 0):
        sys.stdout.flush()
        return True

    sys.stdout.flush()
    return False

def print_mouse():
    mouse_position = pyautogui.position()
    print(f"Mouse position: {mouse_position[0]:04d}, {mouse_position[1]:04d}", end='')
    sys.stdout.write('\r')

@click.command()
@click.option('--test', '-t', is_flag=True, default=False, help='Whether to avoid clicks')
@click.option('--user', '-u', default='faffopong', help='Username')
def main(user, test):
    print(test)

    while True:
        print(f"Waiting until {user} is in a room...")
        inRoom = False
        while not inRoom:
            inRoom = isInRoom(user)
            print_mouse()
            sleep(INTERVAL)
        print(f"User {user} is in a room!",  end='')
        print(f"Joining room.")
        joinRoom(test)
        while inRoom:
            inRoom = isInRoom(user)
            print_mouse()
            sleep(INTERVAL)
        print(f"👻 User {user} is not in a room anymore.")
        print(f"Leavining room.")
        exitRoom(test)


if __name__ == '__main__':
    main(sys.argv[1:])