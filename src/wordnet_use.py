from v4.bridge import get_siblings as get
from v4.wordnet import get_word, caller, NOUN, VERB, ADJ, ALL

app_path = "C:/Program Files (x86)/WordNet/2.1/bin/wn"
out_base = "C:\\Users\\jay\\Documents\\projects\\context-api\\context\\src\\data\\wordnet"

get = caller(ALL, app_path=app_path, output_dir=out_base)

# res = get('egg', to_file=None)
# res = get('egg', to_file=False)
# res = get('egg', to_file=True)
# res = get('egg', to_file='egg.txt')
d= get('day')
