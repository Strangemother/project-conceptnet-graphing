from api import Plog
from patterns import PlogBlock, PlogLine
# Test file

def test_file_on_init():
    f = open('file')
    plog = Plog(f)
    assert plog.get_file() == f
    assert plog.get_data() == f

def test_add_file():
    f = open('file')
    plog = Plog()
    plog.set_file(f)
    assert plog.get_file() == f
    assert plog.get_data() == f

def test_add_string():
    CDP_DATA = '''
    Device ID: SEP001F9EAB59F1
    Entry address(es):
      IP address: 10.243.14.48
    Platform: Cisco IP Phone 7941,  Capabilities: Host Phone
    Interface: FastEthernet0/15,  Port ID (outgoing port): Port 1
    Holdtime : 124 sec
    '''
    plog = Plog(CDP_DATA)
    assert plog.get_file()

def test_add_block():
    '''
    Add a basic empty block to the plog.blocks
    '''
    plog = Plog()
    block = PlogBlock()
    plog.add_block(block)
    assert len(plog.blocks) == 1

def test_add_block_string():
    '''
    Add a plog block as as a string. This is converted to conform
    into a plog.line for a plog.block
    '''
    plog = Plog()
    plog.add_block('Device')
    assert len(plog.blocks) == 1

def test_line():
    '''Pass a string to the PlogLine,
    it should __eq__ a string correctly.'''
    
    string = 'Device'
    line = PlogLine(string)
    assert line == string

def test_block_header():
    ''' Add the first line to a block and check it's added as a header'''

    line = PlogLine('Device')
    block = PlogBlock(line)
    assert block.header == line

def test_block_header_string_cast():
    '''Plog block is given a string, block.header should exist'''

    block = PlogBlock('Device')
    assert type(block.header) == PlogLine


def test_enumerate():
    '''
    Check to ensure the enumeration of a file or string 
    is exaclty the length of lines for the supplied.
    '''

    CDP_DATA = '''Device ID: SEP001F9EAB59F1
    Entry address(es):
      IP address: 10.243.14.48
    Platform: Cisco IP Phone 7941,  Capabilities: Host Phone
    Interface: FastEthernet0/15,  Port ID (outgoing port): Port 1
    Holdtime : 124 sec'''
    plog = Plog(CDP_DATA)
    plog._c = 0
    def counts(line, line_no):
        plog._c = plog._c + 1

    plog.run(counts)
    assert plog._c == 6