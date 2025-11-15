#Terminal 2

import socket
import time
import json

class PilotDisplay:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8889
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.current_speed = 0
        print("Pilot Display Started")
        print(" Waiting for airspeed data...")
        print("=" * 50)
#monitor incoming messages and update display
    def update_display(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            
            self.current_speed = message['airspeed']
            
            if message['type'] == 'normal':
                print(f" [DISPLAY] Current Airspeed: {self.current_speed} knots  NORMAL")
            
            elif message['type'] == 'attack':
                print(f" [DISPLAY] Current Airspeed: {self.current_speed} knots  SPOOFED!")
                
                # Warning for dangerous values
                if self.current_speed < 130:
                    print(" LOW AIRSPEED WARNING!")
                elif self.current_speed > 350:
                    print("  OVERSPEED WARNING!")

if __name__ == "__main__":
    display = PilotDisplay()
    display.update_display()