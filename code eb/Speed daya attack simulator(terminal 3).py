
 #demo attack

import socket
import time
import json

class SpoofingAttack:
    def __init__(self):
        self.bus_port = 8888
        self.display_port = 8889
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def launch_attack(self):
        # Attack sequence (typically air speed between 450 and 520 knots)
        fake_speeds = [600, 480, 530, 500, 400, 690, 320, 770, 310, 680] #false data

        
        for i, speed in enumerate(fake_speeds):
            # Send spoofed data to bus monitor
            bus_msg = {
                'type': 'attack',
                'sender': 'MALWARE_SPOOFER',
                'airspeed': speed,
                'label': 0x81
            }
            self.sock.sendto(json.dumps(bus_msg).encode(), ('localhost', self.bus_port))
            
            # Send spoofed data to pilot display
            display_msg = {
                'type': 'attack',
                'airspeed': speed,
                'system': 'SPOOFED'
            }
            self.sock.sendto(json.dumps(display_msg).encode(), ('localhost', self.display_port))
            
            print(f" [ATTACK] Injected fake airspeed: {speed} knots")
            time.sleep(3)

if __name__ == "__main__":
    print("start Spoofing Attack")
    print("Injecting fake airspeed values")
    attack = SpoofingAttack()
    print("Alarm...Alarm...Alarm...Alert...LOW AIRSPEED WARNING!")
    print("Alarm...Alarm...Alarm...Alert...OVERSPEED WARNING!")
    attack.launch_attack()