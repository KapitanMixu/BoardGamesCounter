from tortoise import fields
from tortoise.models import Model


class Player(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    scores: fields.ReverseRelation["Score"]

    class Meta:
        table = "players"
