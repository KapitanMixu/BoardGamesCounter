from tortoise import fields
from tortoise.models import Model


class WishlistItem(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    planszeo_url = fields.CharField(max_length=500, null=True)
    bgg_url = fields.CharField(max_length=500, null=True)
    notes = fields.TextField(null=True)
    # cached cheapest offer from Planszeo
    best_price = fields.FloatField(null=True)
    best_price_shop = fields.CharField(max_length=255, null=True)
    offer_count = fields.IntField(null=True)
    price_updated_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "wishlist_items"
