import re
class MixinBase(object):
    ''' Base mixin object of all Plog Mixins to inherit'''
    def __init__(self, *args, **kwargs):
        pass

class PlogBlockRefMixin(MixinBase):

    def __init__(self, *args, **kwargs):
        self._ref=None
        super(PlogBlockRefMixin, self).__init__(*args, **kwargs)

    def ref():
        doc = "The ref property."
        def fget(self):
            return self.get_ref()
        def fset(self, value):
            self.set_ref(value)
        def fdel(self):
            del self._ref
        return locals()
    ref = property(**ref())

    def set_ref(self, value):
        # import pdb; pdb.set_trace()
        if type(value) == PlogBlock:
            value = value.ref
        self._ref = value

    def get_ref(self):
        return self._ref


class PlogBlockLineMixin(PlogBlockRefMixin):
    ''' Mixin to help line acceptance on an object'''

    def __init__(self, *args, **kwargs):
        self.open_lines = {}
        self._header_line = None
        self._footer_line = None
        self._lines = []
        # Hold a cache of line references to be
        # used against a callback.
        self.line_refs = []
        super(PlogBlockLineMixin, self).__init__(*args, **kwargs)

    def lines():
        doc = "The lines property."
        def fget(self):
            return [self.header] + self._lines + [self.footer]
        def fset(self, value):
            self._lines = value
        def fdel(self):
            del self._lines
        return locals()
    lines = property(**lines())

    def as_tuples(self):
        return [(x.ref, x,) for x in self.data]

    def as_dict(self, _dict=None, exclude=None, include=None):
        '''Retuns an object defining matched lines'''
        if exclude is None:
            exclude = ['footer']

        _d = _dict or {}
        for x in self.data:
            if x.ref not in exclude:
                _d.update(**{x.ref: x.clean()})
        return _d

    def header():
        doc = "The headerline for the PlogBlock"
        def fget(self):
            return self.get_header_line()
        def fset(self, value):
            self.set_header_line(value)
        def fdel(self):
            self.set_header_line(None)
        return locals()
    header = property(**header())

    def footer():
        doc = "The footerline for the PlogBlock"
        def fget(self):
            return self.get_footer_line()
        def fset(self, value):
            self.set_footer_line(value)
        def fdel(self):
            self.set_footer_line(None)
        return locals()
    footer = property(**footer())

    def set_header_line(self, plog_line):
        ''' The header line of the block
        to validate a start object.'''

        line = plog_line
        if type(plog_line) == str:
            ref = plog_line.ref if hasattr(plog_line, 'ref') else 'header'
            line = PlogLine(plog_line, ref=ref)
        self._header_line = line

    def get_header_line(self):
        return self._header_line

    def set_footer_line(self, plog_line):
        ''' The footer line of the block
        to validate a start object.'''
        line = plog_line
        if type(plog_line) == str:
            line = PlogLine(plog_line, ref='footer')
        self._footer_line = line

    def get_footer_line(self):
        return self._footer_line

    def add_lines(self, **kwargs):
        for ref in kwargs:
            line = kwargs[ref]
            if line.ref is None:
                line.ref = ref
            else:
                line._kwarg = ref
            self.add_line(line)
            self.line_refs.append({line.ref, line})

    def add_line(self, plog_line):
        ''' Apply a PlogLine to the PlogBlock. If the line is a string,
        it'll be converted to a PlogLine '''
        line = plog_line
        if type(plog_line) == str:
            line = PlogLine(plog_line)
        self._lines.append(line)

    def valid_line(self, plog_line):
        ''' Returns object or None to define if the passed plog_line
        is a valid line within the applied validator lines.
        If the plog_line passed matches the format of a PlogLine within
        self.lines, the matching validator line will be returned else None will
        return. '''
        for pline in self.lines:
            matched, sre_match = pline.match(plog_line)
            if matched:
                v = Validator(**{'sre': sre_match, 'line': pline})
                return v
        return None

    def valid(self):
        for line in self.data:
            if line.valid() is False: return False
        return True


