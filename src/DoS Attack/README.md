# DoS (Denial of Service) Attack

This module demonstrates a Denial of Service attack against an ARINC 429 altitude reporting system. The attack floods the pilot interface with junk data packets, overwhelming the receiver and disrupting the display of legitimate altitude readings.

---

## How the Attack Works

The DoS attack is implemented in `dos_term.py` as a high-frequency UDP packet flooder. It targets the same port as the pilot interface and sends **100 packets per second** for 5 seconds, each containing a randomly generated out-of-range altitude value flagged as `junk_dos`.

The pilot interface (`pilot_interface.py`) has a built in DoS detection mechanism that monitors incoming message rate. If more than **10 messages arrive within a 0.1 second window**, it raises a flood alert:

```
***INCOMING DATA FLOOD DETECTED***
```

While the detection triggers an alert, the interface continues processing all incoming packets — meaning legitimate altitude data is buried under the flood of junk messages, effectively denying the pilot a clean, reliable display.

### Why This Is Dangerous

In a real avionics environment, a pilot relying on altitude data to navigate terrain, approach, or maintain separation from other aircraft could be dangerously misled if that data stream is disrupted or overwhelmed. Even a brief loss of reliable altitude readings can be critical.

---

## Files

| File                  | Role                                                        |
|-----------------------|-------------------------------------------------------------|
| `ARINC_data_bus.py`   | Legitimate ARINC 429 altitude sender                        |
| `dos_term.py`         | DoS attacker — floods the pilot interface with junk packets |
| `pilot_interface.py`  | Pilot altitude display with basic DoS rate detection        |

---

## Setup

>  The virtual CAN interface must be running before starting the simulation.

```bash
sudo modprobe can
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0
```

---

## Running the Attack Demo

Open two terminals:

**Terminal 1 — Start the pilot interface:**
```bash
python pilot_interface.py
```

**Terminal 2 — Launch the DoS attack:**
```bash
python dos_term.py
```

The pilot interface will detect the incoming flood and print a warning. The attack runs for 5 seconds and reports the total number of packets sent on completion.

---

## Known Limitations

There is currently **no defense implementation** for this attack vector. A future defense expansion would include **rate limiting** to cap the number of messages accepted per time window, and **illegitimate message filtering** to reject packets that do not conform to the expected ARINC 429 message structure — ensuring junk data is dropped before it ever reaches the pilot display.

---

## Contributors

| Name                 | GitHub                                             | Contributions  |
|----------------------|----------------------------------------------------|----------------|
| Brandon Matthew Tiet | [@btiet88-beep](https://github.com/btiet88-beep)  | DoS attack     |
