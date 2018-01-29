
def apply_to_context(thin_structure_words):
    '''given data from the token assess, build clean data for the context
    engine, populating with missing data as required.
    '''
    words = thin_structure_words

    print words.keys()
    print 'tree',  thin_structure_words['tree']

    if 'words' in words:

        for wordset in words['words']:
            word, wtype, ident, dict_ref = wordset
            print "looking at - ", word, wtype
    else:
        print 'no word information'
