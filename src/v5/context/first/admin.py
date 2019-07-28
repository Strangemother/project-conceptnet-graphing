from django.contrib import admin

from . import models

@admin.register(
    models.Tag,
    models.DefinitionType,
    models.DefinitionValueType,
    models.Definition,
    models.TokenWord,
    models.PositionTokenWord,
    models.TemporalInput,
    models.TemporalSession,
    )
class StandardAdmin(admin.ModelAdmin):
    pass
