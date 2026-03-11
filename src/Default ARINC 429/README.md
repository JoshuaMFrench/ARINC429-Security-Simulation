# ARINC 429 Base Simulation

This module simulates a basic ARINC 429 avionics communication environment over a virtual CAN (VCAN) interface. It models three avionics components communicating over a shared data bus, demonstrating how real aircraft systems transmit and receive flight data using the ARINC 429 protocol.

---

## Components

| File                 | Role                        | Description                                                                 |
|----------------------|-----------------------------|-----------------------------------------------------------------------------|
| `aoa.py`             | Angle-of-Attack Sensor      | Transmits aviation sensor data (e.g. aircraft orientation) onto the VCAN bus |
| `flightman.py`       | Flight Management System    | Transmits autopilot and flight path data onto the VCAN bus                  |
| `pilot_interface.py` | Pilot Interface / Receiver  | Listens on the VCAN bus and records all incoming messages from both systems |

---

## How It Works

`aoa.py` and `flightman.py` simulate avionics hardware transmitting data over the ARINC 429 protocol. Messages are encoded and sent over a virtual CAN (`vcan0`) interface.

`pilot_interface.py` acts as the receiving end — representing what a pilot-facing display or flight computer would see — and prints all incoming messages to the console as they arrive.

### ARINC 429 Message Structure

All messages are transmitted as **32-bit words**, with each bit range serving a specific purpose:

| Field  | Bits  | Purpose                                                                                          |
|--------|-------|--------------------------------------------------------------------------------------------------|
| Label  | 1–8   | Identifies the data type (e.g. airspeed, altitude, heading)                                      |
| SDI    | 9–10  | Source/Destination Identifier — defines which system is sending and receiving                    |
| Data   | 11–28 | The actual payload value being transmitted                                                       |
| SSM    | 29–30 | Sign/Status Matrix — holds contextual information such as positive/negative values or cardinal direction |
| Parity | 31–32 | Checks for loss or corruption of data during transmission                                        |

This structure ensures every message on the bus is self-describing — the receiving system knows what the data is, where it came from, what it means, and whether it arrived intact, all from a single 32-bit word.

---

## Demo

Running the simulation shows `pilot_interface.py` receiving and displaying real-time messages from both the angle-of-attack sensor and the flight management system over the VCAN bus.

**Left terminal — `pilot_interface.py` receiving messages:**
```
Message Received from Flight Management system
Flight is On Path
Message received from Angle of Attack sensor
Plain is pointing North
Message Received from Flight Management system
Flight is Off Path
Message received from Angle of Attack sensor
Plain is pointing South
Message received from Angle of Attack sensor
Plain is pointing Up
```

**Right terminal — `aoa.py` and `flightman.py` transmitting:**
```
Message Sent!
Message Sent!
Message Sent!
...
```

---

## Setup

> ⚠️ The virtual CAN interface must be running before starting the simulation.

```bash
sudo modprobe can
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0
```

---

## Running the Simulation

Open **two terminals** and run the following:

**Terminal 1 — Start the pilot interface (receiver):**
```bash
python pilot_interface.py
```

**Terminal 2 — Start both transmitters:**
```bash
python aoa.py & python flightman.py
```

Messages will begin appearing in the pilot interface terminal as soon as the transmitters start sending.

---

## Contributors

| Name           | GitHub                                              |
|----------------|-----------------------------------------------------|
| Joshua French  | [@JoshuaMFrench](https://github.com/JoshuaMFrench) |
