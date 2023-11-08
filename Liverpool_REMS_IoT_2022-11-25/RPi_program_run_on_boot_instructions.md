# Set a Raspberry-Pi for running a program at startup

## Using bash-scripting method:
- [ ] (https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/)


## Using rc.local method:
- [ ] (https://linuxhint.com/use-rc-local-on-ubuntu/)

"rc.local" is a file that contains commands that are executed on the startup of the machine. This file already exists in the official operating system of the RPi (Raspbian OS).

*Note: If the RPi is using Ubuntu or other operating system instead of Raspbian, it might be neccessary to create the rc.local file from scratch as it will not come with it by default. In that case, follow the instructions indicated in this website:

1. Editing the rc.local file
- On your Raspberry Pi, open the file /etc/rc.local as root with an editor:
```bash
  sudo nano /etc/rc.local
```
- Add your commands below the comments, and leave the exit 0 line at the end of the file:

To wait for RPi to connect to the network before running the program
```bash
  sleep 5
```
Add the script you want to run with its directory path 
```bash
  python3 /home/pi4/serial/"name of the file".py
```
Do not forget the exit 0 line at the end
```bash
  exit 0
```

2. Check if rc.local file is executable
```bash
  sudo chmod +x /etc/rc.local 
```

3. Check if rc.local service is active
```bash
  sudo systemctl status rc-local
```

4. Now reboot your Raspberry Pi to test it:
```bash
  reboot
```


## If you need to remove root permissions to launch a python file ("To remove the sudo command"):

- Add your RPi username to the dialout:
```bash
sudo adduser <the user you want to add> dialout
```
- Then:
Log out and log in again, or Reboot the machine.


## Web sources:
- [ ] (https://linuxhint.com/use-rc-local-on-ubuntu/)
- [ ] (https://raspberrypi-guide.github.io/programming/run-script-on-boot#write-to-logfile)
- [ ] (https://gist.github.com/fabiosoft/debba6b13a8ab3e40036e2d5a93edebc)
- [ ] (https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

