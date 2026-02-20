import argparse
import time
import shutil
import subprocess
import json

from core.port_scanner import PortScanner
from core.banner_grabber import grab_banner
from core.service_fingerprint import fingerprint_service
from core.risk_engine import calculate_risk
from core.detector import detect_os
from core.reporter import generate_json_report, generate_html_report


def run_nmap(target, port_range):
    if not shutil.which("nmap"):
        print("[!] Nmap not found in system PATH.")
        return None

    print("[+] Running Advanced Nmap scan...")

    command = [
        "nmap",
        "-sS",
        "-sV",
        "-O",
        "--reason",
        "-T4",
        "--open",
        "-p", port_range,
        "-oJ", "nmap_output.json",
        target
    ]

    try:
        subprocess.run(command, check=True)
        with open("nmap_output.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Nmap scan failed: {e}")
        return None

def parse_nmap_ports(nmap_data):
    open_ports = []
    services = {}

    try:
        ports = nmap_data["scan"]
        for host in ports:
            for p in ports[host]["tcp"]:
                if ports[host]["tcp"][p]["state"] == "open":
                    open_ports.append(int(p))
                    services[int(p)] = ports[host]["tcp"][p]["name"]
    except:
        pass

    return open_ports, services


def compare_results(internal_ports, nmap_ports):
    internal_set = set(internal_ports)
    nmap_set = set(nmap_ports)

    only_internal = internal_set - nmap_set
    only_nmap = nmap_set - internal_set

    print("\n[+] Comparison Result:")
    print(f"    Internal only: {sorted(list(only_internal))}")
    print(f"    Nmap only: {sorted(list(only_nmap))}")


def main():
    parser = argparse.ArgumentParser(description="NetSpectre - Advanced Port Scanner")
    parser.add_argument("--target", required=True, help="Target IP or hostname")
    parser.add_argument("--ports", default="1-1024", help="Port range (e.g. 1-1000)")
    parser.add_argument("--use-nmap", action="store_true", help="Enable Nmap fallback mode")

    args = parser.parse_args()

    print(f"[+] Target: {args.target}")
    print(f"[+] Port Range: {args.ports}")

    start_time = time.time()

    # INTERNAL SCAN
    scanner = PortScanner(args.target, args.ports)
    open_ports = scanner.scan()

    services = {}
    for p in open_ports:
        banner = grab_banner(args.target, p)
        services[p] = fingerprint_service(p, banner)

    os_guess = detect_os(open_ports)
    risk_score = calculate_risk(open_ports)

    # NMAP MODE 
    nmap_ports = []
    nmap_services = {}

    if args.use_nmap:
        nmap_data = run_nmap(args.target, args.ports)
        if nmap_data:
            nmap_ports, nmap_services = parse_nmap_ports(nmap_data)
            compare_results(open_ports, nmap_ports)

    scan_time = time.time() - start_time

    # REPORT GENERATION
    report_data = {
        "target": args.target,
        "internal_scan": {
            "open_ports": open_ports,
            "services": services,
            "os_guess": os_guess,
            "risk_score": risk_score
        },
        "nmap_scan": {
            "open_ports": nmap_ports,
            "services": nmap_services
        },
        "scan_time": round(scan_time, 2)
    }

    generate_json_report(report_data)
    generate_html_report(report_data)

    print("\n[+] Scan Summary")
    print(f"    Open Ports (Internal): {open_ports}")
    if args.use_nmap:
        print(f"    Open Ports (Nmap): {nmap_ports}")
    print(f"    OS Guess: {os_guess}")
    print(f"    Risk Score: {risk_score}")
    print(f"    Scan Time: {round(scan_time,2)} sec")
    print("[+] Reports generated successfully.")


if __name__ == "__main__":
    main()