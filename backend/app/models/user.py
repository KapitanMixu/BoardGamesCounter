from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=150, unique=True)
    password_hash = fields.CharField(max_length=255)
    role = fields.CharField(max_length=20, default="reader")  # "admin" | "reader"
    player: fields.ForeignKeyNullableRelation["Player"] = fields.ForeignKeyField(
        "models.Player", related_name="user", null=True, on_delete=fields.SET_NULL
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
