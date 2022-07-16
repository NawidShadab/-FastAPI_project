"""adding contnent column to the posts table

Revision ID: 3021a78410ae
Revises: cb18a85b237f
Create Date: 2022-07-15 18:06:33.745960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3021a78410ae'
down_revision = 'cb18a85b237f'
branch_labels = None
depends_on = None

# adding new column content to posts table by upgrade 
def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


# by downgrade we remove the content column we created in upgrade() funtion (name of tabel name of clm)
def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
