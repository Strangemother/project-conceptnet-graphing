from api import Plog
from patterns import PlogLine, PlogBlock

f = open('test_data2.txt', 'r')
# Capture something
block = PlogBlock('Device ID:', ref='Device')
block.header.ref='device_id'
block.footer = PlogLine('----------', ref='footer').anything()

ip_address = PlogLine('IP address:')
block.add_lines(ip=ip_address)

# new parser
plog = Plog(f, whitespace='|')
# run it
plog.add_block(block)
blocks = plog.run()

for block in blocks:
	if block.valid():
		print block.as_dict()

