import sys
import time

import colorama
from colorama import Back, Fore, Style
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier

from web_driver_conf import *

BANNER = """
 ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗    ██╗     ███╗   ███╗███████╗
██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝    ██║     ████╗ ████║██╔════╝
██║     ███████║█████╗  ██║     █████╔╝     ██║     ██╔████╔██║███████╗
██║     ██╔══██║██╔══╝  ██║     ██╔═██╗     ██║     ██║╚██╔╝██║╚════██║
╚██████╗██║  ██║███████╗╚██████╗██║  ██╗    ███████╗██║ ╚═╝ ██║███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝╚══════╝
"""

LINK = 'https://elearning.cis.asu.edu.eg/undergraduate/login/index.php'

SUBJECTS = ['Dummy 1-based', 'Database Management Systems', 'Discrete Mathematics',
            'Logic Design', 'Object Oriented Proramming', 'Report Writing', 'Statistical Analysis']

USERNAME = 'your username here'
PASSWORD = 'your password here'

usernameXpath = '//*[@id="username"]'
passwordXpath = '//*[@id="password"]'

driver = None
options = None
notification = None

colorama.init(autoreset=True)


def initConsole():
    global notification
    print(Fore.GREEN + BANNER)
    print('Logging in now, Please wait ...')
    notification = ToastNotifier()
    notification.show_toast(
        'Checking LMS now', 'Please Wait ...', 'col.ico', 4)


def initDriver():
    global driver, options
    options = get_web_driver_options()
    # ⮦ comment this one out if you want to see what's happening realtime (to render the GUI)
    set_automation_as_head_less(options)
    set_ignore_certificate_error(options)
    set_browser_as_incognito(options)
    driver = get_chrome_web_driver(options)


def login(un, pw):
    global driver
    driver.get(LINK)
    time.sleep(1)
    Uelement = driver.find_element_by_xpath(usernameXpath)
    Uelement.send_keys(un)
    Pelement = driver.find_element_by_xpath(passwordXpath)
    Pelement.send_keys(pw)
    Pelement.send_keys(Keys.ENTER)
    print('Logged in Succesfully!')

    # Manually go to home
    driver.get('https://elearning.cis.asu.edu.eg/undergraduate/my/')
    time.sleep(1)


def getStuff():
    i = 1
    flag = 0
    print('*'*60)
    try:
        elems = driver.find_elements_by_class_name('small')
        for el in elems:
            if i != 1:
                print('-'*40)

            # Gets the number out of (Course Progress: 100%)
            percentage = int(el.text.split()[2][:-1])

            if (percentage < 100 and i != 4) or (percentage < 98 and i == 4):
                print(f'{Fore.CYAN} New Stuff at {SUBJECTS[i]}')
                flag += 1
            else:
                print(f'{Fore.RED} Nothing new at {SUBJECTS[i]}')

            i += 1

        print('*'*60)
        print(Fore.GREEN + '\nTerminating now ...')

        if flag:
            notification.show_toast(
                'New Stuff Found', 'Please check LMS', 'col.ico', 8)
        else:
            notification.show_toast(
                'Nothing New', 'Keep up the good work', 'col.ico', 5)

    except:
        print("Problem with LMS servers")

    driver.close()
    print(Fore.GREEN + 'Terminated ...')
    sys.exit()


if __name__ == '__main__':
    initConsole()
    initDriver()
    login(USERNAME, PASSWORD)
    getStuff()
