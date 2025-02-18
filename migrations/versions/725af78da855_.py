"""empty message

Revision ID: 725af78da855
Revises: ef14b173511d
Create Date: 2024-05-17 14:24:36.122635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '725af78da855'
down_revision = 'ef14b173511d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filtro',
    sa.Column('_id', sa.String(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('lista_filtros', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('_id')
    )
    op.drop_table('procedimento')
    op.drop_table('etapa')
    op.drop_table('ticket')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('_id', sa.INTEGER(), nullable=False),
    sa.Column('problema', sa.VARCHAR(), nullable=False),
    sa.Column('ativo', sa.VARCHAR(), nullable=False),
    sa.Column('prioridade', sa.INTEGER(), nullable=False),
    sa.Column('estado', sa.VARCHAR(), nullable=False),
    sa.Column('data_hora_a', sa.DATETIME(), nullable=False),
    sa.Column('data_hora_f', sa.DATETIME(), nullable=False),
    sa.Column('periodo', sa.VARCHAR(), nullable=True),
    sa.Column('file', sa.VARCHAR(), nullable=True),
    sa.Column('autor', sa.VARCHAR(), nullable=False),
    sa.Column('att', sa.VARCHAR(), nullable=True),
    sa.Column('dep', sa.VARCHAR(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=False),
    sa.Column('re_att_just', sa.VARCHAR(), nullable=True),
    sa.Column('p_defined', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('etapa',
    sa.Column('_id', sa.INTEGER(), nullable=False),
    sa.Column('texto', sa.VARCHAR(), nullable=False),
    sa.Column('ticket_id', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('procedimento',
    sa.Column('_id', sa.INTEGER(), nullable=False),
    sa.Column('titulo', sa.VARCHAR(), nullable=False),
    sa.Column('procedimento', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('_id')
    )
    op.drop_table('filtro')
    # ### end Alembic commands ###
