'''Use berkley key assoc exe app as a data input by reading STDOUT of a windows
cli tool.'''

import os
import subprocess

from typemap import noun, verb, adj, attrs

ALL = noun.keys() + verb.keys() + adj.keys()


def caller(params=None):
    params = params or []
    base_path = "C:\\Program Files (x86)\\WordNet\\2.1\\bin\\wn"
    out_base = "C:\\Users\\jay\\Documents\\projects\\context-api\\context\\src\\data\\wordnet"

    def perform_call(word, additional_params=None):
        ams = additional_params or []
        switches = ' -'.join(list(set(params + ams)))
        ps = '-'.join(params)
        filepath = "{}-{}.txt".format(word, ps)
        out = os.path.join(out_base, filepath)
        st = '"{app}" {word} -{switches} > "{out}"'
        call_str = st.format(app=base_path,
                             word=word,
                             switches=switches,
                             out=out)
        print(call_str)
        res = subprocess.run(call_str.split(' '), capture_output=True)
        import pdb; pdb.set_trace()  # breakpoint 6cb0fec2 //

    return perform_call
