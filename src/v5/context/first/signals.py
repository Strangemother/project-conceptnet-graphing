from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from . import models

print('first::signals')
import django.dispatch
from django.dispatch import receiver


pre_save_input = django.dispatch.Signal(providing_args=["instance"])
post_save_input = django.dispatch.Signal(providing_args=["instance"])
tokenized_input = django.dispatch.Signal(providing_args=["instance"])


#@receiver(post_save, sender=models.TemporalInput)
@receiver(post_save_input)
#@receiver(pre_save, sender=models.TemporalInput)
def tokenize_input_instance(sender, instance, **kwargs):
    """
    Arguments sent with this signal:
        sender
            The model class.
        instance
            The actual instance being saved.
        created
            A boolean; True if a new record was created.
        raw
            A boolean; True if the model is saved exactly as presented
            (i.e. when loading a fixture). One should not query/modify other
            records in the database as the database might not be in a
            consistent state yet.
        using
            The database alias being used.
        update_fields
            The set of fields to update as passed to Model.save(), or None if
            update_fields wasn’t passed to save().
    """
    models.tokenize_input(instance)
    print('post save', instance)
    tokenized_input.send(sender=sender, instance=instance)

@receiver(tokenized_input)
def dictionary_input_instance(sender, instance, **kwargs):
    models.get_dictionary(instance)
