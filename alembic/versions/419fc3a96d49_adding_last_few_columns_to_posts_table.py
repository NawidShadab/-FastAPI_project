"""adding last few columns to posts table

Revision ID: 419fc3a96d49
Revises: c401ea24c934
Create Date: 2022-07-15 22:35:04.113331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '419fc3a96d49'
down_revision = 'c401ea24c934'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    
    pass
