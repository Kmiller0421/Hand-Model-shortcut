import mediapipe as mp
import cv2
import numpy as np
from google.protobuf.json_format import MessageToDict

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels

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
    
    def hand_initialization(self, webcam):
        with self.mp_hands as hands:
            while True:
                success, img = webcam.read()
                if not success:
                    break

                h, w, c = img.shape
                image_rgb = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
                image_results = hands.process(image_rgb)
                img = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

                if image_results.multi_hand_landmarks:
                    for handLMs in image_results.multi_hand_landmarks:
                        x_max = 0
                        y_max = 0
                        x_min = w
                        y_min = h

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

                        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (138,43,226), 2)
                        self.mp_drawing.draw_landmarks(img, handLMs, self.hand.HAND_CONNECTIONS)

                        label_x = x_min
                        label_y = y_min - 10 # Position above the top of the hand

                        for i in image_results.multi_handedness:
                           label = MessageToDict(i)['classification'][0]['label']
                           if label == 'Left':
                               # Display 'Left Hand' on the left side of the window
                               cv2.putText(img, label + ' Hand', (label_x, label_y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (138,43,226), 2)
                            
                           if label == 'Right':
                               # Display 'Right Hand' on the right side of the window
                               cv2.putText(img, label + ' Hand', (label_x, label_y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (138,43,226), 2)

                cv2.imshow('Hand Tracking', img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                  break

    