#!/usr/bin/env bash

# it will show you the value that is stored in /etc/hostname
# See hostname --help for a lot of options. From the help ...
echo "ip a: "
ip a
echo "short host name: "
hostname --short
echo "alias names: "
hostname --alias
echo "all addresses for the host: "
hostname --all-ip-addresses
echo "all long host names (FQDNs): "
hostname --all-fqdns
echo "DNS domain name: "
hostname --domain
echo "NIS/YP domain name: "
hostname --yp
hostname --nis
