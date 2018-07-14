from collections import OrderedDict


class SentenceList(object):
    '''Incoming strings for temporal streams can be defined as a sentence.
    Opening and closing a sentence pushes the unique sentence graph
    to the next stage.
    '''
    def __init__(self):
        self.lists = {}

    def open(self):
        key = "list-{}".format(len(self.lists))
        self.lists[key] = {'given_words': () }
        return key

    def append_word(self, list_key, value):

        pos_key = len(self.lists[list_key]['given_words'])
        print 'adding', value, 'to sentence', list_key
        # linear stack
        # self.lists[list_key][value]['given_words'] += (value, )
        return pos_key

temporal_list = SentenceList()


def open_temporal():
    """Expecting a stream for temporal capture of a sentence or linear context.
    Ready the graphing for incoming data and return an identification key to
    be given during stream.
    """
    _id = temporal_list.open()
    print 'open temporal {}'.format(_id)
    return _id


def add_word(temporal_key, word):
    '''push the word into the current sentence'''

    word_id = temporal_list.append_word(temporal_key, word)
    # The word is in the sentence for other awareness; now
    # we work with the word, and write-back to the given reference.

    # Literal translate:
    #   Convert the given word to a hard-coded coversion to another word.
    #   For example "i" to "I" and inflections "Haven't" "Have Not"
    #
    #   In some cases (such as inflections) the translation can be derived from
    #   training and data learning. By applying a small graph for "n't"
    #   and pushing that into the secondary graphing, it can be soft-coded.
    #

