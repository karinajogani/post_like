"""create table

Revision ID: 6947f3af3298
Revises: a281547e0ebc
Create Date: 2023-01-05 16:54:37.072835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6947f3af3298'
down_revision = 'a281547e0ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Like', 'is_delete')
    op.drop_column('Like', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Like', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('Like', sa.Column('is_delete', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###