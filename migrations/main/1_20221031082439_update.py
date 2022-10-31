from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "github_username" VARCHAR(200) NOT NULL
);
COMMENT ON COLUMN "users"."github_username" IS 'Describes github username of the User';
COMMENT ON TABLE "users" IS 'Stores info about users.';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "users";"""
