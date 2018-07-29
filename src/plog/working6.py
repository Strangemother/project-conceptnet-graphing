from api import Plog
from patterns import PlogLine as Line, PlogBlock as Block


block = Block('Device ID:', ref='Device')
block.header.ref='device_id'

block.add_lines(
    entry_address=Line('IP address:'),
    platform=Line('Platform:'),
    interface=Line('Interface:'),
    hold_time=Line('Holdtime').maybe(' ').then(':'),
    version=Line('Version').maybe(' ').then(':').multiline(),
    ad_version=Line('advertisement version:'),
    duplex=Line('Duplex:'),
    power_drawn=Line('Power drawn:'),
    power_request_id=Line('Power request id:'),
    power_management_id=Line('Power management id:'),
    power_request_levels=Line('Power request levels are:'),
)

block.footer = Line('----------', ref='footer').anything()


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

