# Hand Model shortcut
This is a program that allows the user to open and close default applications, as well as control media playback.

# Purpose - :black_nib:
The purpose of this project was to explore MediaPipe by integrating its hand detection model 
into a program that allows me to control application launching and media functions using finger touch gestures. 
This implementation enables seamless control of these functions by touching my fingers together.

# How it works
* The program starts with a welcome menu offering the user two options: to either begin the program or view the instructions.
* Once the user chooses to start the Hand Model Program, they will see a live video feed of themselves on the screen.
* By raising their hands within the camera frame, they can use specific finger-touch gestures to interact with the system.
* These gestures allow the user to open and close default applications, as well as control media playback.
* The user can exit the Hand Model Program at any time by pressing the 'Esc' key.

# Bulit With - 🧰
* Python
* MediaPipe 
* Tkinter   
* CV2
* AppOpener

# Challenges
* Understanding how to calculate the distance between my fingers in a 3D environment.
* Drawing bounding boxes around the hands in the live video feed.
* Accurately determining the threshold for detecting when two fingers touch, ensuring that multiple inputs aren’t triggered unintentionally when performing a gesture.

# Demo video - :movie_camera:
