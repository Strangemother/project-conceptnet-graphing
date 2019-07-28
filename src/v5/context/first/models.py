from django.db import models
import nltk
from . import dictionary


import sys

from . import infl

def tokenize_input(input_model):
    value = input_model.value
    t = nltk.word_tokenize(value)
    # ['I', 'like', 'cake']
    tokens = nltk.pos_tag(t)
    # [('I', 'PRP'), ('like', 'VBP'), ('cake', 'VB')]
    pms = ()
    for index, (word, tag) in enumerate(tokens):
        tagm, created = Tag.objects.get_or_create(value=tag)
        if created:
            tagm.save()
        pw, created = PositionTokenWord.objects.get_or_create(
            position=index,
            value=word,
            tag=tagm,
            )
        if created:
            pw.save()
        pms += (pw, )
    print(f'Writing: {len(pms)} to "{input_model}"')
    input_model.tokens.add(*pms)
    #input_model.save()


def get_dictionary(input_model):

    words = input_model.tokens.all()

    for word in words:
        print('Fetching word', word)
        res = dictionary.get_word(word.value)
        word.raw_dictionary = res

        sibs = infl.get_siblings(word.value)
        tense, created = Tense.objects.get_or_create(
            plural=sibs['plural'],
            plural_noun=sibs['plural_noun'],
            plural_verb=sibs['plural_verb'],
            plural_adj=sibs['plural_adj'],
            singular_noun=sibs['singular_noun'],
            present_participle=sibs['present_participle'],
        )

        if created:
            tense.save()
        word.tense = tense

        for key in res:
            # meaning, synonym, antonym

            if key == 'value':
                continue

            if res[key] is None:
                print(f'Dictionary Key "{key}" is None for {word}')
                continue

            # meaning, synonym, antonym
            deft, created = DefinitionType.objects.get_or_create(value=key)
            if created is True: deft.save()

            # Noun, Adjective
            if isinstance(res[key], dict):
                for val_type in res[key]:
                    #   'done with delicacy and skill',
                    for dictionary_str in res[key][val_type]:
                        defvt, created = DefinitionValueType.objects.get_or_create(value=val_type)
                        if created is True: defvt.save()

                        df, created = Definition.objects.get_or_create(
                            associate=deft,
                            type=defvt,
                            value=dictionary_str)

                        if created is True: df.save()

                        print(f'Applying new definition {df}')
                        word.dictionary.add(df)
            elif isinstance(res[key], list):
                defvt, created = DefinitionValueType.objects.get_or_create(value='undefined')
                if created is True: defvt.save()

                for dictionary_str in res[key]:
                    df, created = Definition.objects.get_or_create(
                            associate=deft,
                            type=defvt,
                            value=dictionary_str)
                    if created is True: df.save()

        word.save()



class Tag(models.Model):
    value = models.CharField(help_text='Word', max_length=255)

    def __str__(self):
        return self.value


# {
# 'value': 'nice',
#     'meaning': {
#         'Noun': [
#                 'a city in southeastern France on the Mediterranean; the leading resort on the French Riviera'
#             ],
#         'Adjective': [
#                 'pleasant or pleasing or agreeable in nature or appearance',
#                 'socially or conventionally correct; refined or virtuous',
#                 'done with delicacy and skill',
#                 'excessively fastidious and easily disgusted',
#                 'exhibiting courtesy and politeness'
#             ]
#     },
# 'synonym': None,
# 'antonym': None}


class DefinitionType(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class DefinitionValueType(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class Definition(models.Model):
    associate = models.ForeignKey(DefinitionType, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(DefinitionValueType, on_delete=models.DO_NOTHING)
    value = models.TextField()

    def __str__(self):
        return f'{self.associate}, {self.type}, {self.value}'

class Tense(models.Model):
    plural = models.CharField(max_length=255, null=True, blank=True)#('we'),
    plural_noun = models.CharField(max_length=255, null=True, blank=True)#('we'),
    plural_verb = models.CharField(max_length=255, null=True, blank=True)#('I'),
    plural_adj = models.CharField(max_length=255, null=True, blank=True)#('I'),
    singular_noun = models.CharField(max_length=255, null=True, blank=True)#(False),
    present_participle = models.CharField(max_length=255, null=True, blank=True)#('Iing'),


class TokenWord(models.Model):
    value = models.CharField(help_text='Word', max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    raw_dictionary = models.TextField(blank=True, null=True)
    dictionary = models.ManyToManyField(Definition)
    tense = models.ForeignKey(Tense, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.value} - {self.tag}"


class PositionTokenWord(TokenWord):
    position = models.SmallIntegerField()
    #tokenword = models.ForeignKey(TokenWord, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"({self.position}) {self.value} - {self.tag}"


class TemporalInput(models.Model):
    """In the firt layer a temporal input defines content (a string) from
    the user to train up. Each _sentence_ is a layer0 type.
    """
    value = models.TextField(help_text='Input data as a start value.')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tokens = models.ManyToManyField(PositionTokenWord, blank=True)#, on_delete=models.DO_NOTHING    )

    def __str__(self):
        return self.value


class TemporalSession(models.Model):
    """Group many inputs to a session.
    """
    # The list of assigned inputs.
    inputs = models.ManyToManyField(TemporalInput)

    def __str__(self):
        return f"TemporalSession of {self.inputs.count()} inputs"
