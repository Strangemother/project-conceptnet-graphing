from io import StringIO
from plog import patterns

class MixinBase(object):
    ''' Base mixin object of all Plog Mixins to inherit'''
    def __init__(self, *args, **kwargs):
        pass

class PlogFileMixin(MixinBase):
    '''
    A PlogFileMixin is designed to wrap a file object to
    represent correctly for enumeration. You can pass a string or
    a file object.
    Strings are converted to StringIO.StringIO before use.
    Pass this to the class for easy get_file, set_file methods
    '''
    def __init__(self, *args, **kwargs):
        ''' initial file can be given '''
        self._file = None
        self._data = None

        if len(args) > 0:
            ''' could be file or string'''
            self.set_data(args[0])

        super(PlogFileMixin, self).__init__(*args, **kwargs)

    def set_file(self, log_file):
        ''' Add a file to the class to parse
        This will return a StringIO if a string
        was passed as data.'''
        self.set_data(log_file)

    def set_data(self, data):
        ''' wrapper for applying the file content
        to the class'''
        if type(data) == str:
            output = StringIO.StringIO(data)
            self._data = output
        else:
            self._data = data

    def get_data(self):
        return self._data

    def get_file(self):
        ''' return the internal file,
        This will return a StringIO if a string
        was passed as data
        '''
        return self.get_data()


class PlogBlockMixin(MixinBase):
    '''
    Methods to assist block design on on a class
    '''
    def __init__(self, *args, **kwargs):
        self._blocks = []
        super(PlogBlockMixin, self).__init__(*args, **kwargs)

    def blocks():
        doc = "The blocks property."
        def fget(self):
            return self._blocks
        def fset(self, value):
            self._blocks = value
        def fdel(self):
            del self._blocks
        return locals()
    blocks = property(**blocks())

    def block_match(self, block, line, string, reg):
        '''
        Method called upon a successfull match of a block
        header

        block {PlogBlock} - The block containing the matched PlogLine
        line {PlogLine} - PlogLine matched
        string {str} - String matched from file
        reg {regex} - Regex SRE match object (if it exists)
        '''

        #print '> Block', block
        #print '  Match', line
        #print '  Found', string, '\n'

    def compile_blocks(self):
        '''Call each block to compile as needed'''
        for block in self.blocks:
            block.compile()

    def close_all_blocks(self):
        '''
        Close any dangling blocks (blocks open at the end of parsing)
        and return a list of closed blocks.
        '''
        closed =[]
        for block in self.blocks:
            if block.is_open:
                print('force close', block.ref)
                closed.append(block)
                block.close()
        return closed

    def add_blocks(self, *args):
        '''
        Add a list of blocks to append

            add_blocks(block1, block2, block3, ... )
            add_blocks(*blocks)
        '''
        for block in args:
            self.add_block(block)

    def add_block(self, block):
        '''
        Append a plog block to all valid blocks.
        '''
        _block = block
        if type(block) == str:
            _block = patterns.PlogBlock(block)
        elif hasattr(_block, 'block'):
            _block = _block.block

        self._blocks.append(_block)

    def get_blocks_with_header(self, *args):
        '''
        Pass one or many PlogLines and return all matching
        blocks with the headers of that type.
        '''

        header_line = args[0]
        # Loop blocks.
        _blocks = []

        for block in self.blocks:
            mtch, reg = block.header.match(header_line)
            if mtch:
                _blocks.append(block)
                self.block_match(block, block.header, header_line, reg)
        return _blocks

    def get_blocks_with_header_footer(self, *args):
        '''
        Pass one or many PlogLines and return all matching
        blocks with the headers of that type.
        '''

        mline = args[0]
        # Loop blocks.
        _blocks = []

        mtch = None
        mtch_f = None
        reg = None
        reg_f = None

        for block in self.blocks:
            if block.header:
                mtch, reg = block.header.match(mline)

            if block.footer:
                mtch_f, reg_f = block.footer.match(mline)

            if mtch_f or mtch:
                _blocks.append(block)

            if mtch:
                self.block_match(block, block.header, mline, reg or reg_f)

            if mtch_f:
                self.block_match(block, block.footer, mline, reg or reg_f)


        return (_blocks, True if mtch else False, )


