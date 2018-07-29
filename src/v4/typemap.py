COORDS = hash('COORDS')
HASSTUFFPTR = hash('HASSTUFFPTR')
WNGREP = hash('WNGREP')
MERONYM = hash('MERONYM')
FRAMES = hash('FRAMES')
CLASS = hash('CLASS')
ENTAILPTR = hash('ENTAILPTR')
ATTRIBUTE = hash('ATTRIBUTE')
ANTPTR = hash('ANTPTR')
PERTPTR = hash('PERTPTR')
CAUSETO = hash('CAUSETO')
HASPARTPTR = hash('HASPARTPTR')
HYPERPTR = hash('HYPERPTR')
HYPOPTR = hash('HYPOPTR')
DERIVATION = hash('DERIVATION')
RELATIVES = hash('RELATIVES')
HMERONYM = hash('HMERONYM')
HHOLONYM = hash('HHOLONYM')
SIMPTR = hash('SIMPTR')
HASMEMBERPTR = hash('HASMEMBERPTR')
FREQ = hash('FREQ')
ISSTUFFPTR = hash('ISSTUFFPTR')
ISPARTPTR = hash('ISPARTPTR')
HOLONYM = hash('HOLONYM')
SYNS = hash('SYNS')
ISMEMBERPTR = hash('ISMEMBERPTR')
CLASSIFICATION = hash('CLASSIFICATION')
OVERVIEW = hash('OVERVIEW')

ADJ = hash('ADJ')
NOUN = hash('NOUN')
VERB = hash('VERB')
ADV = hash('ADV')
ALL_POS = hash('ALL_POS')


type_map = {
    'CC' :'Coordinating conjunction',
    'CD' :'Cardinal number',
    'DT' :'Determiner',
    'EX' :'Existential there',
    'FW' :'Foreign word',
    'IN' :'Preposition or subordinating conjunction',
    'JJ' :'Adjective',
    'JJR' :'Adjective, comparative',
    'JJS' :'Adjective, superlative',
    'LS' :'List item marker',
    'MD' :'Modal',
    'NN' :'Noun, singular or mass',
    'NNS' :'Noun, plural',
    'NNP' :'Proper noun, singular',
    'NNPS' :'Proper noun, plural',
    'PDT' :'Predeterminer',
    'POS' :'Possessive ending',
    'PRP' :'Personal pronoun',
    'PRP$':'Possessive pronoun',
    'RB' :'Adverb',
    'RBR' :'Adverb, comparative',
    'RBS' :'Adverb, superlative',
    'RP' :'Particle',
    'SYM' :'Symbol',
    'TO' :'to',
    'UH' :'Interjection',
    'VB' :'Verb, base form',
    'VBD' :'Verb, past tense',
    'VBG' :'Verb, gerund or present participle',
    'VBN' :'Verb, past participle',
    'VBP' :'Verb, non-3rd person singular present',
    'VBZ' :'Verb, 3rd person singular present',
    'WDT' :'Wh-determiner',
    'WP' :'Wh-pronoun',
    'WP$':'Possessive wh-pronoun',
    'WRB' :'Wh-adverb',
    '.': 'Puncuation',
}


simplify = {
    'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',],
    'pronoun': ['PRP' , 'PRP$', 'WP' , 'WP$',],
    'adjective': ['JJ', 'JJR', 'JJS', ],
    'noun': ['NN', 'NNS', 'NNP', 'NNPS'],
    'adverb': ['RB', 'RBR', 'RBS'],
}



noun = {
    'antsn':"Antonyms",
    'hypen':"Hypernyms",
    'hypon':"Hyponyms & Hyponym Tree",
    'treen':"Hyponyms & Hyponym Tree",
    'synsn':"Synonyms (ordered by estimated frequency)",
    'attrn':"Attributes",
    'derin':"Derived Forms",
    'domnn':"Domain",
    'famln':"Familiarity & Polysemy Count",
    'coorn':"Coordinate Terms (sisters)",
    'grepn':"List of Compound Words",
     #'over':"Overview of Senses",
    "hypen": "Synonyms/Hypernyms (Ordered by Estimated Frequency)",
    "holon": "Holonyms",
    "sprtn": "Part Holonyms",
    "smemn": "Member Holonyms",
    "ssubn": "Substance Holonyms",
    "hholn": "Holonyms",
    "meron": "Meronyms",
    "subsn": "Substance Meronyms",
    "partn": "Part Meronyms",
    "membn": "Member Meronyms",
    "hmern": "Meronyms",
    "nomnn": "Derived Forms",
    "domtn": "Domain Terms",
}

