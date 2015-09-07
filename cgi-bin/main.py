
import random, sys, time, pygame, os
from pygame.locals import *
#import wifitools
import pickle
import sqlite3
import datetime
import medManager
import userManager

##TODO: change for PI
#os.environ["SDL_FBDEV"] = "/dev/fb1"
#os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
#os.environ["SDL_MOUSEDRV"] = "TSLIB"

FPS = 30
WINDOWWIDTH = 320
WINDOWHEIGHT = 240
FLASHSPEED = 500 # in milliseconds
FLASHDELAY = 200 # in milliseconds
BUTTONSIZE = 80
BUTTONGAPSIZE = 10

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
DARK         = ( 18,  40,  13)
MID          = ( 47,  82,  20)
LIGHT        = ( 77, 129,  41)
DARKGRAY     = ( 64,  64,  64)
bgColor = BLACK

HEADER = 30
BORDER = 10
# status bar
RECTSTATUS = pygame.Rect(0, 0, WINDOWWIDTH, HEADER)
IMAGE_WIFI0 = pygame.image.load("images/wifi0.BMP")
IMAGE_WIFI1 = pygame.image.load("images/wifi1.BMP")
IMAGE_WIFI2 = pygame.image.load("images/wifi2.BMP")
IMAGE_WIFI3 = pygame.image.load("images/wifi3.BMP")
IMAGE_WIFI4 = pygame.image.load("images/wifi4.BMP")
IMAGE_ALARM = pygame.image.load("images/alarm.BMP")
IMAGE_NOALARM = pygame.image.load("images/noalarm.BMP")
IMAGE_ALERT = pygame.image.load("images/alert.BMP")
IMAGE_WARNING = pygame.image.load("images/warning.BMP")
IMAGE_LOCK = pygame.image.load("images/lock.BMP")
IMAGE_TIMER = pygame.image.load("images/timer.BMP")

IMAGE_GEARS = pygame.image.load("images/gears.png")
IMAGE_BACK = pygame.image.load("images/back.png")
IMAGE_PILL = pygame.image.load("images/pill.png")
IMAGE_LOAD = pygame.image.load("images/load.png")
IMAGE_PLUS = pygame.image.load("images/plus.png")
IMAGE_FACE = pygame.image.load("images/face.png")
IMAGE_POWER = pygame.image.load("images/power.png")
IMAGE_BRIGHTNESS = pygame.image.load("images/brightness.png")
IMAGE_WIFI_SETTINGS = pygame.image.load("images/wifi_settings.png")

# main menu
RECT_BG = pygame.Rect(0, HEADER, 210, 320)
BUTTON_1  = pygame.Rect(10, HEADER+BORDER, 90, 90)
BUTTON_2  = pygame.Rect(110, HEADER+BORDER, 90, 90)
BUTTON_3  = pygame.Rect(210, HEADER+BORDER, 90, 90)
BUTTON_4  = pygame.Rect(10, HEADER+BORDER+100, 90, 90)
BUTTON_5  = pygame.Rect(110, HEADER+BORDER+100, 90, 90)
BUTTON_6 = pygame.Rect(210, HEADER+BORDER+100, 90, 90)

LIST_1  = pygame.Rect(10, HEADER+BORDER, 190, 40)
LIST_2  = pygame.Rect(10, HEADER+BORDER+50, 190, 40)
LIST_3  = pygame.Rect(10, HEADER+BORDER+100, 190, 40)
LIST_4  = pygame.Rect(10, HEADER+BORDER+150, 190, 40)
LIST_UP = pygame.Rect(210, HEADER+BORDER, 90, 40)
LIST_DN = pygame.Rect(210, HEADER+BORDER+50, 90, 40)


ACTION_DISPENSE = 1
ACTION_STATUS = 2
ACTION_LOAD = 3
ACTION_SETTINGS = 4
ACTION_BACK = 5
ACTION_WIFI = 6
ACTION_ADDUSER = 7
ACTION_USER1 = 8
ACTION_USER2 = 9
ACTION_USER3 = 10
ACTION_USER4 = 11
ACTION_SHUTDOWN = 12
ACTION_BRIGHTNESS = 13
ACTION_LIST_1 = 14
ACTION_LIST_2 = 15
ACTION_LIST_3 = 16
ACTION_LIST_4 = 17
ACTION_LIST_UP = 18
ACTION_LIST_DN = 19
ACTION_VENDING = 20
ACTION_HOME = 21
ACTION_MANAGE = 22

