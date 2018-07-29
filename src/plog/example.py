# Some working samples of plog


CDP_DATA = '''
Device ID: SEP001F9EAB59F1
Entry address(es):
  IP address: 10.243.14.48
Platform: Cisco IP Phone 7941,  Capabilities: Host Phone
Interface: FastEthernet0/15,  Port ID (outgoing port): Port 1
Holdtime : 124 sec

Version :
SCCP41.8-2-1S

advertisement version: 2
Duplex: full
Power drawn: 6.300 Watts
Power request id: 23025, Power management id: 3
Power request levels are:6300 0 0 0 0
Management address(es):
'''

plog = Plog(CDP_DATA)
line = PlogLine(header__istartswith='Device ID')

PlogLine()

PlogBlock()






# Usage putty
f = open('file.txt')
plog = Plog(f)

# Usage Cisco CDP
f = open('file.txt')
cdp = Plog(f)
cdp.whitespace = '|'
cdp.terminator = ','

# First method of creating a block
# Define a line, of which will match the
# block header
device_line = PlogLine('Device ID', ref='device')
# pass the line into a PlogBlock, passing as
# the initial argument for __init__ provides
# the line as the header_line - all arguments thereafter
# are lines to match within the open block
# context
pb = PlogBlock(device_line)
# Finally add the block to all blocks
cdp.add_block(header_block)

# Shortcut version of appliance.
# Define an object within the block namespace.
# The name provided for the variable becomes
# the ref of the psuedo PlogBlock
# The tuple of tuples applied will be in format
#
# (header_line, terminator
#   (line, )
#   (line, )
#  )
#
#  the first value can be a PlogLine,
#  or a tuple of (header_line, terminator_line).
#  Values after are parsed as PlogLinePatterns
#  to match as lines within the block

#  Each line is a PlockLinePattern definition or
#  a tuple for associated types
#  Terminator is optional, pass no
cdp.block.device = ('Device ID')

cdp.block.device = PlogBlockPatten('Device ID')

# To assist in itteration, create
# a block - a repeated element
# within the log


'''
A PlogBlock is a definition for a single
repeated object within your log.
Consider a single bash command:

    $ ls
    foo bar env readme.md app*
'''
#ls_line = PlogLine()
#ls_block = PlogBlock(ls_line, ref='ls')
#cdp.add_block(ls_block)

'''
Parsing logs, may also grab actions to
perform take python [ESC], [BS]
By applying an action to take when
discovering occurances.
[32mjjagpal01@JJAGPALPC01 [33m/cygdrive/c/Users/jjagpal01/Documents/projects/morf[0m
'''


'''
The short syntax allows the feature
to name and define your block within an
inline fashion. This is the same as
passing a PlogBlock

    block - required block PlogBlock style string
    device - becomes PlogBlock ref

Passing a reference PlogBlockPatten
or a tuple shape will be parsed into a working
PlogBlock
    First object will be the block header
cdp.block.device = (
        PlogLine('ls')
    )
'''

# What is Plog

'''
Plog is a simple tool to convert log files into a more digestable format.
Consider a log file for cisco CDP device readouts. By applying a few
simple PlogBlock rules, the file will be converted into a digestable format.

A PlogBlock defines a repeated section of your log - Chunking the data into 
smaller definable bites.

A PlogLine defines a single line to detect within the log. You can also apply
PlogLines to PlogBlocks for a more defined pattern
'''


