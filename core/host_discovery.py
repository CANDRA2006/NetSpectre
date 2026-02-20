import ipaddress
import subprocess
import platform

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.call(["ping", param, "1", str(ip)],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
    return result == 0

def discover_hosts(network_cidr):
    network = ipaddress.ip_network(network_cidr, strict=False)
    active_hosts = []

    for ip in network.hosts():
        if ping_host(ip):
            active_hosts.append(str(ip))

    return active_hosts