class PlogBlockDataMixin(PlogBlockLineMixin):

    def __init__(self, *args, **kwargs):
        self.data = []
        super(PlogBlockDataMixin, self).__init__(*args, **kwargs)


    def add_data(self, data, validate=True):
        ''' Add data to the block (a PlogLine).
        If validation is True (default) and validation lines have been applied,
        the value will be validated before data append. If the value
        does not match a PlogLine format, it will not be added to the data list '''
        # If the block has lines. Validate against the
        # lines to apply value and context.
        # import pdb; pdb.set_trace()

        if len(self.lines) > 0:
            # Receive a validator (Only if data validates
            #  against a line)
            data.validator = self.valid_line(data)

            if data.validator:
                # all open lines are closed, as multiline is terminated by
                # the success of another validated line
                self.open_lines = {}
                # The line validated - are string from the file
                #  has matched the regex pattern of the valid line
                line = data.validator.line
                # Provide the reference given to the line
                data.ref = line.ref
                # Add the line to multiline open_lines so future data
                # passed from the file is pushed into an open line
                if line._multiline and line not in self.open_lines:
                    self.open_lines.update({line: data})

                self.data.append(data)
                return True
            else:
                for oline in self.open_lines:
                    olined = self.open_lines[oline]
                    olined.value += '\n' + data.value
                    # import pdb; pdb.set_trace()
                    return True
                else:
                    return False
        else:
            self.data.append(data)
            return True


class PlogBlockFileMixin(PlogBlockDataMixin):
    '''
    A PlogFileMixin is designed to wrap a file object to
    represent correctly for enumeration. You can pass a string or
    a file object.
    Strings are converted to cStringIO.StringIO before use.
    Pass this to the class for easy get_file, set_file methods
    '''
    def __init__(self, *args, **kwargs):
        ''' initial file can be given '''
        self._file = None
        self._data = None

        if len(args) > 0:
            ''' could be file or string'''
            self.set_data(args[0])

        super(PlogBlockFileMixin, self).__init__(*args, **kwargs)

    def set_file(self, log_file):
        ''' Add a file to the class to parse
        This will return a StringIO if a string
        was passed as data.'''
        self.set_data(log_file)

    def set_data(self, data):
        ''' wrapper for applying the file content
        to the class'''
        if type(data) == str:
            output = cStringIO.StringIO(data)
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


class Validator(object):
    ''' An object to represent a clean data object '''
    def __getitem__(self, v):
        return self.__dict__[v]

    def __init__(self, **entries):
        self.__dict__.update(entries)


class PatternBase(object):
    ''' Base mixin object of all Plog Mixins to inherit'''
    def __init__(self, *args, **kwargs):
        super(PatternBase, self).__init__()


def re_escape(fn):
    def arg_escaped(this, *args):
        t = [isinstance(a, VerEx) and a.s or re.escape(str(a)) for a in args]
        return fn(this, *t)
    return arg_escaped


