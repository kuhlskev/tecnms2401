# Building the Environment
## This is a rough guideline how to bring up / prepare the entire environment.
Git client
VirtualBox 5.2.6
Vagrant 2.0.1
Docker 17.12
cdrtools (in particular mkisofs)
a build environment (e.g. compiler, make, ...), suggest to use MacPorts or Brew if running on a Mac
Clone the iso-xrv-x64-vbox repository from GitHub 
IOS XE image from Cisco.com (e.g. here, then go to IOS XE Software and download the >16.5 .iso file in the Latest tree branch, ~350MB in size)
Go to the directory where you cloned the iso-xrv-x64-vbox repository. Start the Vagrant box image build by running the following command:iosxe_iso2vbox.py -v ~/Downloads/csr1000v-universalk9.16.05.02.iso 
This will take a while. When done, you need to install the resulting box into Vagrant:vagrant box add --name iosxe csr1000v-universalk9.16.05.02.box (See the output at the end of the script. It has the exact location of the generated box file and also the command to add / replace the Vagrant box file).

## Building the Vagrant Box
### The next steps are required to prepare configuration disks for the routers
Configure and Start Routers
Clone this repo from GitHub into a new directory: https://github.com/kuhlskev/tecnms2401
Make sure that the Vagrant box name matches the one configured in the Vagrant file
Ensure you have the required tools installed
run make to create the ISO files with the router configurations
Bring up the routers using vagrant up (brings up all) or vagrant up rtr1 to only start rtr1


