#!/usr/bin/python
# coding:utf-8
import subprocess


def configure_static_ip(interface, ip_address, prefix_length, gateway, dns_servers):
    # Configure IP address and prefix length
    command = [
        "sudo", "nmcli", "con", "mod", interface,
        "ipv4.addresses", f"{ip_address}/{prefix_length}",
        "ipv4.method", "manual"
    ]
    subprocess.run(command, check=True)

    # Configure gateway
    command = [
        "sudo", "nmcli", "con", "mod", interface,
        "ipv4.gateway", gateway
    ]
    subprocess.run(command, check=True)

    # Configure DNS servers
    dns_str = " ".join(dns_servers)
    command = [
        "sudo", "nmcli", "con", "mod", interface,
        "ipv4.dns", dns_str,
        "ipv4.ignore-auto-dns", "yes"
    ]
    subprocess.run(command, check=True)

    # Apply the new configuration
    command = [
        "sudo", "nmcli", "con", "down", interface
    ]
    subprocess.run(command, check=True)

    command = [
        "sudo", "nmcli", "con", "up", interface
    ]
    
    subprocess.run(command, check=True)

    command = [
        "sudo", "nmcli", "con", "modify", interface,"connection.autoconnect","yes"
    ]
    subprocess.run(command, check=True)





# Example usage
if __name__ == "__main__":
    configure_static_ip("ens34", "192.168.2.130", "24", "192.168.2.1", ["202.102.224.68", "202.102.227.68"])