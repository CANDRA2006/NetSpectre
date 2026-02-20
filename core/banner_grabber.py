import socket

def grab_banner(target, port):
    try:
        with socket.socket() as sock:
            sock.settimeout(1)
            sock.connect((target, port))
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024)
            return banner.decode(errors="ignore").strip()
    except:
        return None