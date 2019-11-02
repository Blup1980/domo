Install :

1) install log2ram
2) reboot
3) install Docker
    sudo apt-get install apt-transport-https ca-certificates software-properties-common -y
    curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
    sudo usermod -aG docker pi
    systemctl start docker.service
    sudo apt-get install docker-compose
4) create group and user for openhab
    sudo addgroup --gid 9001 openhab
    sudo adduser --no-create-home -uid 9001 --gid 9001 --disabled-password openhab
4) create a location for logs with all access :
    sudo mkdir /var/log/container-logs
    sudo chmod 777 /var/log/container-logs
    
