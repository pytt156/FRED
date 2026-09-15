import socket

s = socket.socket()
s.settimeout(5)
s.connect(("172.20.10.4", 1883))
print("TCP CONNECTED")
s.close()