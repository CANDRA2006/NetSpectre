import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.config_loader import load_config
import sys

config = load_config()

class PortScanner:
    def __init__(self, target, port_range):
        self.target = target
        self.start_port, self.end_port = map(int, port_range.split("-"))
        self.timeout = config["default_timeout"]
        self.max_threads = config["max_threads"]

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                if sock.connect_ex((self.target, port)) == 0:
                    return port
        except:
            return None

    def scan(self):
        total_ports = self.end_port - self.start_port + 1
        scanned = 0
        open_ports = []

        print(f"[+] Using {self.max_threads} threads")
        print("[+] Scanning ports...")

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(self.scan_port, port): port
                for port in range(self.start_port, self.end_port + 1)
            }

            for future in as_completed(futures):
                result = future.result()
                scanned += 1

                percent = (scanned / total_ports) * 100
                sys.stdout.write(f"\rProgress: {percent:.2f}%")
                sys.stdout.flush()

                if result:
                    open_ports.append(result)

        print("\n[+] Scan complete.")
        return sorted(open_ports)