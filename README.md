# ARINC 429 Security Simulation

A simulation of the ARINC 429 aviation communication protocol with implemented attack vectors and corresponding software-based defenses. Built to identify vulnerabilities in avionics data bus communications and demonstrate practical mitigation strategies.

---

## Overview

ARINC 429 is the primary data bus standard used in commercial and transport aircraft, governing how avionics systems communicate. This project simulates the protocol over a virtual CAN (VCAN) interface, implements three real world attack scenarios against it, and provides working defenses for each.

The goal is to demonstrate how legacy aviation protocols can be vulnerable to modern network attacks, and how those vulnerabilities can be addressed in software.

---

## Attack Vectors

| Attack    | Description                                              | Defense Implemented |
|-----------|----------------------------------------------------------|---------------------|
| Spoofing  | Injecting forged ARINC 429 messages onto the data bus   |  HMAC-based message authentication |
| Replay    | Capturing and retransmitting valid messages maliciously  |  Timestamp + sequence validation    |
| DoS       | Flooding the bus to disrupt legitimate communications    |  Rate limiting and message filtering |

---

## Project Structure

```
ARINC429-Security-Simulation/
├── README.md
├── LICENSE
├── src/
│   ├── arinc429/               # Base ARINC 429 protocol simulation
│   ├── spoofing/               # Spoofing attack and defense
│   │   └── README.md           # Run instructions
│   ├── replay/                 # Replay attack and defense
│   │   └── README.md           # Run instructions
│   └── dos/                    # DoS attack and defense
│       └── README.md           # Run instructions
├── models/                     # SysML architecture models
└── docs/                       # Reference documentation and reports
```

---

## Prerequisites

### System Requirements
- **OS:** Kali Linux (or any Linux distro with CAN support)
- **Python:** 3.x

### Python Libraries

All libraries are Python-native **except `can`**, which requires installation:

```bash
pip install python-can
```

Native libraries used (no installation needed):
`timer` · `random` · `hashlib` · `hmac` · `struct` · `socket` · `json`

---

## Setup — Virtual CAN Interface

>  **This must be run before any demo.** All simulations communicate over a virtual CAN interface (`vcan0`).

Open a terminal and run:

```bash
sudo modprobe can
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0
```

Verify the interface is up:

```bash
ip link show vcan0
```

---

## Running the Simulations

Each attack and defense module has its own `README.md` with specific run instructions. Navigate to the relevant subfolder to get started:

```
src/spoofing/README.md
src/replay/README.md
src/dos/README.md
```

Start with the base simulation before running any attack:

```bash
python src/arinc429/simulation.py
```

---

## Tech Stack

- **Python 3** — Protocol simulation and attack/defense implementation
- **Virtual CAN (VCAN)** — Simulated avionics data bus
- **SysML** — System architecture modeling
- **python-can** — CAN bus interface library

---

## Contributors

Built as a collaborative academic project exploring cybersecurity vulnerabilities in aviation communication systems.

| Name             | GitHub                                                  | Contributions                          |
|------------------|---------------------------------------------------------|----------------------------------------|
| Joshua French    | [@JoshuaMFrench](https://github.com/JoshuaMFrench)     | Base simulation, Replay attack         |
| Elnatan Belay    | [@NEGUSNATE12](https://github.com/NEGUSNATE12)         | Spoofing attack                        |
| Brandon Matthew Tiet | [@btiet88-beep](https://github.com/btiet88-beep)   | DoS attack                             |


---

## License

This project is licensed under the terms described in the [LICENSE](LICENSE) file.
