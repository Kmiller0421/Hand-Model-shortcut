import cv2
import mediapipe as mp

import math

from google.protobuf.json_format import MessageToDict

from AppOpener import open
import pyautogui
import time

class Hand:
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=True, 
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=2
        )
        self.hand = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.MIDDLE_FINGER_TIP = mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP.value
        self.INDEX_FINGER_TIP = mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP.value
        self.RING_FINGER_TIP = mp.solutions.hands.HandLandmark.RING_FINGER_TIP.value
        self.PINKY_FINGER_TIP = mp.solutions.hands.HandLandmark.PINKY_TIP.value
        self.THUMB_TIP = mp.solutions.hands.HandLandmark.THUMB_TIP.value
    
    def hand_initialization(self, webcam):
        with self.mp_hands as hands:
            while webcam.isOpened():
                success, img = webcam.read()
                if not success:
                    print("Camera frame is empty")
                    break

                h, w, c= img.shape

                # Flip the webcam and convert image from BGR to RGB
                image_rgb = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
                # Used to optimize performance by preventing unnecessary modifications to the image data while being processed
                image_rgb.flags.writeable = False 
                # Peforms hand landmark detection (Contains hand landmarks and handeness classification)
                image_results = hands.process(image_rgb)
                # Convert image after being process since cv2 expects images in BGR 
                img = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR) 

                if image_results.multi_hand_landmarks:
                    # Adds a counter to an iterable and returns it in the form of of an enumerating object.
                    # Example: l1 = ["eat", "sleep", "repeat"] -> [(0, 'eat'), (1, 'sleep'), (2, 'repeat)]
                    # I am grabing hand landmark positions and returning them as an enumerating object
                    for i, handLMs in enumerate (image_results.multi_hand_landmarks):

                        x_max, y_max = 0
                        x_min = w, y_min = h

                        for lm in handLMs.landmark:
                            x, y = int(lm.x * w), int(lm.y * h)
                            if x > x_max:
                              x_max = x
                            if x < x_min:
                              x_min = x
                            if y > y_max:
                              y_max = y
                            if y < y_min:
                              y_min = y

                        # Draw a bounding box around the hand based on landmark positions
                        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (138,43,226), 2)
                        self.mp_drawing.draw_landmarks(img, handLMs, self.hand.HAND_CONNECTIONS)

                        label_x = x_min
                        label_y = y_min - 10 # Position above the top of the hand

                        handedness = image_results.multi_handedness[i]

                        label = MessageToDict(handedness)['classification'][0]['label']
                        (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

                        # Create and display the background for text 'Left Hand' and 'Right Hand'
                        cv2.rectangle(img, (label_x - 1, label_y + baseline - label_height - 20), 
                        (label_x + label_width + 80, label_y + baseline), (0, 0, 0), -1)
                        # Display 'Left Hand', 'Right Hand' or both on the hand window
                        cv2.putText(img, label + ' Hand', (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                        self.mp_drawing.draw_landmarks(img, handLMs, mp.solutions.hands.HAND_CONNECTIONS)

                        middle_finger_tip = handLMs.landmark[self.MIDDLE_FINGER_TIP]
                        index_finger_tip = handLMs.landmark[self.INDEX_FINGER_TIP]
                        ring_finger_tip = handLMs.landmark[self.RING_FINGER_TIP]
                        pinky_finger_tip = handLMs.landmark[self.PINKY_FINGER_TIP]
                        thumb_tip = handLMs.landmark[self.THUMB_TIP]

                        dist = Distance()

                        # Calculate the distance between specific landmark fingers and return their values
                        distance_1 = dist.point_distance(index_finger_tip, thumb_tip)
                        distance_2 = dist.point_distance(middle_finger_tip, thumb_tip)
                        distance_3 = dist.point_distance(ring_finger_tip, thumb_tip)
                        distance_4 = dist.point_distance(pinky_finger_tip, thumb_tip)

                        threshold = 0.04
                        print(i, handLMs)

                        t = Task()

                        value = 0

                        # If left or right hand is detected and one of the four distances are less than the threshold
                        # assign value a number and send parameter to Class Task function.
                        if label == 'Left':
                          if distance_1 < threshold:
                            value = 1
                          elif distance_2 < threshold:
                             value = 2
                          elif distance_3 < threshold:
                             value = 3
                          elif distance_4 < threshold:
                             value = 4

                        if label == 'Right':
                          if distance_1 < threshold:
                            value = 5
                          elif distance_2 < threshold:
                             value = 6
                          elif distance_3 < threshold:
                             value = 7
                            
                        t.preset_task(value)

                cv2.imshow('Hand Tracking', img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                  break

class Distance:
    def __init__(self) -> None:
        pass

    def point_distance(self, point_1, point_2):

        # Euclidean formula to calculate the distance between two points using the landmark data
        dist_formula = math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2
                      + (point_2.z - point_1.z) ** 2)
        
        return dist_formula
    
class Task:
    def __init__(self) -> None:
        pass

    # Does a task based off the value being sent from hand_initialization function
    def preset_task(self, value):
        if value == 1:
              open("Google Chrome", match_closest=True)
        elif value == 2:
            open("Spotify", match_closest=True)
        elif value == 3:
            open("Steam", match_closest=True)
        elif value == 4:
            pyautogui.hotkey('alt', 'f4')
        elif value == 5:
            pyautogui.press('playpause')
            time.sleep(0.2)
        elif value == 6:
            pyautogui.press('prevtrack')
            time.sleep(0.2)
        elif value == 7:
            pyautogui.press('nexttrack')
            time.sleep(0.2)

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

    