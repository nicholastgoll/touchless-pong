# Touchless Pong

This is a touchless pong game that uses the Raspberry Pi 4 Model B, HC-SR04
ultrasonic distance sensor, and more.

## TODO Outline:

- make sure sensor works (w stability and accuracy)
- get pygame pong working wo sensor to make sure gameplay works
- create web page and figure out how to connect it to RPi

## Notes for game.py
Currently, pong game is fully functional with arrow keys. We can make aesthetic changes still.
!need to add sensor functions, want to do this in same file.
For it to work with the sensor, one important thing is to change the PLAYER_SPEED 
to change dynamically to match the user's hand speed. Need to figure this out..
