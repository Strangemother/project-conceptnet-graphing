from api import Plog
from patterns import PlogLine, PlogBlock


block = PlogBlock('Device ID:', ref='Device')
block.header.ref='device_id'
block.footer = PlogLine('----------', ref='footer').anything()


lines = {}
lines['entry_address'] = PlogLine('IP address:')
lines['platform'] = PlogLine('Platform:')
lines['interface'] = PlogLine('Interface:')
lines['hold_time'] = PlogLine('Holdtime').maybe(' ').then(':')
lines['version'] = PlogLine('Version').maybe(' ').then(':').multiline()
lines['version'] = PlogLine('advertisement version:')
lines['duplex'] = PlogLine('Duplex:')
lines['power_drawn'] = PlogLine('Power drawn:')
lines['power_request_id'] = PlogLine('Power request id:')
lines['power_management_id'] = PlogLine('Power management id:')
lines['power_request_levels'] = PlogLine('Power request levels are:')
block.add_lines(**lines)


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

