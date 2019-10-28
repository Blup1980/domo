Install :

1) install log2ram
2) reboot
3) install Docker
    sudo apt-get install apt-transport-https ca-certificates software-properties-common -y
    curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
    sudo usermod -aG docker pi
    sudo curl https://download.docker.com/linux/raspbian/gpg
    vim /etc/apt/sources.list
         Add the following line and save:   
         deb https://download.docker.com/linux/raspbian/ stretch stable
    sudo apt-get update
    sudo apt-get upgrade
    systemctl start docker.service
