# Touchless Pong

A Raspberry Pi powered Pong game controlled by hand movement using an ultrasonic distance sensor.

This project includes a web interface for game setup, and LED status indicator, sound effects, email notifications with game results, and ThingSpeak IoT analystics to track game results over time.

## Features:

- **Gesture Control** - Move in-game paddle by moving your hand in front of the HC-SR04 ultrasonic sensor
- **Control Modes** - Option to play with arrow keys or ultrasonic sensor
- **Web Interface** - Choose your controller, start games, and view game history analytics
- **LED Indicator** - Green LED lights up while game is in progress
- **Sound Effects** - Audio feedback for countdown, scoring, losing a point, winning, and losing
- **Email Notifications** - Optionally input email and recieve your game results via email after each match
- **ThingSpeak Analytics** - Game stats are logged to ThingSpeak for game history visualization

## Hardware and Software Used

**Hardware** :
- Raspberry Pi 4 Model B
- HC-SR04 Ultrasonic Distance Sensor
- 1x green LED
- 270 and 2x 470 Ohm resistors
- At least 6 jumper wires
- small speaker (connected via 3.5mm audio jack)
- breadboard
- Monitor connected to Pi or Virtual Network Computing (VNC) Software
- Keyboard and mouse
- Optional but recommended table tennis paddle or any flat surface instead of using just your hand for best sensor feedback

**Wiring** *(important if you are not planning on changing pin variables in code)*
- HC-SR04 Wiring
    
