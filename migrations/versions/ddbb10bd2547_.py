"""empty message

Revision ID: ddbb10bd2547
Revises: d2e206eff2bb
Create Date: 2024-05-22 17:06:58.723363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddbb10bd2547'
down_revision = 'd2e206eff2bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dados', schema=None) as batch_op:
        batch_op.add_column(sa.Column('desc', sa.String(), nullable=False))
        batch_op.drop_column('descrição')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dados', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descrição', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('desc')

    # ### end Alembic commands ###
