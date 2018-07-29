from pprint import pprint
from api import Plog
from patterns import PlogLine, PlogBlock
from blocks import CDPBlock

f = open('test_data2.txt', 'r')
plog = Plog(f, whitespace='|', terminator=',')
# import pdb; pdb.set_trace()
plog.add_blocks(CDPBlock)
plog.run()

for block in plog.data_blocks:
	if block.valid():
		d = block.as_dict()
		print d

import pdb; pdb.set_trace()
