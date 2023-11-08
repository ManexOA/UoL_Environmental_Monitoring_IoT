from dylos import Dylos

# initialize
d = Dylos(port='/dev/ttyUSB0')

# start listening
d.read()
