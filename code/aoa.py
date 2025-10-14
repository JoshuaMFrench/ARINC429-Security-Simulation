import random
import can
import time
def compute_odd_parity(word_31bits: int) -> int:
	#compute ARINC 429 odd parity bit
	ones_total = bin(word_31bits).count('1')
	return 1 if ones_total %2 == 0 else 0

def arinc429_sender(label: int, sdi: int, data: int, ssm: int) -> int:

	#packs message into 32 bit word
	""" Format
	1-8: label
	9-10 SDI
	11-29 Data
	30-31 SSM
	32 Parity bit
	"""
	word = (label & 0xFF)
	word |=(sdi & 0x3) << 8
	word |= (data& 0x7FFFF) <<10
	word |= (ssm& 0x3) << 29

	#compute parity bit
	parity = compute_odd_parity(word)
	word |= (parity <<31) # add parity bit
	return word

def send_word(word):
	bus = can.interface.Bus(channel='vcan0', interface='socketcan')
	#convert 32 digit int into 4 bytes in big endian
	data_bytes = word.to_bytes(4,byteorder ='big')
	msg = can.Message(
		arbitration_id=0x100, #Arinc has no arbitrarion so all sending messages will be on the same arbitrarion to simulate no priority
		data=data_bytes,
		is_extended_id = False
	)
	try:
		bus.send(msg)
		print("Message Sent!")
	except can.CanError:
		print("Message NOT sent!")
	bus.shutdown()

def generate_random_word(data_overide=None):
	label=0x00
	sdi = 0x3
	data= random.randint(0, 0x7FFFF) if data_overide is None else data_overide # random 19 bits or overiden data
	ssm = random.randint(0, 0x3) # random 2 bits
	word = arinc429_sender(label, sdi,data,ssm)
	return word

def main():
	for i in range(4):
		word = generate_random_word()
		send_word(word)
		time.sleep(.25)
	send_word(generate_random_word(data_overide=0))

main()
	

