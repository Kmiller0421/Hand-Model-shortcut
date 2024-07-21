from AppOpener import open
import pyautogui

class Task:
    def __init__(self):
        None

    def preset_task(self, value):
        if value == 1:
              open("Google Chrome", match_closest=True)
        elif value == 2:
            open("Spotify", match_closest=True)
        elif value == 3:
            open("Steam", match_closest=True)
        elif value == 4:
            pyautogui.press('playpause')
        elif value == 5:
            pyautogui.press('prevtrack')
        elif value == 6:
            pyautogui.press('nexttrack')
        
