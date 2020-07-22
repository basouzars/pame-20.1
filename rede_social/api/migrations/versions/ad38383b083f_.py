"""empty message

Revision ID: ad38383b083f
Revises: 
Create Date: 2020-07-21 22:11:21.945822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad38383b083f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('activated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=280), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=280), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post likes',
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('posts_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['posts_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], )
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment likes',
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('comments_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comments_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment likes')
    op.drop_table('products')
    op.drop_table('post likes')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###