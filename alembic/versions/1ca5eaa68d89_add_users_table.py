"""add users table

Revision ID: 1ca5eaa68d89
Revises: 3021a78410ae
Create Date: 2022-07-15 18:23:51.302491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ca5eaa68d89'
down_revision = '3021a78410ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('create_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')  # not to have dublicae emial 
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
