from api import Plog
from patterns import PlogLine, PlogBlock


#
block = PlogBlock('Device ID:', ref='Device')
block.header.ref='device_id'

block.footer = PlogLine('----------', ref='footer').anything()

lines = {}
lines['entry_address'] = PlogLine('IP address:')
lines['platform'] = PlogLine('Platform:')
lines['interface'] = PlogLine('Interface:')
lines['hold_time'] = PlogLine('Holdtime').maybe(' ').then(':')
lines['version'] = PlogLine('Version').maybe(' ').then(':').multiline()
lines['ad_version'] = PlogLine('advertisement version:')

block.add_lines(**lines)


# new parser
f = open('test_data2.txt', 'r')
plog = Plog(f, whitespace='|')
# run it
plog.add_block(block)
blocks = plog.run()

for block in blocks:
	if block.valid():
		print block.as_dict()

