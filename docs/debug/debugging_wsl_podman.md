# Debugging Podman in WSL (Fedora 42)

> ⚠️ **Tested Environments Only:** These instructions have been verified on:
> - Fedora 42 running inside WSL2
> - macOS with Podman installed
>
> Other systems may behave differently or require further steps.

This guide provides useful steps for configuring and debugging Podman on **Fedora 42 running inside WSL**.

---

## WSL (Fedora 42) Setup Notes

### 1. Install Podman using DNF

```bash
sudo dnf install podman podman-compose
```

### Configure Podman to Use `iptables`

Make sure `iptables` package is installed:

```bash
sudo dnf install iptables-nft
```

To ensure proper networking behavior when using Podman inside WSL, update the containers configuration:

```conf
# /etc/containers/containers.conf
[network]
firewall_driver="iptables"
```

---

### Additional Notes
- Container networking in WSL can occasionally fail. Restart WSL or the container engine if things break unexpectedly.
- This setup is not yet tested in native Ubuntu WSL or Debian — use Fedora 42 WSL for best compatibility.
- Make sure your user is part of the appropriate groups if you face permission issues with Podman.