"""empty message

Revision ID: 5f1a2bd186d7
Revises: 72aaed25d335
Create Date: 2023-09-15 09:29:23.565522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f1a2bd186d7'
down_revision = '72aaed25d335'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('etapa',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('texto', sa.String(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('_id')
    )
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    op.drop_table('etapa')
    # ### end Alembic commands ###
