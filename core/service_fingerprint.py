def fingerprint_service(port, banner):
    known_services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP"
    }

    if port in known_services:
        return known_services[port]

    if banner:
        if "apache" in banner.lower():
            return "Apache Web Server"
        if "nginx" in banner.lower():
            return "Nginx Web Server"
        if "openssh" in banner.lower():
            return "OpenSSH"

    return "Unknown Service"