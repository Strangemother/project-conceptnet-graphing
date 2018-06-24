

def print_edges(res):
    _format = "{:<15} {:5} {:20} {:20} {:20} {}"

    # Languages not to list based upon start edge:
    exclude_langs = ['ja', 'fr', 'ast', 'bg', 'el', 'dsb', 'de', 'chr', 'co',
        'cy', 'fil', 'br', 'hu', 'hi', 'cic', 'es', 'pt', 'th', 'ar', 'fa',
        'zh', 'arc', 'arn', 'ar', 'ba', 'bn', 'cs', 'da', 'sq', 'gl', 'ca', 'ms'
        'af', 'fi', 'frp', 'gsw','gd', 'hy', 'fj', 'ga', 'he', 'ht', 'af',
        'haw', 'eo', 'et', 'ha', 'eu', 'ms', 'ko', 'la', 'lij', 'fo','ko',
        'lb', 'fur', 'io', 'is', 'it',
        ]

    include_langs = ['en']

    print _format.format('Type', 'lang', 'Start', 'End', 'End-lang', 'weight')
    meta = res.get('meta', None)
    if meta is None:
        return res

    for edge in meta:
        lang = edge['start'].get('language', '')
        if  lang in exclude_langs:
            if lang not in include_langs:
                continue

        if len(include_langs) > 0 and lang not in include_langs:
            continue

        print _format.format(
            edge['rel']['label'],
            # unicode.encode(edge['id'], errors='replace'),
            edge['start'].get('language', ''),
            unicode.encode(edge['start']['label'], errors='replace'),
            unicode.encode(edge['end']['label'], errors='replace'),
            edge['end'].get('language', ''),
            edge['weight']
            )
    return res

