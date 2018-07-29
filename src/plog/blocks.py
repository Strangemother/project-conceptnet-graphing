from patterns import PlogLine, PlogBlock

class CDPBlock(object):
	'''Given as a 'block' through PlugBlockMixin.add_block.
	The add_block method looks for the `block` attribute and appends
	it to the running blocks.

	Lines represent each attribute to dicover within the _Start_ and _stop_
	content of a block. Each `PlogLine` extracts an explicitly designed
	value, adding it to the 'lines' of a block.
	A block returns the line value as a dictionary attribute in `Plug.data_block`.
	'''

	# Define a PlogBlock and its starting value.
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
