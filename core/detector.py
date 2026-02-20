def detect_os(open_ports):
    if 135 in open_ports or 445 in open_ports:
        return "Windows (Likely)"
    if 22 in open_ports:
        return "Linux/Unix (Likely)"
    return "Unknown"