from tortoise import fields
from tortoise.models import Model


class Game(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    min_players = fields.IntField(default=2)
    max_players = fields.IntField(default=4)
    duration_minutes = fields.IntField(null=True)
    duration_type = fields.CharField(max_length=20, null=True)  # "total" | "per_player"
    created_at = fields.DatetimeField(auto_now_add=True)

    sessions: fields.ReverseRelation["GameSession"]

    class Meta:
        table = "games"
