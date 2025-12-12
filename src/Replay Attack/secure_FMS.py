import random
import can
import time
import hmac
import hashlib
import struct

SENDER_ID_FMS = 1  # 0b01

# random key (for demo) in real system, inject securely
LOCAL_KEY = random.randint(0, 0xFF)

counter = 0


def compute_odd_parity(word_39bits: int) -> int:
    ones_total = bin(word_39bits).count('1')
    return 1 if ones_total % 2 == 0 else 0


def arinc429_sender_40(label: int, sdi: int, data: int, ssm: int, auth: int) -> int:
    """
    Build 40-bit secure ARINC word:
    [parity:1][ssm:2][data:19][sdi:2][label:8][auth:8]
    """
    word = 0
    word |= (ssm & 0x3) << 37
    word |= (data & 0x7FFFF) << 18
    word |= (sdi & 0x3) << 16
    word |= (label & 0xFF) << 8
    word |= (auth & 0xFF)

    parity = compute_odd_parity(word)
    return (parity << 39) | word


def send_word(bus, word_full: int):
    data_bytes = word_full.to_bytes(5, byteorder='big')
    msg = can.Message(
        arbitration_id=0x100,
        data=data_bytes,
        is_extended_id=False
    )
    try:
        bus.send(msg)
        print(f"[FMS]: Message sent!")
    except can.CanError:
        print("[FMS]: Messgae NOT  sent!")


def compute_mac(key: int, label: int, sdi: int, data_field: int, nonce: int) -> int:
   #creates a MAC and truncates it into 8 bits
    key_bytes = key.to_bytes(1, 'big')
    # pack label 
    msg = struct.pack(">BBI", label & 0xFF, sdi & 0xFF, data_field & 0xFFFFFFFF) + nonce.to_bytes(1, 'big')
    full = hmac.new(key_bytes, msg, hashlib.sha256).digest()
    return full[0]  # truncate to 8 bits


def broadcast_own_key(bus):
    # initializes key 
    label = 0xFE
    data = 0
    sdi = SENDER_ID_FMS
    ssm = 0

    auth = LOCAL_KEY & 0xFF
    word = arinc429_sender_40(label, sdi, data, ssm, auth)
    send_word(bus, word)

    print(f"[FMS] Broadcasted key: 0x{auth:02X}")


def send_normal_messages(bus):
    global counter, LOCAL_KEY

    for i in range(6):
        label = 0xFF        
        sdi = SENDER_ID_FMS
        raw_value = random.randint(0, 0x7FF) 
        ssm = 0

        nonce = counter & 0xFF
        #packs nonce and data together
        data_field = ((nonce & 0xFF) << 11) | (raw_value & 0x7FF)

        auth = compute_mac(LOCAL_KEY, label, sdi, data_field, nonce) & 0xFF

        word = arinc429_sender_40(label, sdi, data_field, ssm, auth)
        send_word(bus, word)

        counter = (counter + 1) & 0xFF
        time.sleep(2)


def main():
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')

    time.sleep(0.2)
    broadcast_own_key(bus)

    time.sleep(0.2)
    send_normal_messages(bus)


if __name__ == "__main__":
    main()
