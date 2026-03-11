# Spoofing Attack & Defense

This module demonstrates a spoofing attack against the ARINC 429 base simulation and an HMAC based defense that detects and rejects forged messages. The attack targets the airspeed data being transmitted to the pilot display, injecting false values designed to trigger dangerous flight warnings.

---

## How the Attack Works

The spoofing attack is implemented in `Speed daya attack simulator(terminal 3).py` as a malicious transmitter that injects fake airspeed messages directly onto the VCAN bus and to the pilot display simultaneously.

The attacker sends forged messages with fabricated airspeed values — ranging from dangerously low to well above the normal operating range of 450–520 knots. Each message includes a fake HMAC signature attempting to impersonate a legitimate sensor. Since the base protocol has no way to verify message authenticity, the pilot display accepts these messages at face value and raises false alarms:

- Speeds **below 450 knots** trigger a `LOW AIRSPEED WARNING`
- Speeds **above 520 knots** trigger an `OVERSPEED WARNING`

From the pilot's perspective, the aircraft appears to be in a dangerous condition when it is not, a potentially catastrophic result in a real avionics system.

---

## How the Defense Works

The defense uses **HMAC (Hash-based Message Authentication Code)** to cryptographically authenticate every message before it is accepted.

### Authentication Flow
1. The legitimate sender (`SecureARINC429`) generates an HMAC signature using a **shared secret key** and the airspeed value, producing a 16-character digest via SHA-256
2. The signature is embedded in the message alongside the data
3. The secure bus monitor (`SecureMonitor`) recomputes the expected HMAC on receipt and compares it against the received signature using a timing-safe comparison (`hmac.compare_digest`) to prevent timing attacks
4. If the signatures match, the message is accepted as valid
5. If they do not match — as is the case with the attacker's fake HMAC and the message is flagged and rejected

Since the attacker does not have the shared secret key, any HMAC they provide will fail verification. The fake SHA-256 hash embedded in the attack messages is simply ignored.

---

## Files

| File                                        | Role                                      |
|---------------------------------------------|-------------------------------------------|
| `Speed daya attack simulator(terminal 3).py`| Spoofing attacker — injects fake airspeed |
| `Pilot Display (Terminal 2).py`             | Unsecured pilot display (attack demo)     |
| `ARINC 429 Bus Monitor (Terminal 1).py`     | Secure bus monitor with HMAC verification |
| `pilotmac.py`                               | Secure pilot display (defense demo)       |

---

## Setup

>  The virtual CAN interface must be running before starting the simulation.

```bash
sudo modprobe can
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0
```

---

## Running the Attack

Open two terminals:

**Terminal 1 — Start the unsecured pilot display:**
```bash
python "Pilot Display (Terminal 2).py"
```

**Terminal 2 — Launch the spoofing attack:**
```bash
python "Speed daya attack simulator(terminal 3).py"
```

The pilot display will begin receiving and displaying the fake airspeed values, triggering low airspeed and overspeed warnings.

---

## Running the Defense

Open two terminals:

**Terminal 1 — Start the secure bus monitor:**
```bash
python "ARINC 429 Bus Monitor (Terminal 1).py"
```

**Terminal 2 — Launch the spoofing attack:**
```bash
python "Speed daya attack simulator(terminal 3).py"
```

The secure monitor will authenticate incoming messages, accept only those with a valid HMAC, and flag all spoofed messages as rejected.

---

## Contributors

| Name           | GitHub                                               | Contributions            |
|----------------|------------------------------------------------------|--------------------------|
| Elnatan Belay  | [@NEGUSNATE12](https://github.com/NEGUSNATE12)       | Spoofing attack & defense |
