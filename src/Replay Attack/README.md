# Replay Attack & Defense

This module demonstrates a replay attack against the ARINC 429 base simulation and a two layer defense that prevents it. The attack targets the Flight Management System by exploiting the lack of message authentication in the base protocol, while the defense introduces cryptographic authentication and message ordering to detect and drop replayed messages.

---

## How the Attack Works

The replay attack is implemented as a malicious Flight Management System (`mal_FMS.py`) that runs alongside the legitimate avionics components. Rather than generating its own data, it acts as a passive listener on the VCAN bus, waiting for a specific message from the Angle of Attack sensor specifically, the message indicating that the **plane is pointing down**.

Once that message is captured, `mal_FMS.py` immediately replays it hundreds of times in rapid succession. From the pilot interface's perspective, it appears as though the aircraft is in a continuous downwards attitude. Simulating what a pilot would interpret as the plane crashing.

This attack is particularly dangerous because the messages are **valid and correctly formatted** and originated from a legitimate sensor. The base protocol has no way to distinguish a genuine message from a replayed one.

---

## How the Defense Works

The defense is implemented across a new set of secure files (`secure_aoa.py`, `secure_FMS.py`, `secure_pilot_interface.py`) and operates in two stages:

### Stage 1 — HMAC Authentication
Each message is signed using an **HMAC (Hash based Message Authentication Code)** before being transmitted. The receiving system verifies the signature before accepting the message. This ensures that only messages from a known, authenticated source are processed, stopping spoofed or forged messages outright.

### Stage 2 — Nonce-Based Ordering
To counter replay attacks specifically, a **nonce** (a one-time-use counter) is embedded into each message. The nonce tracks the expected order of messages, the receiver knows what sequence number to expect next, and any message arriving with an out of order or repeated nonce is immediately dropped.

To accommodate the nonce, the 32-bit ARINC 429 word is extended with an additional **8 bit nonce field**, incorporated into the message structure alongside the existing label, SDI, data, SSM, and parity fields.

Together, these two layers mean that even if an attacker captures a valid, authenticated message and attempts to replay it, the nonce check will detect that the sequence number has already been used and reject it.

---

## Demo

**Attack — `mal_FMS.py` flooding the pilot interface with replayed nose-down messages:**

Right terminal shows `mal_FMS.py` capturing an AoA message and replaying it repeatedly:
```
Received AoA zero message — starting replay flood...
Message Sent From Malicious FMS!
Message Sent From Malicious FMS!
Message Sent From Malicious FMS!
...
```

Left terminal shows `pilot_interface.py` being overwhelmed with nose-down readings:
```
Message received from Angle of Attack sensor
Plain is pointing Down
Message received from Angle of Attack sensor
Plain is pointing Down
Message received from Angle of Attack sensor
Plain is pointing Down
...
```

---

**Defense — replayed messages detected and dropped by nonce validation:**

Right terminal shows `mal_FMS.py` successfully capturing and replaying a message, but the defense catching it:
```
[mal_FMS] Captured message #8 for replay!
[mal_FMS]: Replayed frame 100 times!
```

Left terminal shows `secure_pilot_interface.py` authenticating legitimate messages and dropping all replayed ones:
```
[Pilot] Learned key from SDI=0: 0xF3
[Pilot] Learned key from SDI=1: 0x15
[Pilot] AoA (authenticated): plane pointing West
[Pilot] FMS (authenticated): Flight is On Path
[Pilot] Message FAILED nonce check: got nonce=1, expected=2. DROPPED.
[Pilot] Message FAILED nonce check: got nonce=1, expected=2. DROPPED.
[Pilot] Message FAILED nonce check: got nonce=1, expected=2. DROPPED.
...
```

The 100 replayed frames are all rejected — the pilot interface only ever sees legitimate, authenticated messages.

---

## Setup

> The virtual CAN interface must be running before starting the simulation.

```bash
sudo modprobe can
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0
```

---

## Running the Attack

Open two terminals:

**Terminal 1 — Start the pilot interface:**
```bash
python pilot_interface.py
```

**Terminal 2 — Start the legitimate transmitters alongside the malicious FMS:**
```bash
python aoa.py & python flightman.py & python mal_FMS.py
```

---

## Running the Defense

Open two terminals:

**Terminal 1 — Start the secure pilot interface:**
```bash
python secure_pilot_interface.py
```

**Terminal 2 — Start the secure transmitters alongside the malicious FMS:**
```bash
python secure_aoa.py & python secure_FMS.py & python mal_FMS.py
```

Replayed messages will appear as failed nonce checks and be dropped automatically.

---

## Contributors

| Name          | GitHub                                             | Contributions          |
|---------------|----------------------------------------------------|------------------------|
| Joshua French | [@JoshuaMFrench](https://github.com/JoshuaMFrench) | Replay attack & defense |
