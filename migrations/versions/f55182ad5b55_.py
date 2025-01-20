"""empty message

Revision ID: f55182ad5b55
Revises: f2d2e9ac397e
Create Date: 2024-05-21 09:25:36.756529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f55182ad5b55'
down_revision = 'f2d2e9ac397e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('filtro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lat', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('long', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('zoom', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('maptype', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('cor', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('filtro', schema=None) as batch_op:
        batch_op.drop_column('cor')
        batch_op.drop_column('maptype')
        batch_op.drop_column('zoom')
        batch_op.drop_column('long')
        batch_op.drop_column('lat')

    # ### end Alembic commands ###
