#!/bin/bash
# launcher.sh
sleep 2
xmodmap ~/r_e_c_u_r/dotfiles/.remap &
python3 -m cProfile ~/r_e_c_u_r/r_e_c_u_r.py | tee >profile.output

