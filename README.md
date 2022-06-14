# OpenCV-Mini-Game-Cheat

Thanks to this program, a mini game, which is a part of an online game where people spend hours, can be played without sitting in front of the computer.

# Packets

These Python libraries are used in the code:

-pynput

-opencv

-numpy

-PIL

-pyautogui

-keyboard

-time


# Folder Content

1-find_tile.py: The positions of the tiles, key, chair and door are detected.

2-main.py: goChair, clickOnKey, playIt functions

# The Game

When the player sits on the chair, the door closes and the game begins. Arriving on the playing field the coins start to move randomly left and right. After that, the player tries to use the key in order to stop all the coins while they are on the middle tiles. If the player manages to use the key at the right time, he gets 1 game currency for every 15 points.

![miniGame](https://user-images.githubusercontent.com/98697826/173625883-5faf8f95-59e8-4629-a980-dd421a6c74ea.png)

# How it works?

The biggest rectangle, which fits in the tiles, are calculated. Secondly, screenshots of 3 rectangles are converted to HSV format. So that coins can be more easily distinguished from tiles. Moreover coins are deleted from the tile captures. Then the white pixels formed by deleting the coins are counted and if the white pixels are more than the specified number in all tile images, the mouse cursor is directed to the key and used. This process is repeated in a loop.


Uploading video.mp4…


