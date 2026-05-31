from tortoise import fields
from tortoise.models import Model


class GameSession(Model):
    id = fields.IntField(primary_key=True)
    game = fields.ForeignKeyField("models.Game", related_name="sessions")
    played_at = fields.DatetimeField(auto_now_add=True)
    notes = fields.TextField(null=True)

    scores: fields.ReverseRelation["Score"]

    class Meta:
        table = "game_sessions"


class Score(Model):
    id = fields.IntField(primary_key=True)
    session = fields.ForeignKeyField("models.GameSession", related_name="scores")
    player = fields.ForeignKeyField("models.Player", related_name="scores")
    points = fields.IntField(null=True)
    winner = fields.BooleanField(default=False)

    class Meta:
        table = "scores"
