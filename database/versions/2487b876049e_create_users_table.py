"""create users table

Revision ID: 2487b876049e
Revises: 3816be1dfec7
Create Date: 2020-12-03 11:21:25.169988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2487b876049e'
down_revision = '3816be1dfec7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('is_bot', sa.Boolean),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('username', sa.String),
        sa.Column('restricted', sa.Boolean),
        sa.Column('restriction_reason', sa.String),
        sa.Column('lang_code', sa.String),

        sa.Column('gbanned', sa.Boolean),
        sa.Column('gban_reason', sa.String),
        sa.Column('superuser', sa.Boolean),

        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('users')
