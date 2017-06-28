# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile for 2 CSR Routers and a JumpHost Ubuntu box
# For the session we will use kuhlskev/ansible_host container at dockerhub

Vagrant.configure("2") do |config|
    config.vm.define "csr" do |node|
      node.vm.box = "iosxe16.6.eft"
      node.ssh.insert_key = false
      node.vm.synced_folder '.', '/vagrant', disabled: true
      node.vm.network "private_network", 
        ip: "172.20.20.10",
        auto_config: false
      node.vm.network "private_network", 
        virtualbox__intnet: "link1", 
        auto_config: false

      # attach a configuration disk
      node.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", 3072]
        v.customize ["storageattach", :id, 
          "--storagectl", "IDE_Controller", 
          "--port", 1, 
          "--device", 0, 
          "--type", "dvddrive", 
          "--medium", "rtr1.iso"
        ]
        v.customize ["modifyvm", :id, 
          "--uart1", "0x3F8", 4, 
          "--uartmode1", 'tcpserver', 59996
        ]
      end
    end
    config.vm.define "csr2" do |node|
      node.vm.box = "iosxe16.6.eft"
      node.ssh.insert_key = false
      node.vm.synced_folder '.', '/vagrant', disabled: true
      node.vm.network "private_network", 
        ip: "172.20.20.20",
        auto_config: false
      node.vm.network "private_network", 
        virtualbox__intnet: "link1", 
        auto_config: false

      # attach a configuration disk
      node.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", 3072]
        v.customize ["storageattach", :id, 
          "--storagectl", "IDE_Controller", 
          "--port", 1, 
          "--device", 0, 
          "--type", "dvddrive", 
          "--medium", "rtr2.iso"
        ]
        v.customize ["modifyvm", :id, 
          "--uart1", "0x3F8", 4, 
          "--uartmode1", 'tcpserver', 59997
        ]
      end
    end    
    config.vm.define "xrv" do |node|
      node.vm.box =  "xrv"
      node.vm.network :forwarded_port, guest: 830, host: 6830, id: 'netconf', auto_correct: true
      node.vm.network :forwarded_port, guest: 22, host: 2223, id: 'ssh', auto_correct: true
      node.ssh.insert_key = false
      #node.vm.network :forwarded_port, guest: 57722, host: 2222, id: 'shell', auto_correct: true      
      # gig0/0/0/0 connected to link2, gig00/0/1 connected to link1, gig0/0/0/2 connected to link3, auto-config not supported.
      node.vm.network "private_network", 
        ip: "172.20.20.30",
        auto_config: false
      node.vm.network :private_network, virtualbox__intnet: "link1", auto_config: false
      node.vm.network :private_network, virtualbox__intnet: "link3", auto_config: false 
      node.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", 3096]
        # Optional, forward the XR console serial port a TCP port on the host
        v.customize ["modifyvm", :id, "--uart1", "0x3F8", 4, "--uartmode1", 'tcpserver', 59998]
        # Optional, forward the XR auxiliary serial  port a TCP port on the host
        v.customize ["modifyvm", :id, "--uart2", "0x2F8", 3, "--uartmode2", 'tcpserver', 59999]
      end
      node.vm.provision "file", source: "xrv/configs/rtr_config", destination: "/home/vagrant/rtr_config"

      node.vm.provision "shell" do |s|
        s.path =  "xrv/scripts/apply_config.sh"
        s.args = ["/home/vagrant/rtr_config"]
      end
    end
    #config.vm.define "n9kv" do |n9kv|
    #  #n9kv.vm.box = "nx7.0.3.I6.2"
    #  #n9kv.vm.box = "n9kv-2"
    #  #n9kv.vm.box = "N9k-NCRC"
    #  n9kv.vm.box = "n9kv-172"
    #  n9kv.ssh.insert_key = false
    #  n9kv.vm.boot_timeout = 420
    #  #n9kv.vm.ssh.shell, disabled: true
    #  n9kv.vm.synced_folder '.', '/vagrant', disabled: true
    #  n9kv.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true
    #  n9kv.vm.network "forwarded_port", guest: 830, host: 7830, auto_correct: true
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network1"
    #  n9kv.vm.network "private_network", ip: "172.20.20.50", auto_config: false
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network2"
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network3"
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network4"
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network5"
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network6"
    #  n9kv.vm.network "private_network", auto_config: false, virtualbox__intnet: "nxosv_network7"
    #  #{}"private_network", auto_config: false, virtualbox__intnet: "nxosv_network7"
    #  n9kv.vm.provider :virtualbox do |vb|
    #    vb.customize ["modifyvm", :id, "--memory", 4096]
    #    vb.name = "n9kv"
    #    vb.customize ['modifyvm',:id,'--nicpromisc2','allow-all']
    #    vb.customize ['modifyvm',:id,'--nicpromisc3','allow-all']
    #    vb.customize ['modifyvm',:id,'--nicpromisc4','allow-all']
    #    vb.customize ['modifyvm',:id,'--nicpromisc5','allow-all']
    #    vb.customize ['modifyvm',:id,'--nicpromisc6','allow-all']
    #    vb.customize ['modifyvm',:id,'--nicpromisc7','allow-all']
    #    vb.customize ['modifyvm',:id,'--nicpromisc8','allow-all']
    #    vb.customize ["modifyvm", :id, 
    #        "--uart1", "0x3F8", 4, 
    #        "--uartmode1", 'tcpserver', 59999
    #    ]
    #    vb.customize "pre-boot", [
    #        "storageattach", :id,
    #        "--storagectl", "SATA",
    #        "--port", "1",
    #        "--device", "0",
    #        "--type", "dvddrive",
    #        "--medium", "nxosv1.iso",
    #    ]
    #  end
      #n9kv.vm.provision "shell", privileged: true, inline: <<-SHELL
      #  sleep 30 #otherwise the interfaces might not be ready for configuration
      #  # Configure Eth1/1 with unique MAC and IP
      #  echo -e 'hostname n9kv1\nfeature nxapi\nvrf context management\n ip route 0.0.0.0/0 10.0.2.3\ndefault interface Ethernet1/1\ninterface Ethernet1/1\n no shutdown\n no switchport\n\n mac-address 1.1.1\ninterface Ethernet1/7\n no switchport\n mac-address 1.1.1\n'> /tmp/mac-cfg
      #  sudo vsh -r /tmp/mac-cfg
      #  sudo ip add add 172.20.20.50/24 dev Eth1-1
      #  echo "192.168.1.254    master">>/etc/hosts
      #  sudo bash -c  'echo "nameserver 10.0.2.3" > /etc/resolv.conf'
      #  sudo vsh -c 'copy running-config startup-config'
      #  echo -e '\n\n----------------\n\nProvisioning complete, next connect to the master instance ("vagrant ssh master") and run the Ansible playbook ("ansible-playbook -i ansible/hosts ansible/site.yml")\n'
      #SHELL
  #end
end
