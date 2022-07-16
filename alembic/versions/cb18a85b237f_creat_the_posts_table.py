"""creat the posts table

Revision ID: cb18a85b237f
Revises: 
Create Date: 2022-07-15 17:32:35.687499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb18a85b237f'
down_revision = None
branch_labels = None
depends_on = None

# here we add the changes we make to the table
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))
    pass

# in this function we add commands to bring back our old table, the changes that we make with upgrade() funtion will be set back
def downgrade() -> None:
    op.drop_table('posts')
    pass
