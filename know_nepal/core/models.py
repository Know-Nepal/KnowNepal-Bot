from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    guild_id = fields.BigIntField()
    github_username = fields.CharField(
        max_length=200, description="Describes github username of the User"
    )

    class Meta:
        table = "users"
        table_description = "Stores info about users."