MENU_MAIN = 0
MENU_SETTINGS = 1
MENU_WIFI = 2
MENU_USERS = 3
MENU_ADDUSER = 4
MENU_DISPENSE = 5
MENU_LOAD = 6
MENU_LOADING = 7
MENU_SHUTDOWN = 8
MENU_BRIGHTNESS = 9
MENU_VENDING = 10
MENU_MANAGE = 11

##TODO: change for PI
wifipercent = 100 #int(wifitools.get_main_percent())

users = ['Joe', 'Amy', 'Dad', 'Mom']
pickle.dump(users, open("data/users.pkl","wb"))
users = pickle.load(open("data/users.pkl","rb"))

#global vars
list_position = 0
list_next = 0
list_id = 0
current_user = 0
pill_id = 0
pill_name = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    current_menu = MENU_MAIN

    global list_position
    global list_next
    global list_id
    global current_user
    global pill_id
    global pill_name

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	##TODO: change for PI
    #pygame.mouse.set_visible(0)

    IMAGE_GEARS = pygame.image.load("images/gears.png").convert_alpha()
    IMAGE_BACK = pygame.image.load("images/back.png").convert_alpha()
    IMAGE_PILL = pygame.image.load("images/pill.png").convert_alpha()
    IMAGE_LOAD = pygame.image.load("images/load.png").convert_alpha()
    IMAGE_PLUS = pygame.image.load("images/plus.png").convert_alpha()
    IMAGE_FACE = pygame.image.load("images/face.png").convert_alpha()
    IMAGE_POWER = pygame.image.load("images/power.png").convert_alpha()
    IMAGE_BRIGHTNESS = pygame.image.load("images/brightness.png").convert_alpha()
    IMAGE_WIFI_SETTINGS = pygame.image.load("images/wifi_settings.png").convert_alpha()
	


    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False
    updateDisplay = True


    while True: # main game loop
        clickedButton = None # button that was clicked
        if updateDisplay:
            DISPLAYSURF.fill(bgColor)
            drawStatusBar()
            if current_menu == MENU_MAIN:
               drawMainMenu()
            elif current_menu == MENU_SETTINGS:
               drawSettingsMenu()
            elif current_menu == MENU_WIFI:
               drawWIFIMenu()
            elif current_menu == MENU_USERS:
               drawUsersMenu()
            elif current_menu == MENU_DISPENSE:
               drawDispenseMenu()
            elif current_menu == MENU_ADDUSER:
               drawAddUserMenu()
            elif current_menu == MENU_LOAD:
               drawLoadMenu()
            elif current_menu == MENU_LOADING:
               drawLoadingMenu()
            elif current_menu == MENU_SHUTDOWN:
               drawShutdownMenu()
            elif current_menu == MENU_BRIGHTNESS:
               drawBrightnessMenu()
            elif current_menu == MENU_VENDING:
               drawVendingMenu()
            elif current_menu == MENU_MANAGE:
               drawManageMenu()
            updateDisplay = False

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey, current_menu)


        # wait for the player to enter buttons
        if clickedButton:
            if clickedButton == ACTION_SETTINGS:
                current_menu = MENU_SETTINGS
            elif clickedButton == ACTION_WIFI:
                current_menu = MENU_WIFI
            elif clickedButton == ACTION_HOME:
                current_menu = MENU_MAIN
            elif clickedButton == ACTION_BRIGHTNESS:
                current_menu = MENU_BRIGHTNESS
            elif clickedButton == ACTION_LOAD:
                current_menu = MENU_LOAD
            elif clickedButton == ACTION_DISPENSE:
                current_menu = MENU_USERS
            elif clickedButton == ACTION_SHUTDOWN:
                current_menu = MENU_SHUTDOWN
            elif clickedButton == ACTION_ADDUSER:
                current_menu = MENU_ADDUSER
            elif clickedButton == ACTION_MANAGE:
                current_menu = MENU_MANAGE
            elif clickedButton == ACTION_USER1:
                current_menu = MENU_DISPENSE
                current_user = users[0]
            elif clickedButton == ACTION_USER2:
                current_menu = MENU_DISPENSE
                current_user = users[1]
            elif clickedButton == ACTION_USER3:
                current_menu = MENU_DISPENSE
                current_user = users[2]
            elif clickedButton == ACTION_USER4:
                current_menu = MENU_DISPENSE
                current_user = users[3]
            elif clickedButton == ACTION_LIST_1:
                if(list_position < list_next):
                    list_id = list_position
                    if(current_menu == MENU_DISPENSE):
                        current_menu = MENU_VENDING
                    elif(current_menu == MENU_LOAD):
                        current_menu = MENU_LOADING
            elif clickedButton == ACTION_LIST_2:
                if(list_position+1 < list_next):
                    list_id = list_position+1
                    if(current_menu == MENU_DISPENSE):
                        current_menu = MENU_VENDING
                    elif(current_menu == MENU_LOAD):
                        current_menu = MENU_LOADING
            elif clickedButton == ACTION_LIST_3:
                if(list_position+2 < list_next):
                    list_id = list_position+2
                    if(current_menu == MENU_DISPENSE):
                        current_menu = MENU_VENDING
                    elif(current_menu == MENU_LOAD):
                        current_menu = MENU_LOADING
            elif clickedButton == ACTION_LIST_4:
                if(list_position+3 < list_next):
                    list_id = list_position+3
                    if(current_menu == MENU_DISPENSE):
                        current_menu = MENU_VENDING
                    elif(current_menu == MENU_LOAD):
                        current_menu = MENU_LOADING
            elif clickedButton == ACTION_LIST_DN:
                if(list_next > 4):
                    list_position = list_position + 4
            elif clickedButton == ACTION_LIST_UP:
                if(list_position > 0):
                    list_position = list_position - 4
            elif clickedButton == ACTION_BACK:
                if current_menu == MENU_WIFI:
                    current_menu = MENU_SETTINGS
                elif current_menu == MENU_SETTINGS:
                    current_menu = MENU_MAIN
                elif current_menu == MENU_USERS:
                    current_menu = MENU_MAIN
                elif current_menu == MENU_DISPENSE:
                    current_menu = MENU_USERS
                elif current_menu == MENU_ADDUSER:
                    current_menu = MENU_USERS
                elif current_menu == MENU_LOAD:
                    current_menu = MENU_MAIN
                elif current_menu == MENU_SHUTDOWN:
                    current_menu = MENU_MAIN
                elif current_menu == MENU_BRIGHTNESS:
                    current_menu = MENU_SETTINGS
                elif current_menu == MENU_VENDING:
                    current_menu = MENU_DISPENSE
                elif current_menu == MENU_LOADING:
                    current_menu = MENU_LOAD
                elif current_menu == MENU_MANAGE:
                    current_menu = MENU_MAIN
            updateDisplay = True

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def getButtonClicked(x, y, current_menu):
    global list_id
    global list_position
    global list_next
    global pill_id

    if current_menu == MENU_MAIN:
        if BUTTON_1.collidepoint( (x, y) ):#dispense
       	    return ACTION_DISPENSE
        elif BUTTON_2.collidepoint( (x, y) ):#status
            return ACTION_LOAD
        elif BUTTON_3.collidepoint( (x, y) ):
            return ACTION_STATUS
        elif BUTTON_4.collidepoint( (x, y) ):
            return ACTION_MANAGE
        elif BUTTON_5.collidepoint( (x, y) ):#shutdown
            return ACTION_SHUTDOWN
        elif BUTTON_6.collidepoint( (x, y) ):#settings
            return ACTION_SETTINGS
    elif current_menu == MENU_SETTINGS:
        if BUTTON_6.collidepoint( (x, y) ):#back
            return ACTION_BACK
        elif BUTTON_5.collidepoint( (x, y) ):#wifi
            return ACTION_WIFI
        elif BUTTON_4.collidepoint( (x, y) ):#wifi
            return ACTION_BRIGHTNESS
    elif current_menu == MENU_WIFI:
        if BUTTON_6.collidepoint( (x, y) ):#back
            return ACTION_BACK
    elif current_menu == MENU_VENDING:
        if BUTTON_6.collidepoint( (x, y) ):#back
            pill_id = 0
            pill_name = ""
            return ACTION_BACK
        if BUTTON_5.collidepoint( (x, y) ):#back
            x = medManager.getMedX(pill_id)
            y = medManager.getMedY(pill_id)
            print(pill_id, x,y)
            #TODO: do vending here
            medManager.removeInventory(x,y)
            list_id = 0
            list_next = 0
            list_position = 0
            pill_id = 0
            pill_name = ""
            return ACTION_HOME
    elif current_menu == MENU_LOADING:
        if BUTTON_6.collidepoint( (x, y) ):#back
            pill_id = 0
            pill_name = ""
            return ACTION_BACK
        if BUTTON_5.collidepoint( (x, y) ):#back
            print(pill_id, x,y)
            #TODO: do vending here
            x = medManager.getFreeSpaceX()
            y = medManager.getFreeSpaceY()
            d = datetime.date(2016, 11, 23)
            medManager.addInventory(x, y, pill_id, d)
            print("inserted into: ", x, y)
            #return ACTION_HOME
    elif current_menu == MENU_BRIGHTNESS:
        if BUTTON_6.collidepoint( (x, y) ):#back
            return ACTION_BACK
    elif current_menu == MENU_DISPENSE:
        if BUTTON_6.collidepoint( (x, y) ):#back
            list_id = 0
            list_next = 0
            list_position = 0
            return ACTION_BACK
        if LIST_UP.collidepoint( (x, y) ):#back
            return ACTION_LIST_UP
        if LIST_DN.collidepoint( (x, y) ):#back
            return ACTION_LIST_DN
        if LIST_1.collidepoint( (x, y) ):#back
            return ACTION_LIST_1
        if LIST_2.collidepoint( (x, y) ):#back
            return ACTION_LIST_2
        if LIST_3.collidepoint( (x, y) ):#back
            return ACTION_LIST_3
        if LIST_4.collidepoint( (x, y) ):#back
            return ACTION_LIST_4
    elif current_menu == MENU_ADDUSER:
        if BUTTON_6.collidepoint( (x, y) ):#back
            return ACTION_BACK
    elif current_menu == MENU_MANAGE:
        if BUTTON_6.collidepoint( (x, y) ):#back
            list_id = 0
            list_next = 0
            list_position = 0
            return ACTION_BACK
        if LIST_UP.collidepoint( (x, y) ):#back
            return ACTION_LIST_UP
        if LIST_DN.collidepoint( (x, y) ):#back
            return ACTION_LIST_DN
        if LIST_1.collidepoint( (x, y) ):#back
            return ACTION_LIST_1
        if LIST_2.collidepoint( (x, y) ):#back
            return ACTION_LIST_2
        if LIST_3.collidepoint( (x, y) ):#back
            return ACTION_LIST_3
        if LIST_4.collidepoint( (x, y) ):#back
            return ACTION_LIST_4
    elif current_menu == MENU_LOAD:
        if BUTTON_6.collidepoint( (x, y) ):#back
            list_id = 0
            list_next = 0
            list_position = 0
            return ACTION_BACK
        if LIST_UP.collidepoint( (x, y) ):#back
            return ACTION_LIST_UP
        if LIST_DN.collidepoint( (x, y) ):#back
            return ACTION_LIST_DN
        if LIST_1.collidepoint( (x, y) ):#back
            return ACTION_LIST_1
        if LIST_2.collidepoint( (x, y) ):#back
            return ACTION_LIST_2
        if LIST_3.collidepoint( (x, y) ):#back
            return ACTION_LIST_3
        if LIST_4.collidepoint( (x, y) ):#back
            return ACTION_LIST_4
    elif current_menu == MENU_SHUTDOWN:
        if BUTTON_5.collidepoint( (x, y) ):#back
            os.system("sudo shutdown -h now") #shut down the system
        if BUTTON_6.collidepoint( (x, y) ):#back
            return ACTION_BACK
    elif current_menu == MENU_USERS:
        if BUTTON_6.collidepoint( (x, y) ):#back
            return ACTION_BACK
        if BUTTON_3.collidepoint( (x, y) ):#back
            return ACTION_ADDUSER
        if BUTTON_1.collidepoint( (x, y) ):#back
            return ACTION_USER1
        if BUTTON_2.collidepoint( (x, y) ):#back
            return ACTION_USER2
        if BUTTON_4.collidepoint( (x, y) ):#back
            return ACTION_USER3
        if BUTTON_5.collidepoint( (x, y) ):#back
            return ACTION_USER4

    return None

