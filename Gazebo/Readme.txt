This are the steps you need to follow in order to run Gazebo 11 on Ubuntu 20.04 (WSL2) :

1- Open the XLaunch program and set the display settings
 - Multiple windows
 - Display number: 0
 - Start no client
 - Unmark "Native opengl"
 - Mark "Disable access control"
 - Click on "Finish"

2- Open the Linux Terminal and go to /home/user directory

3- Copy and paste these lines on the terminal:

export GAZEBO_IP=127.0.0.1
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0 
export LIBGL_ALWAYS_INDIRECT=0

4- Finally type "gazebo" and you would be able to run Gazebo.



*Source: https://www.youtube.com/watch?v=DW7l9LHdK5c
