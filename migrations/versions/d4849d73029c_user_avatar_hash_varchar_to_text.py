"""user avatar_hash varchar to text

Revision ID: d4849d73029c
Revises: 5f5684cabf81
Create Date: 2022-06-20 15:56:01.810674

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd4849d73029c'
down_revision = '5f5684cabf81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'avatar_hash',
               existing_type=mysql.VARCHAR(length=32),
               type_=sa.Text(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'avatar_hash',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=32),
               existing_nullable=True)
    # ### end Alembic commands ###
