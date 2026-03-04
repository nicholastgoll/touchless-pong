# Touchless Pong

This is a touchless pong game that uses the Raspberry Pi Model 4B, HC-SR04
ultrasonic distance sensor, and more.

## TODO Outline:

- make sure sensor works (w stability and accuracy)
- get pygame pong working wo sensor to make sure gameplay works
- create web page and figure out how to connect it to RPi

## Notes for game.py

working on pong game currently, as of now it's a very basic pong game that doesn't
have scoring, and will not work with sensor atm.
For it to work with the sensor, one important thing is to change the PLAYER_SPEED 
to change dynamically to match the user's hand speed. Need to figure this out..
