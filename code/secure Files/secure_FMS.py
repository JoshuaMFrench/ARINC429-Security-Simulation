# secure_FMS.py 

import random
import can
import time

SENDER_ID_FMS = 1  # 0b01

#random key
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


def broadcast_own_key(bus):
    #initilizes key
    label = 0xFE
    data = 0
    sdi = SENDER_ID_FMS
    ssm = 0

    auth = LOCAL_KEY & 0xFF
    word = arinc429_sender_40(label, sdi, data, ssm, auth)
    send_word(bus, word)

    print(f"[FMS] Broadcasted key: 0x{auth:02X}")


def send_normal_messages(bus):
    
    #Send a series of FMS messages
    
    global counter, LOCAL_KEY

    for i in range(6):
        label = 0xFF          # FMS normal data label
        sdi = SENDER_ID_FMS
        data = random.randint(0, 0x7FFFF)
        ssm = 0

        auth = (counter & 0xFF) ^ (LOCAL_KEY & 0xFF)

        word = arinc429_sender_40(label, sdi, data, ssm, auth)
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
