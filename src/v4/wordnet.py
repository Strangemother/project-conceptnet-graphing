'''Use berkley key assoc exe app as a data input by reading STDOUT of a windows
cli tool.'''

import os
import subprocess
import plog
from plog.api import Plog
from plog.patterns import PlogLine, PlogBlock
from .typemap import noun, verb, adj, attrs, adv


NOUN = tuple(noun.keys())
VERB = tuple(verb.keys())
ADJ = tuple(adj.keys())
ADV = tuple(adv.keys())
ALL = list(NOUN + VERB + ADJ + ADV)


APP_PATH = "C:/Program Files (x86)/WordNet/2.1/bin/wn"
OUTPUT_DIR = "C:\\Users\\jay\\Documents\\projects\\context-api\\context\\src\\data\\wordnet"


def get_word(word, *a, app_path=None, output_dir=None, kws=ALL, **kw):
    res = caller(list(kws), app_path=app_path, output_dir=output_dir)(word, *a, **kw)
    #res = process_call_value(str_res)
    return res


def caller(params=None, app_path=None, output_dir=None):
    """Produce a call to the wordnet app using command run.
    provide a list of seitches (without prefix char);
    Return a partial function to call:

        method = caller( ('grepa', 'ants',) )
        method(word)
    """
    params = params or []
    app_path = app_path or APP_PATH
    out_base = output_dir or OUTPUT_DIR

    def perform_call(word, additional_params=None, to_file=None):
        ams = additional_params or []
        items = list(set(params + ams))

        switches = ' -'.join(items)
        ps = hash('-'.join(params))
        filename = "{}-{}.txt".format(word, ps)

        if to_file is True:
            to_file = filename

        out_file = to_file

        list_switches = ['-' + x for x in list(set(params + ams))]
        out = os.path.join(out_base, filename)
        st = '"{app}" {word} -{switches} > "{out}"'
        call_str = st.format(app=app_path,
                             word=word,
                             switches=switches,
                             out=out)
        cmds = [app_path, word] + list_switches

        if out_file is None:
            out_file = os.path.abspath(out)
        elif to_file is not False:
            #out_file = os.path.abspath(to_file)
            out_file = os.path.join(out_base, to_file)

        if (to_file is not False) and (out_file is not None):
            cmds += ['>', out_file]

        print("Running: \n{}\n".format(' '.join(cmds)))

        op = None
        #if out_file is None:
        op = subprocess.PIPE
        # py 3.7
        # res = subprocess.run([call_str], capture_output=True)
        proc = subprocess.run(cmds, stdout=op, timeout=5, shell=True, stderr=subprocess.PIPE)
        res = process_call_value(word, proc)
        return res

    return perform_call


def process_call_value(word, complete_process):

    # print(complete_process.returncode)
    # print(complete_process.args)
    # print('Out len:', len(complete_process.stdout))
    # print('error:', complete_process.stderr)
    string = complete_process.stdout
    if (isinstance(string, bytes) is True) and len(string) == 0:
        filepath = complete_process.args[-1]
        print('File input detected', filepath)
        with open(filepath) as stream:
            data = stream.readlines()
    else:
        data = complete_process.stdout.split('\n')

    return destructure(word, data)
    # return data


def destructure(word, lines):
    print('destructure', word)

    mblocks = tuple(BLOCKS[n](word) for n in BLOCKS)
    # open all blocks
    # iterate line
    # find detection
    #  match to a block and feed into the matching block until break
    #  alert any missed lines (should be entire blocks)
    # Break on new line into detection mode.
    focus_block = None
    match_mode = False

    for index, line in enumerate(lines):
        line = line.rstrip()
        if match_mode:
            # Feed to the block until it returns false.
            # False for continue to the next blocks as a check.
            print('    feeding:', index, focus_block.__class__.__name__, line)
            # time.sleep(.1)
            match_mode = focus_block.feed(line)
            if match_mode:
                continue
            else:
                print('detach from', focus_block)

        # time.sleep(1)

       # print('detecting line', index, line)
       #  print([x.match(line) for x in mblocks])

        for block in mblocks:
            # print('{}, {}'.format(index, block.__class__.__name__))
            if block.match(line):
                print('Match block', index, block)
                match_mode = True
                focus_block = block
    return focus_block

import re
import time


class BlockStructure(object):
    pattern = (r"{word}", re.IGNORECASE)

    def __init__(self, word):
        self.word = word
        self.lines = ()
        self._compile = self.get_compile()

    def get_compile(self):
        pattern = self.get_pattern(self.word)
        print(pattern)
        return re.compile(*pattern)

    def get_pattern(self, word):
        s, *a = self.pattern
        pf = self.pattern_format(word)
        fp = s.format(**pf)
        return tuple([fp] + a)

    def pattern_format(self, word):
        return { 'word': word }

    def feed(self, line):
        """Continue with feeding a block parsing after a match
        Return boolean as match_mode to continue feeding.
        """
        self.lines += (line, )
        if len(line) == 0 and len(self.lines) > 1:
            return False
        return True

    def match(self, line):
        result = False
        match = self._compile.match(line)
        if match:
            self._last_match_start = match.group()
        return match


BLOCKS = {}


def register(cls):
    """
    """
    print('Registering {}'.format(cls))
    BLOCKS[cls.__name__] = cls


class AutoRegister:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register(cls)


class WordnetBase(BlockStructure):
    part = ""
    pattern = (r"{part}(\w*) {word}", re.IGNORECASE)

    def pattern_format(self, word):
        return {'word': word, 'part': self.part}


class GrepBlock(WordnetBase, AutoRegister):
    part = "Grep of "
    # Grep of noun duck
    # Grep of verb duck
    # Grep of adj duck
    #pattern = (r"Grep of (\w*) {word}", re.IGNORECASE)


class HolonymBlock(GrepBlock):
    # Substance Holonyms of noun duck
    # Member Holonyms of noun duck
    # Part Holonyms of noun duck
    # Holonyms of noun duck
    # Holonyms of noun duck
    part = r"(\w*.){0,1}([ ]{0,1})Holonyms of "


class DomainTermsBlock(GrepBlock):
    part = r"Domain Terms of "


class FamiliarityBlock(GrepBlock):
    part = r"Familiarity of "


class EntailmentBlock(GrepBlock):
    part = r"Entailment of "


class SynonymsBlock(GrepBlock):
    part = r"Synonyms of "


class SynonymsHypernyms(GrepBlock):
    part = r"Synonyms/Hypernyms (Ordered by Estimated Frequency) of "


class CoordinateTerms(GrepBlock):
    part = r"Coordinate Terms (sisters) of "


class Troponyms(GrepBlock):
    part = r"Troponyms (hyponyms) of "


class Overview(GrepBlock):
    part = r"Overview of "


class MemberMeronyms(GrepBlock):
    part = r"Member Meronyms of "


class SampleSentences(GrepBlock):
    part = r"Sample Sentences of "


class PartMeronyms(GrepBlock):
    part = r"Part Meronyms of "


class Meronyms(GrepBlock):
    part = r"Meronyms of "


class Hyponyms(GrepBlock):
    part = r"Hyponyms of "


class Antonyms(GrepBlock):
    part = r"Antonyms of "



