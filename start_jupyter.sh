#!/bin/bash
# Prepare environment for TECNMS-2401

#Start up csr in vagrant, if applicable
#vagrant up csr
docker run -d -p58887:58888 -v$(pwd):/home/docker/ --name "tecnms2401" kuhlskev/ansible_ydk_jupyter
#pause for a few seconds to let jupyter startup
sleep 2
#then open browser to http://127.0.0.1:58887
open http://localhost:58887/notebooks/TECNMS-2401.ipynb
