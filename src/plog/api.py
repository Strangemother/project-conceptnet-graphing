'''
Plog.

The api reads through the given file, provided starters, terminators
and key value pair definitions, output it parsed
and applied to an object - later passed through the
api into the django model

Usage:
    api.py

Options:
    --pre-compile=False Optionally don't complile string patterns before use
'''
#import docopt
from plog import mixins
from plog.patterns import PlogLine, PlogBlock
from termcolor import colored
import sys


try:
    from colorama import init
    init()
except: pass


class Plog( mixins.PlogFileMixin,
            mixins.PlogBlockMixin):

    EMPTY_LINE = '\r\n'

    # Set the whitespace character
    whitespace = ' '

    # A file is read as each line
    # But many commands can be passed
    # into a line.
    terminator = ';'

    def __init__(self, *args, **kwargs):
        self.open_box = None
        self.hash_state = {}
        self.line_count = 0
        self.data_blocks = []
        self.open_blocks = {}
        self.terminator = kwargs.get('terminator', self.__class__.terminator)
        self.whitespace = kwargs.get('whitespace', self.__class__.whitespace)
        super(Plog, self).__init__(*args, **kwargs)

    def run(self, parser=None):
        '''
        Begin the process, working the passed
        file. Pass an enumerator method to
        call on each line detection
        '''

        if parser is None:
            parser = self.parse_line

        self.compile_blocks()

        _file = self.get_file()
        line_no = 0
        for line in _file:
            line_no += 1
            clean = self.clean_line(line)
            for cl in clean:
                parser(cl, line_no=line_no)
        self.close_data_blocks( *self.close_all_blocks() )
        return self.data_blocks

    def clean_line(self, line, strip=True):
        '''
        Return a value of clean information for a single line
        from the file
        '''
        stripped = line[:-1]
        cleaned_line = stripped.replace(self.whitespace, ' ')
        split_line = cleaned_line.split(self.terminator)
        splits = []
        for s in split_line:
            splits.append(s.strip())
        return splits

    def close_data_blocks(self, *args):
        '''
        Safely close the open block and remove from open block elements.
        Add data block to
        return the data blocks
        '''
        dbs = []
        for block in args:
            # import pdb; pdb.set_trace()
            if block.is_open:
                block.close()
            data_block = self.open_blocks[block]
            self.data_blocks.append(data_block)
            dbs.append(data_block)
            self.open_blocks[block] = None
        return dbs

    def parse_line(self, line, *args, **kwargs):
        '''
        method is passed to the run and receives
        a single line string to parse and apply PlogLine
        and PlogBlock
        '''
        # Make a plog line.
        pline = PlogLine(line, line_no=kwargs.get('line_no', -1))

        self.line_count += 1
        # Find header_line blocks matching this pline
        blocks, is_header = self.get_blocks_with_header_footer(pline)
        # one or more blocks detected
        pr = ''

        for block in blocks:
            if block.is_open is not True and is_header:
                block.open()
                bl = PlogBlock(ref=block)
                bl.header = block.header
                bl.footer = block.footer
                bl.lines = block.lines
                bl.line_refs = block.line_refs
                bl.open_lines = block.open_lines

                self.open_blocks[block] = bl
                pr = '#%s+' % colored(pline.line_no, 'grey')
            else:
                if block in self.open_blocks and is_header is not True:
                    self.open_blocks[block].add_data(pline)
                    data_blocks = self.close_data_blocks(block)

                    pr = colored('-', 'red')

                    s = '~%s#%s' % (
                            colored(len(data_blocks), 'grey'),
                            colored(pline.line_no, 'grey'),
                        )
                    # sys.stdout.write(s)

        for block in self.open_blocks:
            if block.is_open:
                added = self.open_blocks[block].add_data(pline)
                v =  colored('_', 'grey')
                if added is not True:
                    if pline.value != '':
                        v =  colored('_', 'red')
                        self.open_blocks[block].add_missed(pline)
                    else:
                        v = ''
                pr = '%s%s' % (pr, v)

        bl = len(blocks)
        if bl > 0:
            ct = ( colored('[', 'grey'), colored('%s' % bl, 'white'), colored(']', 'grey'), )
            d = "%s%s%s" % ct
            # sys.stdout.write(d)
        # sys.stdout.write(pr)
