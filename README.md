# CYSE465-Caterpillars-Group <br>
This project is aimed at simulating, attacking, and defending the ARINC 429 aviation protocol. <br>
The communication protocol was simuated over VCAN and was attacked using a spoofing, replay, and DoS attack. <br>
Libraries required to run our code are as listed  <br>
can <br>
time <br> 
random <br> 
hashlib <br>
hmac <br>
struct <br>
socket <br>
json <br>
All libraries are native to python aside from CAN <br>
ALL DEMOS MUST HAVE THE LISTED CAN SETUP BEFORE RUNING, FURTHER INSTRUCTIONS ON HOW TO RUN A DEMO WILL BE IN THE SUBFOLDERS  README FILE <br>
 <br> 
in kali terminal run <br> 
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan<br>
sudo modprobe can <br>