def drawStatusBar():
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, RECTSTATUS)
    if wifipercent == 0:
        DISPLAYSURF.blit(IMAGE_WIFI0, (0,0))
    elif wifipercent <= 20:
        DISPLAYSURF.blit(IMAGE_WIFI1, (0,0))
    elif wifipercent <= 40:
        DISPLAYSURF.blit(IMAGE_WIFI2, (0,0))
    elif wifipercent <= 60:
        DISPLAYSURF.blit(IMAGE_WIFI3, (0,0))
    elif wifipercent <= 80:
        DISPLAYSURF.blit(IMAGE_WIFI4, (0,0))
    else:
        DISPLAYSURF.blit(IMAGE_WIFI0, (0,0))

    DISPLAYSURF.blit(IMAGE_ALARM, (50,0))
    DISPLAYSURF.blit(IMAGE_NOALARM, (80,0))
    DISPLAYSURF.blit(IMAGE_ALERT, (110,0))
    DISPLAYSURF.blit(IMAGE_WARNING, (140,0))
    DISPLAYSURF.blit(IMAGE_LOCK, (170,0))
    DISPLAYSURF.blit(IMAGE_TIMER, (200,0))

def drawUsersMenu():
    i=0
    for user in users:
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(user, 1, BLACK)
        if i == 0:
            pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_1)
            DISPLAYSURF.blit(IMAGE_FACE, (25,HEADER+BORDER+10))
            DISPLAYSURF.blit(label, (15, HEADER+BORDER+70))
        elif i == 1:
            pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_2)
            DISPLAYSURF.blit(IMAGE_FACE, (125,HEADER+BORDER+10))
            DISPLAYSURF.blit(label, (115, HEADER+BORDER+70))
        elif i == 2:
            pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_4)
            DISPLAYSURF.blit(IMAGE_FACE, (25,HEADER+BORDER+110))
            DISPLAYSURF.blit(label, (15, HEADER+BORDER+170))
        elif i == 3:
            pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_5)
            DISPLAYSURF.blit(IMAGE_FACE, (125,HEADER+BORDER+110))
            DISPLAYSURF.blit(label, (115, HEADER+BORDER+170))

        i=i+1
        
    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_3)
    DISPLAYSURF.blit(IMAGE_PLUS, (225,HEADER+BORDER+10))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("ADD User", 1, BLACK)
    DISPLAYSURF.blit(label, (220, HEADER+BORDER+70))
    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))

