def detect_anomalies(open_ports):
    anomalies = []

    if len(open_ports) > 30:
        anomalies.append("High number of exposed services")

    critical_ports = {
        23: "Telnet exposed",
        3389: "RDP exposed",
        21: "FTP exposed"
    }

    for port in open_ports:
        if port in critical_ports:
            anomalies.append(critical_ports[port])

    return anomalies if anomalies else ["No major anomalies detected"]