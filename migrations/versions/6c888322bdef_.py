"""empty message

Revision ID: 6c888322bdef
Revises: 193206b2b627
Create Date: 2021-02-22 17:01:20.736139

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6c888322bdef'
down_revision = '193206b2b627'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pedidos', 'valor',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pedidos', 'valor',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
