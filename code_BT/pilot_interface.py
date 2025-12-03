import socket
import json
import time
from typing import Dict, Any

HOST = 'localhost'
PORT = 55555

DOS_THRESHOLD_COUNT = 10
DOS_THRESHOLD_TIME = 0.1 

class PilotAltitudeDisplay:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.current_altitude = 0 
        self.message_counter = 0
        self.time_window_start = time.time()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind((self.host, self.port))
        except OSError as e:
            print(f"Error binding socket: {e}. Is the port already in use?")
            raise

        print("Pilot Altitude Display Started (DoS Detection Enabled)")
        print(f"Listening on UDP {self.host}:{self.port}")
        print(f"DoS Threshold: >{DOS_THRESHOLD_COUNT} msgs in {DOS_THRESHOLD_TIME}s")
        print("=" * 50)

    def _check_for_dos(self) -> bool:
        current_time = time.time()
        time_elapsed = current_time - self.time_window_start
        
        if time_elapsed >= DOS_THRESHOLD_TIME:
            if self.message_counter > DOS_THRESHOLD_COUNT:
                print("\n\n***INCOMING DATA FLOOD DETECTED***\n")
                self.message_counter = 0 
                self.time_window_start = current_time
                return True
            else:
                self.message_counter = 0
                self.time_window_start = current_time
                return False
        
        self.message_counter += 1
        return False

    def start_receiver_loop(self):
        while True:
            try:
                self.sock.settimeout(0.01)
                
                data, _ = self.sock.recvfrom(1024)

                self._check_for_dos()
                
                # Process the data
                message = json.loads(data.decode())
                self.current_altitude = message['altitude'] 
                altitude_feet = f"{self.current_altitude} ft"

                if message.get('type') == 'normal':
                    print(f" [DISPLAY] Current Altitude: {altitude_feet:<15} NORMAL")
                
                elif message.get('type') == 'attack':
                    print(f" [DISPLAY] Current Altitude: {altitude_feet:<15} SPOOFED!")
                    if self.current_altitude < 500:
                        print("🚨 TERRAIN WARNING! PULL UP!")
                    elif self.current_altitude > 45000:
                        print("⚠️ EXTREME ALTITUDE WARNING!")
                
            except socket.timeout:
                self._check_for_dos() 
                pass
            except json.JSONDecodeError:
                print(" [ERROR] Received invalid JSON data.")
            except KeyError:
                print(" [ERROR] Message missing expected key 'altitude'.")
            except socket.error as e:
                print(f" [SOCKET ERROR] {e}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        receiver = PilotAltitudeDisplay() 
        receiver.start_receiver_loop()
    except Exception as e:
        print(f"\nProgram shutting down: {e}")
