from tortoise import fields
from tortoise.models import Model


class Expansion(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    game = fields.ForeignKeyField("models.Game", related_name="expansions")

    class Meta:
        table = "expansions"
