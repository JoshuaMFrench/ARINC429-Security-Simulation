
#  defense

import socket,time, json, hmac, hashlib

class SecureARINC429:
    def __init__(self):
        self.secret_key = b'Secret_key'  # Shared 
        self.bus_port = 8888
        self.display_port = 8889
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def generate_mac(self, data):
        """Authentication Code"""
        return hmac.new(self.secret_key, str(data).encode(), hashlib.sha256).hexdigest()[:16]  # Short 
    
    def verify_mac(self, data, received_mac):
        """Authentication Code"""
        expected_mac = self.generate_mac(data)
        return hmac.compare_digest(expected_mac, received_mac)
    
    def send_secure_data(self, airspeed):
        """Send authenticated airspeed data"""
        mac = self.generate_mac(airspeed)
        
        secure_msg = {
            'type': 'secure',
            'sender': 'SecureADC',
            'airspeed': airspeed,
            'mac': mac,
            'label': 0x81
        }
        
        self.sock.sendto(json.dumps(secure_msg).encode(), ('localhost', self.bus_port))
        self.sock.sendto(json.dumps(secure_msg).encode(), ('localhost', self.display_port))
        print(f" Sent authenticated airspeed: {airspeed} knots")

class SecureMonitor:
    def __init__(self):
        self.secret_key = b'arinc429_secret_key_2025'
        self.port = 8888
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', self.port))
    
    def verify_message(self, data, received_mac):
        expected_mac = hmac.new(self.secret_key, str(data).encode(), hashlib.sha256).hexdigest()[:16]
        return hmac.compare_digest(expected_mac, received_mac)
    
    def start_secure_monitor(self):
        print("\n Secure Monitor Started")
        print("\n Waiting for authenticated data")
        
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            
            if message['type'] == 'secure':
                is_valid = self.verify_message(message['airspeed'], message['mac'])
                
                if is_valid:
                    print(f"  Valid airspeed: {message['airspeed']} knots from {message['sender']}")
                else:
                    print(f" Spoofed data rejected: {message['airspeed']} knots")
            
            elif message['type'] == 'attack':
                print(f" [UNSECURED ATTACK] {message['sender']} -> FAKE: {message['airspeed']} knots (NO AUTH)")

# Quick demo
if __name__ == "__main__":
    secure_system = SecureARINC429()
    
    # Send some secure data
    secure_system.send_secure_data(460)
    time.sleep(1)
    secure_system.send_secure_data(500)
    time.sleep(1)
    
    print("\n Now attacker-trying...")
    print("\n rejected...")
    
    # Simulate attacker without key
    attacker_msg = {
        'type': 'attack', 
        'sender': 'MALWARE',
        'airspeed': 350,
        'label': 0x81
    }
    secure_system.sock.sendto(json.dumps(attacker_msg).encode(), ('localhost', 8888))
