"""create chats table

Revision ID: 3816be1dfec7
Revises:
Create Date: 2020-12-02 17:06:01.078856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3816be1dfec7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chats',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('kind', sa.String),

        sa.Column('bot_enabled', sa.Boolean),
        sa.Column('is_admin', sa.Boolean),

        sa.Column('ban_command', sa.String),

        sa.Column('gbans_enabled', sa.Boolean),
        sa.Column('gban_command', sa.String),

        sa.Column('fbans_enabled', sa.Boolean),
        sa.Column('fban_command', sa.String),

        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('chats')
