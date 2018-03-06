#!/bin/bash -e

TARGET_IP=169.254.169.254
HOST_PORT=8079

function reset_pfctl(){
  sudo pfctl -F all -f /etc/pf.conf
  sudo pfctl -E
}

if [ "$1" = "remove" ];then
  echo 'Removing mock-server-service forward'
  sudo sed -i.bak '/mock-server-service/d' /etc/pf.conf
  sudo rm /etc/pf.anchors/mock-server-service
  reset_pfctl
  exit 0
fi

echo "Configuring forward port:
  ${TARGET_IP}:80 -> 127.0.0.1:${HOST_PORT}
"

[ -f /etc/pf.anchors/mock-server-service ] ||
sudo tee /etc/pf.anchors/mock-server-service << EOF
Packets = "proto tcp from any to ${TARGET_IP} port 80"
rdr pass log on lo0 \$Packets -> 127.0.0.1 port ${HOST_PORT}
pass out log route-to lo0 inet $Packets keep state
EOF

grep 'mock-server-service' /etc/pf.conf >> /dev/null ||
sudo sed -i.bak '
/dummynet-anchor/i \
rdr-anchor "mock-server-service"
/load anchor.*apple/i \
anchor "mock-server-service"
$ a\
load anchor "mock-server-service" from "/etc/pf.anchors/mock-server-service"
' /etc/pf.conf

reset_pfctl

echo "Done, you can now start the service with one of the two solutions:
    HOST_PORT=${HOST_PORT} docker-compose up
    ./src/simple-mock-server.py ${HOST_PORT}
"
