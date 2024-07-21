import mediapipe as mp
import cv2
import numpy as np
from google.protobuf.json_format import MessageToDict
from distance import distance
from task import Task

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
            while True:
                success, img = webcam.read()
                if not success:
                    print("Camera frame is empty")
                    break

                h, w, c = img.shape
                image_rgb = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
                image_rgb.flags.writeable = False
                image_results = hands.process(image_rgb)
                img = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

                if image_results.multi_hand_landmarks:
                    for i, handLMs in enumerate (image_results.multi_hand_landmarks):
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

                        handedness = image_results.multi_handedness[i]

                        label = MessageToDict(handedness)['classification'][0]['label']
                        (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

                        cv2.rectangle(img, (label_x - 1, label_y + baseline - label_height - 20), 
                        (label_x + label_width + 80, label_y + baseline), (0, 0, 0), -1)
                        # Display 'Left Hand' on the left side of the window
                        cv2.putText(img, label + ' Hand', (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                        self.mp_drawing.draw_landmarks(img, handLMs, mp.solutions.hands.HAND_CONNECTIONS)

                        middle_finger_tip = handLMs.landmark[self.MIDDLE_FINGER_TIP]
                        index_finger_tip = handLMs.landmark[self.INDEX_FINGER_TIP]
                        ring_finger_tip = handLMs.landmark[self.RING_FINGER_TIP]
                        pinky_finger_tip = handLMs.landmark[self.PINKY_FINGER_TIP]
                        thumb_tip = handLMs.landmark[self.THUMB_TIP]

                        dist = distance()

                        distance_1 = dist.point_distance(index_finger_tip, thumb_tip)
                        distance_2 = dist.point_distance(middle_finger_tip, thumb_tip)
                        distance_3 = dist.point_distance(ring_finger_tip, thumb_tip)
                        #distance_4 = dist.point_distance(pinky_finger_tip, thumb_tip)

                        threshold = 0.04
                        threshold_1 = 0.09

                        print(distance_3)

                        t = Task()

                        value = 0

                        if label == 'Left':
                          if distance_1 < threshold:
                            value = 1
                          elif distance_2 < threshold:
                             value = 2
                          elif distance_3 < threshold:
                             value = 3

                        if label == 'Right':
                          if distance_1 < threshold_1:
                            value = 4
                          elif distance_2 < threshold_1:
                             value = 5
                          elif distance_3 < threshold_1:
                             value = 6
                            
                        t.preset_task(value)

                cv2.imshow('Hand Tracking', img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                  break

    