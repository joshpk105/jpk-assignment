"""empty message

Revision ID: be95d651ad8c
Revises: d318e08d8169
Create Date: 2022-02-08 14:07:34.206327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be95d651ad8c'
down_revision = 'd318e08d8169'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'authorship', type_='foreignkey')
    op.drop_constraint(None, 'authorship', type_='foreignkey')
    op.create_foreign_key(None, 'authorship', 'author', ['author_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'authorship', 'book', ['book_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'ownership', type_='foreignkey')
    op.drop_constraint(None, 'ownership', type_='foreignkey')
    op.create_foreign_key(None, 'ownership', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'ownership', 'book', ['book_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ownership', type_='foreignkey')
    op.drop_constraint(None, 'ownership', type_='foreignkey')
    op.create_foreign_key(None, 'ownership', 'book', ['book_id'], ['id'])
    op.create_foreign_key(None, 'ownership', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'authorship', type_='foreignkey')
    op.drop_constraint(None, 'authorship', type_='foreignkey')
    op.create_foreign_key(None, 'authorship', 'book', ['book_id'], ['id'])
    op.create_foreign_key(None, 'authorship', 'author', ['author_id'], ['id'])
    # ### end Alembic commands ###