def drawSettingsMenu():

    pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_4)
    DISPLAYSURF.blit(IMAGE_BRIGHTNESS, (25,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Brightness", 1, BLACK)
    DISPLAYSURF.blit(label, (11, 210))

    pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_5)
    DISPLAYSURF.blit(IMAGE_WIFI_SETTINGS, (125,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("WIFI", 1, BLACK)
    DISPLAYSURF.blit(label, (137, 210))

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))

def drawWIFIMenu():
    myfont = pygame.font.SysFont("monospace", 15)
	##TODO: change for PI
    ip = 0#wifitools.get_connection_info('ip')
    mask = 0#wifitools.get_connection_info('mask')
    brd = 0#wifitools.get_connection_info('broadcast')
    mac = 0#wifitools.get_connection_info('mac')
    label = myfont.render(' IP Address:  '+ip, 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+20))
    label = myfont.render('  Broadcast:  '+brd, 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+35))
    label = myfont.render('   Net Mask:  '+mask, 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+50))
    label = myfont.render('MAC Address:  '+mac, 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+65))

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))

def drawBrightnessMenu():
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render('Adjust Screen Brightness', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+20))

    SLIDER_OUT = pygame.Rect(5, HEADER+BORDER+40, 200, 30)
    pygame.draw.rect(DISPLAYSURF, MID,   SLIDER_OUT)

    brightness = 160
    #print brightness
    SLIDER_VAL = pygame.Rect(10, HEADER+BORDER+45, brightness, 20)
    pygame.draw.rect(DISPLAYSURF, LIGHT,   SLIDER_VAL)

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))

