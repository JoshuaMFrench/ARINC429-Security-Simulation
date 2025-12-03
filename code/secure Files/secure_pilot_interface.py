import can
import time
import random
import hmac
import hashlib
import struct

# Learned keys and expected counters
learned_keys = {}
expected_counters = {}

def compute_odd_parity(word_39bits: int) -> int:
    ones_total = bin(word_39bits).count('1')
    return 1 if ones_total % 2 == 0 else 0

def decode_40bit(word_full: int) -> dict:
    parity = (word_full >> 39) & 0x1
    ssm = (word_full >> 37) & 0x3
    data = (word_full >> 18) & 0x7FFFF
    sdi = (word_full >> 16) & 0x3
    label = (word_full >> 8) & 0xFF
    auth = word_full & 0xFF
    return {
        "parity": parity,
        "ssm": ssm,
        "data": data,
        "sdi": sdi,
        "label": label,
        "auth": auth
    }

def compute_mac(key: int, label: int, sdi: int, data_field: int, nonce: int) -> int:
    key_bytes = key.to_bytes(1, 'big')
    msg = struct.pack(">BBI", label & 0xFF, sdi & 0xFF, data_field & 0xFFFFFFFF) + nonce.to_bytes(1, 'big')
    full = hmac.new(key_bytes, msg, hashlib.sha256).digest()
    return full[0]

def receive_msg(duration=20):
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    start_time = time.time()
    # Random direction and path status for demo
    direction = ["North", "East", "South", "West", "Up"]
    path = ["On", "Off"]
    print("[Pilot] Listening for messages...")

    while time.time() - start_time < duration:
        msg = bus.recv(timeout=1)
        if not msg:
            continue
        word_full = int.from_bytes(msg.data, byteorder='big')
        decoded = decode_40bit(word_full)
       #print(f"[Pilot]:  {decoded}")

        # Learn the keys
        if decoded["label"] == 0xFE:
            sd = decoded["sdi"]
            key = decoded["auth"]
            learned_keys[sd] = key
            expected_counters[sd] = 0
            print(f"[Pilot] Learned key from SDI={sd}: 0x{key:02X}")
            continue

        # verify if we have key for that sender
        sd = decoded["sdi"]
        if sd not in learned_keys:
            print(f"[Pilot] No key for sender SDI={sd} yet — dropping message.")
            continue
        key = learned_keys[sd]
        auth = decoded["auth"]

        # Extract nonce and 11-bit value from the 19-bit data field
        nonce = (decoded["data"] >> 11) & 0xFF
        value = decoded["data"] & 0x7FF
        data_field = decoded["data"]

        expected = expected_counters.get(sd, 0)

        # Check nonce to prevent replay 
        if nonce != expected:
            print(f"[Pilot] Message FAILED nonce check: got nonce={nonce}, expected={expected}. DROPPED.")
            continue

        # Verify MAC
        computed_mac = compute_mac(key, decoded["label"], sd, data_field, nonce) & 0xFF
        if computed_mac != auth:
            print(f"[Pilot] Message FAILED MAC verification. DROPPED.")
            continue

        # Authentication success — increment expected counter
        expected_counters[sd] = (expected + 1) & 0xFF

        # Figure out who sent it by label
        label = decoded["label"]
        data_bin = format(value, "011b")
        if label == 0x00:
            # AoA down message (value==0 interpreted as DOWN)
            if value == 0:
                print("[Pilot] AoA (authenticated): plane pointing Down.")
            else:
                # AoA other messages
                print(f"[Pilot] AoA (authenticated): plane pointing {direction[random.randint(0,4)]}")
        elif label == 0xFF:
            # FMS messages
            print(f"[Pilot] FMS (authenticated): Flight is {path[random.randint(0,1)]} Path")
        else:
            # Other authenticated messages
            pass
    bus.shutdown()
    print("[Pilot] Done listening.")

if __name__ == "__main__":
    receive_msg()