verb = {
    'antsv':"Antonyms",
    'hypov':"Hyponyms & Hyponym Tree",
    'treev':"Hyponyms & Hyponym Tree",
    'deriv':"Derived Forms",
    'famlv':"Familiarity & Polysemy Count",
    'framv':"Verb Frames",
    'coorv':"Coordinate Terms (sisters)",
    'grepv':"List of Compound Words",
     #'over':"Overview of Senses"
    "synsv": "Synonyms/Hypernyms (Ordered by Estimated Frequency)",
    "simsv": "Synonyms (Grouped by Similarity of Meaning)",
    "hypev": "Synonyms/Hypernyms (Ordered by Estimated Frequency)",
    "tropv": "Troponyms (hyponyms)",
    "entav": "Entailment",
    "causv": "'Cause To'",
    "nomnv": "Derived Forms",
    "domnv": "Domain",
    "domtv": "Domain Terms",
    "framv": "Sample Sentences",

}

adj = {
    'antsa':"Antonyms",
    'synsa':"Synonyms (ordered by estimated frequency)",
    'domna':"Domain",
    'famla':"Familiarity & Polysemy Count",
    'grepa':"List of Compound Words",
     #'over':"Overview of Senses",
    'perta': 'Pertainyms',
    'attra': 'Attributes',
    'domta': 'Domain Terms',
}

adv = {
    "synsr": "Synonyms",
    "antsr": "Antonyms",
    "pertr": "Pertainyms",
    "domnr": "Domain",
    "domtr": "Domain Terms",
    "famlr": "Familiarity",
    "grepr": "Grep",
    "over": "Overview",
}


WORDNET_ATTRS = (
    { "-synsa", SIMPTR, ADJ, 0, "Similarity" },
    { "-antsa", ANTPTR, ADJ, 1, "Antonyms" },
    { "-perta", PERTPTR, ADJ, 0, "Pertainyms" },
    { "-attra", ATTRIBUTE, ADJ, 2, "Attributes" },
    { "-domna", CLASSIFICATION, ADJ, 3, "Domain" },
    { "-domta", CLASS, ADJ, 4, "Domain Terms" },
    { "-famla", FREQ, ADJ, 5, "Familiarity" },
    { "-grepa", WNGREP, ADJ, 6, "Grep" },

    { "-synsn", HYPERPTR, NOUN, 0, "Synonyms/Hypernyms (Ordered by Estimated Frequency)" },
    { "-antsn", ANTPTR, NOUN, 2, "Antonyms" },
    { "-coorn", COORDS, NOUN, 3, "Coordinate Terms (sisters)" },
    { "-hypen", -HYPERPTR, NOUN, 4, "Synonyms/Hypernyms (Ordered by Estimated Frequency)" },
    { "-hypon", HYPOPTR, NOUN, 5, "Hyponyms" },
    { "-treen", -HYPOPTR, NOUN, 6, "Hyponyms" },
    { "-holon", HOLONYM, NOUN, 7, "Holonyms" },
    { "-sprtn", ISPARTPTR, NOUN, 7, "Part Holonyms" },
    { "-smemn", ISMEMBERPTR, NOUN, 7, "Member Holonyms" },
    { "-ssubn", ISSTUFFPTR, NOUN, 7, "Substance Holonyms" },
    { "-hholn", -HHOLONYM, NOUN, 8, "Holonyms" },
    { "-meron", MERONYM, NOUN, 9, "Meronyms" },
    { "-subsn", HASSTUFFPTR, NOUN, 9, "Substance Meronyms" },
    { "-partn", HASPARTPTR, NOUN, 9, "Part Meronyms" },
    { "-membn", HASMEMBERPTR, NOUN, 9, "Member Meronyms" },
    { "-hmern", -HMERONYM, NOUN, 10, "Meronyms" },
    { "-nomnn", DERIVATION, NOUN, 11, "Derived Forms" },
    { "-derin", DERIVATION, NOUN, 11, "Derived Forms" },
    { "-domnn", CLASSIFICATION, NOUN, 13, "Domain" },
    { "-domtn", CLASS, NOUN, 14, "Domain Terms" },
    { "-attrn", ATTRIBUTE, NOUN, 12, "Attributes" },
    { "-famln", FREQ, NOUN, 15, "Familiarity" },
    { "-grepn", WNGREP, NOUN, 16, "Grep" },

    { "-synsv", HYPERPTR, VERB, 0, "Synonyms/Hypernyms (Ordered by Estimated Frequency)" },
    { "-simsv", RELATIVES, VERB, 1, "Synonyms (Grouped by Similarity of Meaning)" },
    { "-antsv", ANTPTR, VERB, 2, "Antonyms" },
    { "-coorv", COORDS, VERB, 3, "Coordinate Terms (sisters)" },
    { "-hypev", -HYPERPTR, VERB, 4, "Synonyms/Hypernyms (Ordered by Estimated Frequency)" },
    { "-hypov", HYPOPTR, VERB, 5, "Troponyms (hyponyms)" },
    { "-treev", -HYPOPTR, VERB, 5, "Troponyms (hyponyms)" },
    { "-tropv", -HYPOPTR, VERB, 5, "Troponyms (hyponyms)" },
    { "-entav", ENTAILPTR, VERB, 6, "Entailment" },
    { "-causv", CAUSETO, VERB, 7, "\'Cause To\'" },
    { "-nomnv", DERIVATION, VERB, 8, "Derived Forms" },
    { "-deriv", DERIVATION, VERB, 8, "Derived Forms" },
    { "-domnv", CLASSIFICATION, VERB, 10, "Domain" },
    { "-domtv", CLASS, VERB, 11, "Domain Terms" },
    { "-framv", FRAMES, VERB, 9, "Sample Sentences" },
    { "-famlv", FREQ, VERB, 12, "Familiarity" },
    { "-grepv", WNGREP, VERB, 13, "Grep" },

    { "-synsr", SYNS, ADV, 0, "Synonyms" },
    { "-antsr", ANTPTR, ADV, 1, "Antonyms" },
    { "-pertr", PERTPTR, ADV, 0, "Pertainyms" },
    { "-domnr", CLASSIFICATION, ADV, 2, "Domain" },
    { "-domtr", CLASS, ADV, 3, "Domain Terms" },
    { "-famlr", FREQ, ADV, 4, "Familiarity" },
    { "-grepr", WNGREP, ADV, 5, "Grep" },
    { "-over", OVERVIEW, ALL_POS, -1, "Overview" },
)

