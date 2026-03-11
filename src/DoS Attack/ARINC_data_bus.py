import socket
import json
import time
import random

HOST = 'localhost'
PORT = 55555
UPDATE_RATE_SEC = 0.5

def create_altitude_word(altitude: int, msg_type: str) -> bytes:
    """Creates the JSON packet mimicking an ARINC 429 decoded word."""
    data = {
        "altitude": altitude,
        "type": msg_type
    }
    return json.dumps(data).encode('utf-8')

def arinc_simulator():
    """Simulates the ARINC 429 sender."""
    print("✈️ ARINC 429 Altitude Sender Starting...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    current_altitude = 10000 

    try:
        while True:
            current_altitude += random.randint(-5, 5) 

            if current_altitude > 30000: current_altitude = 30000
            if current_altitude < 5000: current_altitude = 5000

            word = create_altitude_word(current_altitude, 'normal')
            
            sock.sendto(word, (HOST, PORT))
            print(f"[TX-NORMAL] Sent Altitude: {current_altitude} ft")
            
            time.sleep(UPDATE_RATE_SEC)
            
    except KeyboardInterrupt:
        print("\nARINC Simulator shutting down.")
    finally:
        sock.close()

if __name__ == "__main__":
    arinc_simulator()
