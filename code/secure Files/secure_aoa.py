# secure_aoa.py
import random
import can
import time

SENDER_ID_AOA = 0  # 0b00

# Random key on startup
LOCAL_KEY = random.randint(0, 0xFF)

# Counter
counter = 0

def compute_odd_parity(word_39bits: int) -> int:
    ones_total = bin(word_39bits).count('1')
    return 1 if ones_total % 2 == 0 else 0

def arinc429_sender_40(label: int, sdi: int, data: int, ssm: int, auth: int) -> int:
    """
    Build 40-bit word:
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
        print("[AoA]: Message sent!")
    except can.CanError:
        print("[AoA] Message NOT sent!")
# initalizes key
def send_key_broadcast(bus):
    global LOCAL_KEY
    label = 0xFE
    data = 0
    ssm = 0
    auth = LOCAL_KEY & 0xFF
    word = arinc429_sender_40(label, SENDER_ID_AOA, data, ssm, auth)
    send_word(bus, word)
    print(f"[AoA] Broadcasted key: 0x{auth:02X}")

def generate_aoa_data_value():
    return random.randint(0, 0x7FFFF)

def main():
    global counter
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    print("[AoA] Bus opened. Broadcasting key then sending AoA data...")

    send_key_broadcast(bus)
    time.sleep(0.2)

    #  5 random messages
    for i in range(5):
        label = 0x00
        data = generate_aoa_data_value()
        sdi = SENDER_ID_AOA
        ssm = 0
        auth = (counter & 0xFF) ^ (LOCAL_KEY & 0xFF)
        word = arinc429_sender_40(label, sdi, data, ssm, auth)
        send_word(bus, word)
        counter = (counter + 1) & 0xFF
        time.sleep(0.5)

    # sends  down message for replay
    data = 0                   # AoA DOWN message
    auth = (counter & 0xFF) ^ (LOCAL_KEY & 0xFF)
    down_word = arinc429_sender_40(label, sdi, data, ssm, auth)
    send_word(bus, down_word)
    counter = (counter + 1) & 0xFF
    time.sleep(0.5)

    # sends three more random messages
    for i in range(3):
        data = generate_aoa_data_value()
        auth = (counter & 0xFF) ^ (LOCAL_KEY & 0xFF)
        word = arinc429_sender_40(label, sdi, data, ssm, auth)
        send_word(bus, word)
        counter = (counter + 1) & 0xFF
        time.sleep(0.7)

    bus.shutdown()

if __name__ == "__main__":
    main()