class VerEx(PatternBase):
    '''
    --- VerbalExpressions class ---
    the following methods behave different from the original js lib!

    - end_of_line
    - start_of_line
    - or
    when you say you want `$`, `^` and `|`, we just insert it right there.
    No other tricks.

    And any string you inserted will be automatically grouped
    excepte `tab` and `add`.
    '''
    def __init__(self, *args, **kwargs):
        self._multiline = False
        self.s = ''
        self.modifiers = {'I': 0, 'M': 0}

        super(VerEx, self).__init__(*args, **kwargs)


    def add(self, value):
        self.s += value
        return self

    def regex(self, value=None):
        ''' get a regular expression object. '''
        s = self.s if value is None else value
        return re.compile(s, self.modifiers['I'] | self.modifiers['M'])

    def source(self):
        ''' return the raw string'''
        return self.s
    raw = value = source

    # ---------------------------------------------

    def anything(self):
        '''
        Accept any value at this point

            >>> VerEx().anything()

        '''
        return self.add('(.*)')

    @re_escape
    def anything_but(self, value):
        '''
        Accept any value, except the value provided.

            >>> VerEx().anything_but('A-Z0-9')
        '''
        return self.add('([^' + value + ']*)')

    def end_of_line(self, value=None):
        '''
        this should be appended last of all your called methods if
        searching for a terminated value.
        Assert the end of a string at this given point

            >>> VerEx('foo').maybe('bar').end_of_line()
        '''
        if value:
            self.then(value)
        return self.add('$')

    def multiline(self, v=True):
        '''
        Apply a multiline flag or pass false to remove
        if multiline is passed, data lines will be appended to
        the value of the PlogLine until interuppted by a
        another PlogLine validation or the validation is met
        '''
        self._multiline = True
        return self

    @re_escape
    def maybe(self, value):
        '''
        The value passed is potentially a match
            >>> VerEx('foo').maybe('bar')
        '''
        return self.add("(" + value + ")?")

    def start_of_line(self):
        '''
        this is used internally when required.
        '''
        return self.add('^')

    @re_escape
    def find(self, value):
        return self.add('(' + value + ')')
    then = find

    # special characters and groups

    @re_escape
    def any(self, value):
        return self.add("([" + value + "])")
    any_of = any

    def line_break(self):
        return self.add("(\\n|(\\r\\n))")
    br = line_break

    @re_escape
    def range(self, *args):
        from_tos = [args[i:i+2] for i in range(0, len(args), 2)]
        return self.add("([" + ''.join(['-'.join(i) for i in from_tos]) + "])")

    def tab(self):
        return self.add('\\t')

    def word(self):
        return self.add("(\\w+)")

    def OR(self, value=None):
        ''' `or` is a python keyword so we use `OR` instead. '''
        self.add("|")
        return self.find(value) if value else self

    def replace(self, string, repl):
        return self.sub(repl, string)

    # --------------- modifiers ------------------------

    # no global option. It depends on which method
    # you called on the regex object.

    def with_any_case(self, value=False):
        self.modifiers['I'] = re.I if value else 0
        return self

    def search_one_line(self, value=False):
        self.modifiers['M'] = re.M if value else 0
        return self
        # work in a similar fashion to Django
# with an attribute loader for filtering a string,
# passed into a regexing lib
# Eg:
#   P(header__istartswith='Device')

class PlogPattern(VerEx):
    '''
    Define a pattern to match within a plog line
    '''
    def __init__(self, *args, **kwargs):
        '''
        defined to be a set of attributes to
        filter the object definition
        '''
        self._ref = None

        if len(args) > 0:
            self.__value = args[0]

        self._cleaned_data = None
        self._compiled = None
        self.strip_clean = kwargs.get('strip', True)

        super(PlogPattern, self).__init__(*args, **kwargs)

        self.set_ref( kwargs.get('ref', None) )

    @property
    def cleaned_data(self):
        cl = self._cleaned_data
        if cl is None:
            cl = self.clean()
        return cl

    @cleaned_data.setter
    def cleaned_data(self, value):
        self._clean_data = value

    @property
    def compiled(self):
        if not self._compiled:
           self._compiled = self.compile()
        return self._compiled

    @compiled.setter
    def compiled(self, value):
        self._compiled = value

    def compile(self):
        ''' ready the matching re regex item for later use. this method considers
        the current regex start and fixes it accordingly. '''
        if self.value == '':
            self.compiled = None
        else:
            self.compiled = self.regex()
        import pdb; pdb.set_trace()  # breakpoint ddd496e8 //

        return self.compiled

    def ref():
        doc = '''The ref property. A string to define the
        objects value. A friendly name style'''

        def fget(self):
            return self.get_ref()
        def fset(self, value):
            self.set_ref(value)
        return locals()

    ref = property(**ref())

    def set_ref(self, value):
        self._ref = value

    def get_ref(self):
        return self._ref

    def clean(self):
        ''' return a clean verson of the string with the regex
        value stripped
        '''
        if self.strip_clean:
            val = self.get_value()
            _validator = self.validator.line.s

            val = re.sub(_validator, '', val)
            val = val.strip()
            self._cleaned_data = val
        return self._cleaned_data


