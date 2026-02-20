def format_console_output(report):
    print("\n===== NetSpectre Report =====")
    print(f"Target: {report['target']}")
    print(f"Open Ports: {report['open_ports']}")
    print(f"OS Estimation: {report['os_estimation']}")
    print(f"Risk Score: {report['risk_score']['score']}")
    print(f"Severity: {report['risk_score']['severity']}")
    print(f"Anomalies: {report['anomalies']}")