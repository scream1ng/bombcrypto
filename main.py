import mss
import cv2 as cv
import numpy as np
import os
import pyautogui
import random
import time
import yaml

# load config.yaml
f = open('config.yaml', 'r')
conf = yaml.safe_load(f)
f.close()

def screen_shot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
    return img

def load_template(dir='img/'):
    file_names = os.listdir(dir)
    template = {}
    for file in file_names:
        path = dir + file
        template[file[:-len('.jpg')]] = cv.imread(path)
    return template

def position(template, threshold = conf['threshold'], img = None):
    if img is None:
        img = screen_shot()

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    w = template.shape[1]
    h = template.shape[0]

    yloc, xloc = np.where(result >= threshold)
    rectangles = []

    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def click_template(template, value = 0, threshold = conf['threshold'], img = None):
    attempt = 1
    while attempt <= 3:
        try:
            rect = position(template, threshold, img)

            if value == 'all':
                for x, y, w, h in rect:
                    x_loc = x + w/2 + random.randint(-int(w/2), int(w/2))
                    y_loc = y + h/2 + random.randint(-int(h/2), int(h/2))

                    pyautogui.moveTo(x_loc, y_loc, 0.5 + random.random())
                    pyautogui.click()
                break
            else:
                x, y, w, h = rect[value]
                x_loc = x + w / 2 + random.randint(-int(w / 2), int(w / 2))
                y_loc = y + h / 2 + random.randint(-int(h / 2), int(h / 2))

                pyautogui.moveTo(x_loc, y_loc, 0.5 + random.random())
                pyautogui.click()
                break
        except:
            print(f'{attempt} attempt...')
            attempt += 1
            pause(3)

def check_template(template, threshold = conf['threshold'], img = None):
    check = len(position(template, threshold, img))
    return check

def show_matchTemplate(template, threshold = conf['threshold'], img = None):
    if img is None:
        img = screen_shot()

    rect = position(template, threshold, img)

    for (x, y, w, h) in rect:
        img = cv.rectangle(img, (x,y), (x+w,y+h), (0,255,255), 2)

    cv.imshow('img', img)

def pause(t):
    time.sleep(t + random.random())

class bomber:
    def login(self):
        click_template(template['connect_wallet'])
        pause(3)
        click_template(template['sign'])
        pause(3)
        click_template(template['hero_home'])
        click_template(template['all'])
        click_template(template['x'])
        click_template(template['treasure_hunt'])

    def resend(self):
        click_template(template['back2home'], 'all')
        pause(1)
        click_template(template['hero_home'], 'all')
        click_template(template['all'], 'all')
        click_template(template['x'], 'all')
        click_template(template['treasure_hunt'], 'all')

    def connection(self):
        click_template(template['ok'])
        pause(10)
        self.login()

if __name__ == "__main__":
    print(f'=====> The script to be used with 50% zoom')
    print(f'=====> Loaded "config.yaml"')

    # load imange template
    pyautogui.PAUSE = conf['interval']
    global template
    template = load_template()
    print(f'=====> Loaded template\n')

    bot = bomber()
    last = {'login' : 0, 'resend' : 0, 'connection' : 0}
    login_timeout, resend_timeout, connection_timeout = 0, 0, 0

    total_bot = check_template(template['connect_wallet']) + check_template(template['treasure_hunt']) + check_template(template['back2home']) + check_template(template['ok'])
    print(f'{total_bot} Windows...\n')

    while True:
        now = time.time()
        tnow = time.strftime("[%H:%M:%S]", time.gmtime(now))

        if now - last['login'] > login_timeout:
            print(f'{tnow}[LOGIN] -----')
            try:
                if check_template(template['connect_wallet']):
                    print(f'{tnow}[LOGIN] working...')
                    bot.login()
            except:
                print(f'{tnow}[LOGIN] button not found')

            last['login'] = now
            login_timeout = conf['login'] * 60 + random.randint(0, conf['random'] * 60)
            ntime = time.strftime("%M min %S sec", time.gmtime(login_timeout))
            print(f'{tnow}[LOGIN] check again in next {ntime}')

        if now - last['resend'] > resend_timeout:
            print(f'{tnow}[RESEND] -----')
            try:
                if check_template(template['back2home']):
                    print(f'{tnow}[RESEND] working...')
                    bot.resend()
            except:
                print(f'{tnow}[RESEND] button not found]')

            last['resend'] = now
            resend_timeout = conf['resend'] * 60 + random.randint(0, conf['random'] * 60)
            ntime = time.strftime("%M min %S sec", time.gmtime(resend_timeout))
            print(f'{tnow}[RESEND] check again in next {ntime}')

        if now - last['connection'] > connection_timeout:
            print(f'{tnow}[CONNECTION] -----')
            try:
                if check_template(template['ok']):
                    print(f'{tnow}[CONNECTION] working...')
                    bot.connection()
            except:
                print(f'{tnow}[CONNECTION] button not found')

            last['connection'] = now
            connection_timeout = conf['connection'] * 60 + random.randint(0, conf['random'] * 60)
            ntime = time.strftime("%M min %S sec", time.gmtime(connection_timeout))
            print(f'{tnow}[CONNECTION] check again in next {ntime}')

        pause(1)


