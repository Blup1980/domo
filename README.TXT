Install :

1) install log2ram
2) reboot
3) install Docker
    sudo apt-get install apt-transport-https ca-certificates software-properties-common -y
    curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
    sudo usermod -aG docker pi
    systemctl start docker.service
    sudo apt-get install docker-compose
