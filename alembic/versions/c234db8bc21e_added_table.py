"""Added table

Revision ID: c234db8bc21e
Revises: 
Create Date: 2022-12-28 15:24:26.556277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c234db8bc21e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Post',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('total_like', sa.Integer(), nullable=True),
    sa.Column('post_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Like',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('Post_id', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['Post_id'], ['Post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Like')
    op.drop_table('Post')
    op.drop_table('User')
    # ### end Alembic commands ###
