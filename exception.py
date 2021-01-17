import keyboard  # using module keyboard
import time

 #this code is for dealing with the client whilst the game is running.  We need the user to make a command
 #from : https://stackoverflow.com/questions/24072790/detect-key-press-in-python
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('a') or keyboard.is_pressed('b') or keyboard.is_pressed('c'):  # if key 'q' is pressed
            print('You Pressed A Key!')
            # finishing the loop
            time.sleep(0.1)
        else:
            pass
    except:
        break  # if user pressed a key other than the given key the loop will break