"""empty message

Revision ID: f86e5fa19481
Revises: 
Create Date: 2022-02-05 19:23:57.819569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f86e5fa19481'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Unicode(length=64), nullable=True),
    sa.Column('email', sa.Unicode(length=320), nullable=True),
    sa.Column('password_hash', sa.Unicode(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(length=120), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ownership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purchase_datetime', sa.DateTime(), nullable=True),
    sa.Column('note', sa.UnicodeText(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ownership')
    op.drop_table('book')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('author')
    # ### end Alembic commands ###
