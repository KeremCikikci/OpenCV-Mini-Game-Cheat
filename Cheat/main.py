import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import keyboard
import time

""" Do not change the values ​​of lowercase variables without fully understanding the code """


# Show selected tiles in a window
SHOWTILES = True

# Time between two games in seconds
WAITINGTIME = 40

# Door Position [left corner position, top corner postion, right corner position, bottom corner position]
DOOR = [[612, 477], [639, 465], [660, 480], [640, 493]]

# Use key button position [x, y]
KEYBUTTON = [1335, 657]

# Tile postitions [[left corner position, top corner postion, right corner position, bottom corner position], ...]
TILES = [[[452, 559], [480, 544], [510, 558], [480, 572]],
         [[480, 542], [512, 527], [540, 540], [512, 557]],  
         [[515, 525], [545, 510], [573, 526], [545, 540]]]

# Key position [left corner position, top corner postion, right corner position, bottom corner position]
KEY = [575, 500]

# Chair postion [left corner position, top corner postion, right corner position, bottom corner position]
CHAIR = [603, 486]

# Define kernel size  
kernel = np.ones((7,7),np.uint8)

# Lower bound and upper bound for Yellow color
lower_bound = np.array([80, 150, 80])   
upper_bound = np.array([150, 255, 255])

# Create boxes for each tile
boxes = []

# Minimum number of white pixels when coin is on the tile
minWhitePixels_tiles = 1000
minWhitePixels_door = 2000

def goChair():
    while True:
        # Door 
        _door = ImageGrab.grab(bbox=(DOOR[0][0], DOOR[0][1], DOOR[3][0], DOOR[3][1])) #x, y, w, h
        img_np = np.array(_door)

        # Resize Door
        resized = cv2.resize(img_np, (100, 100), interpolation = cv2.INTER_AREA)

        # Covert to HSV
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        # Find the colors within the boundaries
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Remove unnecessary noise from mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Count white pixels
        n_white_pix = np.sum(mask == 255)

        pyautogui.moveTo(CHAIR[0], CHAIR[1])
        pyautogui.click()
        time.sleep(2)
        pyautogui.click()

        if n_white_pix > minWhitePixels_door:
            break
        

def clickOnKey():
    # Key
    pyautogui.moveTo(KEY[0], KEY[1])
    pyautogui.click()
    pyautogui.moveTo(KEYBUTTON[0], KEYBUTTON[1])

def playIt():
    while True:
        # First Tile
        tile1 = ImageGrab.grab(bbox=(boxes[0][0][0], boxes[0][0][1], boxes[0][3][0], boxes[0][3][1])) #x, y, w, h
        img_np1 = np.array(tile1)

        # Second Tile
        tile2 = ImageGrab.grab(bbox=(boxes[1][0][0], boxes[1][0][1], boxes[1][3][0], boxes[1][3][1])) #x, y, w, h
        img_np2 = np.array(tile2)

        # Third Tile
        tile3 = ImageGrab.grab(bbox=(boxes[2][0][0], boxes[2][0][1], boxes[2][3][0], boxes[2][3][1])) #x, y, w, h
        img_np3 = np.array(tile3)

        # Resize Tiles
        resized1 = cv2.resize(img_np1, (100, 100), interpolation = cv2.INTER_AREA)
        resized2 = cv2.resize(img_np2, (100, 100), interpolation = cv2.INTER_AREA)
        resized3 = cv2.resize(img_np3, (100, 100), interpolation = cv2.INTER_AREA)

        # Stitch the Tiles horizontally
        numpy_vertical_img = np.hstack((resized1, resized2, resized3))

        # Covert to HSV
        hsv1 = cv2.cvtColor(resized1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(resized2, cv2.COLOR_BGR2HSV)
        hsv3 = cv2.cvtColor(resized3, cv2.COLOR_BGR2HSV)

        # Stitch the Tiles horizontally
        numpy_vertical = np.hstack((hsv1, hsv2, hsv3))
        
        # Find the colors within the boundaries
        mask = cv2.inRange(numpy_vertical, lower_bound, upper_bound)
        mask1 = cv2.inRange(hsv1, lower_bound, upper_bound)
        mask2 = cv2.inRange(hsv2, lower_bound, upper_bound)
        mask3 = cv2.inRange(hsv3, lower_bound, upper_bound)

        
        if SHOWTILES:
            # Remove unnecessary noise from mask
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)
            mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
            mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
            mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)
            mask3 = cv2.morphologyEx(mask3, cv2.MORPH_CLOSE, kernel)
            mask3 = cv2.morphologyEx(mask3, cv2.MORPH_OPEN, kernel)

            # Apply the mask on the image
            segmented_img = cv2.bitwise_and(numpy_vertical_img, numpy_vertical_img, mask=mask)
        
        # Count white pixels
        n_white_pix1 = np.sum(mask1 == 255)
        n_white_pix2 = np.sum(mask2 == 255)
        n_white_pix3 = np.sum(mask3 == 255)

        print(str(n_white_pix1) + " | " + str(n_white_pix2) + " | " + str(n_white_pix3) + " | ")
        
        if n_white_pix1 > minWhitePixels_tiles and n_white_pix2 > minWhitePixels_tiles and n_white_pix3 > minWhitePixels_tiles:
            pyautogui.click()
            print("3 Coins were detected")
            break

        if SHOWTILES:
            cv2.imshow("Tiles", segmented_img)
        
        if keyboard.is_pressed('q'):
            break
        if cv2.waitKey(1) & 0Xff == ord('q'):
            break

topLeftCorner = [int((DOOR[0][0] + DOOR[1][0]) / 2), int((DOOR[0][1] + DOOR[1][1]) / 2)]     # x, y
topRightCorner = [int((DOOR[1][0] + DOOR[2][0]) / 2), int((DOOR[1][1] + DOOR[2][1]) / 2)]    # x, y
bottomLeftCorner = [int((DOOR[0][0] + DOOR[3][0]) / 2), int((DOOR[0][1] + DOOR[3][1]) / 2)]  # x, y
bottomRightCorner = [int((DOOR[3][0] + DOOR[2][0]) / 2), int((DOOR[3][1] + DOOR[2][1]) / 2)] # x, y
doorBox = [topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner]

for x in range(len(TILES)):
    topLeftCorner = [int((TILES[x][0][0] + TILES[x][1][0]) / 2), int((TILES[x][0][1] + TILES[x][1][1]) / 2)]     # x, y
    topRightCorner = [int((TILES[x][1][0] + TILES[x][2][0]) / 2), int((TILES[x][1][1] + TILES[x][2][1]) / 2)]    # x, y
    bottomLeftCorner = [int((TILES[x][0][0] + TILES[x][3][0]) / 2), int((TILES[x][0][1] + TILES[x][3][1]) / 2)]  # x, y
    bottomRightCorner = [int((TILES[x][3][0] + TILES[x][2][0]) / 2), int((TILES[x][3][1] + TILES[x][2][1]) / 2)] # x, y
    boxes.append([topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner])

while True:
    # Sit on the chair
    goChair()

    # Click on the key
    clickOnKey()

    # Play the game
    playIt()
    time.sleep(WAITINGTIME)
   
