#!/bin/bash
# Prepare environment for DEVNET2449 Lab

#vagrant up csr
docker run -it --rm -p58887:58888 -v$(pwd):/home/docker/ kuhlskev/ansible_ydk_jupyter
#then open browser to http://127.0.0.1:58887
