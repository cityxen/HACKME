# Placeholder for camera to joyport control server

# GPIO Pins used for the serial device
#
# Pin 6  Ground
# Pin 8  TXD
# Pin 10 RXD
# Pin 1  3 volt
#
# GPIO Pins used for the Relay Boards
#
# Relay Board 1
# Pin 2  5 volt VCC Relay Board 1
# Pin 9  Ground Relay Board 1
# Pin 12 Relay 1
# Pin 7  Relay 2
# Pin 11 Relay 3
# Pin 13 Relay 4
# Pin 15 Relay 5
# Pin 19 Relay 6
# Pin 21 Relay 7
# Pin 23 Relay 8
#
# Relay Board 2
# Pin 4  5 volt VCC Relay Board 2
# Pin 39 Ground Relay Board 2
# Pin 16 Relay 1
# Pin 18 Relay 2
# Pin 22 Relay 3
# Pin 40 Relay 4
# Pin 38 Relay 5
# Pin 36 Relay 6
# Pin 32 Relay 7
# Pin 37 Relay 8


# Set up a dictionary for GPIO pins used for the relay up/down states
gp = {12:False, 7:False,11:False,13:False,15:False,19:False,21:False,23:False,16:False,18:False,
      22:False,40:False,38:False,36:False,32:False,37:False} # TODO: Add four more for the 4 relay board
