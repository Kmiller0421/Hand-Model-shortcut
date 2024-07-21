import cv2
from HandModel import Hand  # Importing the class hand

def main():
    webcam = cv2.VideoCapture(0)
    hm = Hand()

    # Webcam input validation
    if webcam.isOpened():
        print("Successfully connected to webcam.")
        hm.hand_initialization(webcam)
    else:
        print("Error! We could not access webcam.")
        print("Please make sure you have built in webcam or external webcam is plugged in.")
        exit()

    webcam.release()

if __name__ == "__main__":
    main()