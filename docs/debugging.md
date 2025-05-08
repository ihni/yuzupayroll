feel free to run the container detached by using
-d flag
then doing
podman exec -it <container-name> bash

in this case, usually it should be payrollsys_db_1

#
use wsl fedora 42
install via dnf and also add
to configure podman to use iptables
```bash
# /etc/containers/containers.conf
[network]
firewall_driver="iptables"
```
iptables-nft

#
add this to make file or
export PODMAN_IGNORE_CGROUPSV1_WARNING=1
services:
  your_service:
    environment:
      - PODMAN_IGNORE_CGROUPSV1_WARNING=1

to suppress cgroups warning on wsl