def drawDispenseMenu():

    global list_position
    global list_next

    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_1)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_2)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_3)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_4)

    myfont = pygame.font.SysFont("monospace", 15)
    i=0
    for med in medManager.getInventory(0):
        if(i >= list_position):
            label = myfont.render(med[1], 1, BLACK)
            DISPLAYSURF.blit(label, (15, HEADER+20+50*(i-list_position)))
            print(med[1])
        i=i+1
    list_next = i - list_position

    if(list_position > 0):
        pygame.draw.rect(DISPLAYSURF, MID,    LIST_UP)
    else:
        pygame.draw.rect(DISPLAYSURF, DARK,    LIST_UP)
    label = myfont.render("Last", 1, BLACK)
    DISPLAYSURF.blit(label, (215, HEADER+20))

    if(list_next > 4):
        pygame.draw.rect(DISPLAYSURF, MID,    LIST_DN)
    else:
        pygame.draw.rect(DISPLAYSURF, DARK,    LIST_DN)
    label = myfont.render("Next", 1, BLACK)
    DISPLAYSURF.blit(label, (215, HEADER+70))
		

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))

def drawAddUserMenu():
    myfont = pygame.font.SysFont("monospace", 15)
    i = 0
    for letter in ['q','w','e','r','t','y','u','i','o','p']:
        button = pygame.Rect(10+30*i, HEADER+75, 25, 30)
        pygame.draw.rect(DISPLAYSURF, MID,   button)
        label = myfont.render(letter, 1, WHITE)
        DISPLAYSURF.blit(label, (20+30*i, HEADER+80))
        i = i + 1
    i = 0
    for letter in ['a','s','d','f','g','h','j','k','l']:
        button = pygame.Rect(25+30*i, HEADER+110, 25, 30)
        pygame.draw.rect(DISPLAYSURF, MID,   button)
        label = myfont.render(letter, 1, WHITE)
        DISPLAYSURF.blit(label, (35+30*i, HEADER+115))
        i = i + 1
    i = 0
    for letter in ['^','z','x','c','v','b','n','m',',','.']:
        button = pygame.Rect(10+30*i, HEADER+145, 25, 30)
        pygame.draw.rect(DISPLAYSURF, MID,   button)
        label = myfont.render(letter, 1, WHITE)
        DISPLAYSURF.blit(label, (20+30*i, HEADER+150))
        i = i + 1
    i = 0
    for letter in ['space', 'del', 'done']:
        button = pygame.Rect(25+90*i, HEADER+180, 85, 30)
        pygame.draw.rect(DISPLAYSURF, MID,   button)
        label = myfont.render(letter, 1, WHITE)
        DISPLAYSURF.blit(label, (35+90*i, HEADER+185))
        i = i + 1



    #pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    #DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    #myfont = pygame.font.SysFont("monospace", 15)
    #label = myfont.render("Back", 1, BLACK)
    #DISPLAYSURF.blit(label, (237, 210))