attrs = {
    'h':'Print help text before search results.',
    'g':'Display textual glosses associated with synsets.',
    'a':'Display lexicographer file information.',
    'o':'Display synset offset of each synset.',
    's':'Display each word\'s sense numbers in synsets',
    'l':'Display the WordNet copyright notice, version number, and license.',
    'n#':'Perform search on sense number # only.',
    'over':'Display overview of all senses of searchstr in all syntactic categories.',
}


REL_HEADINGS = {
    'en': {
        '/r/SimilarTo': ['Similar terms'],
        '/r/RelatedTo': ['Related terms'],
        '/r/Synonym': ['Synonyms'],
        '/r/Antonym': ['Antonyms'],
        '/r/FormOf': ['Word forms', 'Root words'],
        '/r/HasContext': ['Terms with this context', 'Context of this term'],
        '/r/DerivedFrom': ['Derived terms', 'Derived from'],
        '/r/IsA': ['Types of {0}', '{0} is a type of...'],
        '/r/EtymologicallyRelatedTo': ['Etymologically related'],
        '/r/AtLocation': ['Things located at {0}', 'Location of {0}'],
        '/r/Causes': ['Causes of {0}', 'Effects of {0}'],
        '/r/UsedFor': ['Things used for {0}', '{0} is used for...'],
        '/r/NotUsedFor': ['Things that are not used for {0}', '{0} is not used for...'],
        '/r/MotivatedByGoal': ['Things motivated by {0}', '{0} is motivated by...'],
        '/r/HasSubevent': ['Subevents of {0}', '{0} is a subevent of...'],
        '/r/DistinctFrom': ['Distinct terms'],
        '/r/CapableOf': ['Things capable of {0}', '{0} is capable of...'],
        '/r/NotCapableOf': ['Things incapable of {0}', '{0} is not capable of...'],
        '/r/Desires': ['Things that want {0}', '{0} wants...'],
        '/r/NotDesires': ["Things that don't want {0}", "{0} doesn't want..."],
        '/r/PartOf': ['Parts of {0}', '{0} is part of...'],
        '/r/HasPrerequisite': ['Things that require {0}', '{0} requires...'],
        '/r/CausesDesire': ['Things that make you want {0}', '{0} makes you want...'],
        '/r/HasProperty': ['Things with the property {0}', 'Properties of {0}'],
        '/r/MadeOf': ['Things made of {0}', '{0} is made of...'],
        '/r/HasFirstSubevent': ['Things whose first step is {0}', '{0} is the first step of...'],
        '/r/HasLastSubevent': ['Things whose last step is {0}', '{0} is the last step of...'],
        '/r/DefinedAs': ['Things defined as {0}', '{0} is defined as...'],
        '/r/ReceivesAction': ['Things that can be {0}', '{0} can be...'],
        '/r/HasA': ['Things with {0}', '{0} has...'],
        '/r/SymbolOf': ['Symbols of {0}', '{0} symbolizes...'],
        '/r/ObstructedBy': ['{0} obstructs...', '{0} is obstructed by...'],
        '/r/Entails': ['Things that entail {0}', '{0} entails...'],
        '/r/CreatedBy': ['Things created by {0}', '{0} is created by...'],
        '/r/MannerOf': ['Ways of {0}', '{0} is a way of...'],
        '/r/LocationOfAction': ['Places where {0} happens', '{0} happens at...'],
        '/r/Uses': ['Things that use {0}', '{0} uses...'],
        '/r/ControlledBy': ['{0} controls...', '{0} is controlled by...'],
        '/r/LocatedNear': ['Things located near {0}', '{0} is near...'],
        '/r/ExternalURL': ['Links to ConceptNet', 'Links to other sites'],
    }
}
