#!/bin/bash
# Shows the image on terminal 4 (press alt-f4)
# Add user to root and video groups and change permissions on tty4
#   usermod -a -G root <username>   # for tty4 rw
#   usermod -a -G video <username>  # for fb? rw
#   sudo chmod 660 /dev/tty4

# Quit fbi is it is running.
pidof fbi
if [[ $? -eq 0 ]] ; then
	kill -s quit $(pidof fbi)
fi

# Display fullscreen on tty4
fbi -noverbose -a -T 4 "$1"