def drawShutdownMenu():
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render('Push the \'Turn Off\'', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+20))
    label = myfont.render('button one more time', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+35))
    label = myfont.render('to shut down machine', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+50))

    pygame.draw.rect(DISPLAYSURF, LIGHT,    BUTTON_5)
    DISPLAYSURF.blit(IMAGE_POWER, (125,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Turn Off", 1, BLACK)
    DISPLAYSURF.blit(label, (117, 210))

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))

def drawVendingMenu():
    global list_id
    global pill_id
    global pill_name
    i=0
    for med in medManager.getInventory(0):
        if(i == list_id):
            pill_name = med[1]
            pill_id = med[0]
        i=i+1

    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render('Push the \'Dispense\'', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+20))
    label = myfont.render('button one more time', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+35))
    label = myfont.render('to dispense one pill of:', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+50))
    label = myfont.render(pill_name, 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+75))

    pygame.draw.rect(DISPLAYSURF, LIGHT,    BUTTON_5)
    DISPLAYSURF.blit(IMAGE_PILL, (125,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Dispense", 1, BLACK)
    DISPLAYSURF.blit(label, (117, 210))

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))


def drawLoadMenu():

    global list_position
    global list_next

    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_1)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_2)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_3)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_4)

    myfont = pygame.font.SysFont("monospace", 15)
    i=0
    for med in medManager.getInventory(1):
        if(i >= list_position):
            label = myfont.render(med[1], 1, BLACK)
            DISPLAYSURF.blit(label, (15, HEADER+20+50*(i-list_position)))
            print(med[1])
        i=i+1
    list_next = i - list_position

    if(list_position > 0):
        pygame.draw.rect(DISPLAYSURF, MID,    LIST_UP)
    else:
        pygame.draw.rect(DISPLAYSURF, DARK,    LIST_UP)
    label = myfont.render("Last", 1, BLACK)
    DISPLAYSURF.blit(label, (215, HEADER+20))

    if(list_next > 4):
        pygame.draw.rect(DISPLAYSURF, MID,    LIST_DN)
    else:
        pygame.draw.rect(DISPLAYSURF, DARK,    LIST_DN)
    label = myfont.render("Next", 1, BLACK)
    DISPLAYSURF.blit(label, (215, HEADER+70))
		

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))


