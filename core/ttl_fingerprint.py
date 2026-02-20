import subprocess
import platform

def estimate_os(target):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, "1", target], universal_newlines=True)
        if "TTL=" in output.upper():
            ttl = int(output.upper().split("TTL=")[1].split()[0])
            if ttl <= 64:
                return "Linux/Unix (Estimated)"
            elif ttl <= 128:
                return "Windows (Estimated)"
        return "Unknown"
    except:
        return "Unknown"