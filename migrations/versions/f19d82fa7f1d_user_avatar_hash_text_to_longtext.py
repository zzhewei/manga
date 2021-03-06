"""user avatar_hash text to longtext

Revision ID: f19d82fa7f1d
Revises: d4849d73029c
Create Date: 2022-06-20 16:13:46.615375

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f19d82fa7f1d'
down_revision = 'd4849d73029c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'avatar_hash',
               existing_type=mysql.TEXT(),
               type_=mysql.LONGTEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'avatar_hash',
               existing_type=mysql.LONGTEXT(),
               type_=mysql.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###
