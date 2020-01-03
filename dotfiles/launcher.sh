#!/bin/bash
# launcher.sh
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

sleep 2
xmodmap ~/r_e_c_u_r/dotfiles/.remap &
python3 ~/r_e_c_u_r/helpers/soundreact.py &
python3 ~/r_e_c_u_r/r_e_c_u_r.py

