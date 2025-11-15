# Terminal 1

import socket
import time
import json

class ARINC429Bus:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print(" Monitor Started")
        print(" Listening on localhost:8888")
        print("=" * 50)
#monitor incoming messages
    def start_monitor(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            
            if message['type'] == 'data':
                print(f" [BUS] {message['sender']} -> "
                      f"Airspeed: {message['airspeed']} knots "
                      f"(Label: 0x{message['label']:02X})")
            
            elif message['type'] == 'attack':
                print(f" [ATTACK] {message['sender']} -> "
                      f"FAKE Airspeed: {message['airspeed']} knots "
                      f" SPOOFED DATA!")
            
            elif message['type'] == 'warning':
                print(f" [WARNING] {message['message']}")

if __name__ == "__main__":
    bus = ARINC429Bus()
    bus.start_monitor()