class PlogBlock(PlogPattern, PlogBlockFileMixin):
    ''' A block of definable content, containing
    a list of Plog lines.

    When a PlogBlock is used when commanded for use
    during the parsing of a file - all lines
    after are passed into the block as lines
    associated with it's context. This will
    occur until a PlockBlock terminator line
    is parsed of PlogBlock().drop()
    is called whist context is open.'''

    def __init__(self, *args, **kwargs):
        '''  Pass the PlogLine used to
        validate a header of a given block.

        The footer_line is optional but would
        automatically terminate upon a new block. '''
        self.is_open = False

        self.pre_compile = kwargs.get('pre_compile', True)
        self.missed = []

        super(PlogBlock, self).__init__(*args, **kwargs)
        hl = args[0] if len(args) > 0 else None
        fl = args[1] if len(args) > 1 else None

        self.set_header_line(hl)
        self.set_footer_line(fl)



    def __repr__(self):
        ref = self.get_ref()
        s = self.header.format if ref is None else ref
        c = len(self.data)
        return '<%s: \'%s\'~%s>' % (self.__class__.__name__, s, c)

    def __str__(self):
        ref = self.get_ref()

        s = self.header if ref is None else ref
        c = len(self.data)
        return "<%s: %s~%s>" % (self.__class__.__name__, s, c)

    def add_missed(self, pline):
        self.missed.append(pline)

    def compile(self):
        '''Compile the header, footer and line PlogLine's
         ready to match testing'''

        if self.pre_compile == True:
            if self.header:
                self.header_compiled = self.header.compile()
            else:
                self.header_compiled = None

        if self.pre_compile == True:
            if self.footer:
                self.footer_compiled = self.footer.compile()
            else:
                self.footer_compiled = None

        for pline in self.lines:
            pline.compile()

        return (self.header_compiled, self.footer_compiled)

    def open(self):
        ''' Open the block during file enumeration to
        begin recieve lines'''
        self.is_open = True

    def close(self):
        self.is_open = False


# Device ID: AH1CMSW07
# Entry address(es):
#   IP address: 10.240.14.3
# Power request id: 23025, Power management id: 3

class DjangoPlogBlock(PlogBlock):
    '''
    Wraps a PlogBlock into a django mode using ref's from
    field values.
    '''

    def __init__(self, *args, **kwargs):
        super(DjangoPlogBlock, self).__init__(*args, **kwargs)
        self.model = kwargs.get('model', None)


    def _save(self):
        ''' Save the model returning boolean on success '''
        if self.model:
            val = self.as_dict()
            return self.model(**val).save()
        return False

class PlogLine(PlogPattern):
    # Define a line to match based upon it's value
    '''Define a single line to match'''

    # method of pattern matching for the regex checking
    method = 'match' # 'search'

    def __init__(self, value=None, block=None, *args, **kwargs):
        ''' Pass block to define the parent block object of this
        line. This may be None '''
        super(PlogLine, self).__init__(*args, **kwargs)

        self._ref = kwargs.get('ref', None)
        # the value found on the last match() method call
        self.matched = None
        self.validator = None

        self.value = value
        if self.value:
            self.startswith(self.value)

        self.block = block
        self.line_no = kwargs.get('line_no', -1)

    def validator_regex(self, value=None):
        '''
        Return the regex string used to validate the PlogLine or string value.
        If a validator exists, this is used as the regex, else a string
        is created from the own value.
        '''
        val = self if value is None else value
        if type(val) == PlogLine:
            val = val.value

        if self.validator:
            s = self.validator.line.s
        else:
            s = self.s
        return s


    def valid(self, value=None):
        ''' Return boolean for validity of the field'''
        v = self.value if value is None else value
        reg = self.validator_regex()
        regex = self.regex(reg)
        matcher = getattr(regex, self.__class__.method)
        matched = matcher(v)

        return True if matched else False

    def startswith(self, value):
        self.start_of_line()
        return self.then(value)

    def match(self, line):
        '''
        recieve a plogline
        Return tuple of True/False if the value matches the value
        and the matched object if one exists.
        '''
        matched = None
        matcher = getattr(self.compiled, self.__class__.method)
        matched = matcher(line.value)

        if matched:
            groups = matched.group()
            self.matched = matched.string
            return (True, matched)
        else:
            v = line == self.get_value()
            return (v, None)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


    def __str__(self):
        return 'PlogLine #%s: \"%s\"' % (self.line_no, self.value,)

    def __repr__(self):
        return '<%s>' % self.__str__()

    def __eq__(self, other):
        return self.value == other
