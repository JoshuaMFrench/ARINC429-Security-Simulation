# CYSE465-Caterpillars-Group
This project is aimed at simulating, attacking, and defending the ARINC 429 aviation protocol.
The communication protocol was simuated over VCAN and was attacked using a spoofing, replay, and DoS attack.
Libraries required to run our code are as listed 
can
time
random
hashlib 
hmac
struct
socket
json
All libraries are native to python aside from CAN
ALL DEMOS MUST HAVE THE LISTED CAN SETUP BEFORE RUNING, FURTHER INSTRUCTIONS ON HOW TO RUN A DEMO WILL BE IN THE SUBFOLDERS README FILE

in kali terminal run
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan
sudo modprobe can
