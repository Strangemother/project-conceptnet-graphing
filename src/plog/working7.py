from api import Plog
from patterns import PlogLine, PlogBlock as Block


block = Block('Device ID:', ref='Device')
#block.header.ref='device_id'

line = PlogLine(ref='ip')
line.startswith('IP address:')
block.add_line(line)

block.footer = PlogLine('----------', ref='footer').anything()

# new parser
f = open('test_data2.txt', 'r')
# plog = Plog(f, whitespace='|')
plog = Plog(f, whitespace='|', terminator=',')

# run it
plog.add_block(block)
blocks = plog.run()

for block in blocks:
	if block.valid():
		print block.as_dict()