def drawLoadingMenu():
    global list_id
    global pill_id
    global pill_name
    i=0
    for med in medManager.getInventory(1):
        if(i == list_id):
            pill_name = med[1]
            pill_id = med[0]
        i=i+1

    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render('Push the \'Load\'', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+20))
    label = myfont.render('once for each pill you', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+35))
    label = myfont.render('want to load of:', 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+50))
    label = myfont.render(pill_name, 1, WHITE)
    DISPLAYSURF.blit(label, (10, HEADER+75))

    pygame.draw.rect(DISPLAYSURF, LIGHT,    BUTTON_5)
    DISPLAYSURF.blit(IMAGE_PILL, (125,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Load", 1, BLACK)
    DISPLAYSURF.blit(label, (117, 210))

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))
    
def drawManageMenu():

    global list_position
    global list_next

    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_1)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_2)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_3)
    pygame.draw.rect(DISPLAYSURF, LIGHT,    LIST_4)

    myfont = pygame.font.SysFont("monospace", 15)
    i=0
    for med in medManager.getInventory(1):
        if(i >= list_position):
            label = myfont.render(med[1], 1, BLACK)
            DISPLAYSURF.blit(label, (15, HEADER+20+50*(i-list_position)))
            print(med[1])
        i=i+1
    list_next = i - list_position

    if(list_position > 0):
        pygame.draw.rect(DISPLAYSURF, MID,    LIST_UP)
    else:
        pygame.draw.rect(DISPLAYSURF, DARK,    LIST_UP)
    label = myfont.render("Last", 1, BLACK)
    DISPLAYSURF.blit(label, (215, HEADER+20))

    if(list_next > 4):
        pygame.draw.rect(DISPLAYSURF, MID,    LIST_DN)
    else:
        pygame.draw.rect(DISPLAYSURF, DARK,    LIST_DN)
    label = myfont.render("Next", 1, BLACK)
    DISPLAYSURF.blit(label, (215, HEADER+70))
		

    pygame.draw.rect(DISPLAYSURF, MID,   BUTTON_6)
    DISPLAYSURF.blit(IMAGE_BACK, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Back", 1, BLACK)
    DISPLAYSURF.blit(label, (237, 210))


def drawMainMenu():
    pygame.draw.rect(DISPLAYSURF, LIGHT,   BUTTON_1) #dispense
    DISPLAYSURF.blit(IMAGE_PILL, (25,HEADER+BORDER+10))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Dispense", 1, BLACK)
    DISPLAYSURF.blit(label, (19, 110))

    pygame.draw.rect(DISPLAYSURF, LIGHT,    BUTTON_2) #load
    DISPLAYSURF.blit(IMAGE_LOAD, (125,HEADER+BORDER+10))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Load", 1, BLACK)
    DISPLAYSURF.blit(label, (137, 110))

    pygame.draw.rect(DISPLAYSURF, LIGHT,  BUTTON_3) #status

    pygame.draw.rect(DISPLAYSURF, LIGHT,    BUTTON_4)
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Manage", 1, BLACK)
    DISPLAYSURF.blit(label, (22, 210))

    pygame.draw.rect(DISPLAYSURF, MID,    BUTTON_5)#power
    DISPLAYSURF.blit(IMAGE_POWER, (125,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Turn Off", 1, BLACK)
    DISPLAYSURF.blit(label, (117, 210))

    pygame.draw.rect(DISPLAYSURF, LIGHT,  BUTTON_6)#settings
    DISPLAYSURF.blit(IMAGE_GEARS, (225,HEADER+BORDER+110))
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Settings", 1, BLACK)
    DISPLAYSURF.blit(label, (217, 210))






if __name__ == '__main__':
    main()
