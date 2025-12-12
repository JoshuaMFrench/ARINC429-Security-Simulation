import can
import time
import random
def arinc429_receive(word: int) -> dict:

	"""
	unpacks 32 bit ARINC word 
	returns a dictinary describing the inputs
	"""
	parity = (word >> 31) & 0x1
	ssm =(word >> 29) & 0x3
	data = (word >> 10) & 0x7FFFF
	sdi = (word >> 8) & 0x3
	label = word & 0xFF

	return {
	"parity": format(parity, "1b"),
	"ssm":format(ssm, "02b"),
	"data": format(data, "019b"),
	"sdi": format(sdi, "02b" ),
	"label": format(label, "08b")
	}

def receive_msg(duration=10):
	bus = can.interface.Bus(channel='vcan0',interface ='socketcan')
	start_time = time.time()
	direction = ["North", "East", "South", "West", "Up"]
	path = ["On","Off"]
	while time.time() - start_time < duration:
		msg=bus.recv(timeout=1)
		if msg:
			word = int.from_bytes(msg.data,byteorder ='big')
			decoded = arinc429_receive(word)

			label = decoded["label"]
			data = decoded["data"]
			if label == "00000000":
				print("Message received from Angle of Attack sensor")
				if data == "0000000000000000000":
					print("Plain is pointing Down")
				else:
					print(f"Plain is pointing {direction[random.randint(0,4)]}")
			elif label == "11111111":
				print("Message Received from Flight Management system")
				print(f"Flight is {path[random.randint(0,1)]} Path") 

			else:
				print(f"Message recived with label {label}")
			print(f"Message: {decoded}")
	bus.shutdown()

receive_msg()
