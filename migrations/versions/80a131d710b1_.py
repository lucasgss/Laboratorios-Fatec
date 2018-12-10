"""empty message

Revision ID: 80a131d710b1
Revises: 
Create Date: 2018-12-10 15:56:50.822000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80a131d710b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artefatoDono',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descricao')
    )
    op.create_table('artefatoTipo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descricao')
    )
    op.create_table('papel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descricao')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('senha_hash', sa.String(length=128), nullable=False),
    sa.Column('denominacao', sa.String(length=20), nullable=True),
    sa.Column('papel_id', sa.Integer(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['papel_id'], ['papel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuario_email'), 'usuario', ['email'], unique=True)
    op.create_index(op.f('ix_usuario_nome'), 'usuario', ['nome'], unique=False)
    op.create_table('laboratorio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=60), nullable=True),
    sa.Column('auditado', sa.Boolean(), nullable=True),
    sa.Column('professorTitular_id', sa.Integer(), nullable=True),
    sa.Column('professorSuplente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['professorSuplente_id'], ['usuario.id'], ),
    sa.ForeignKeyConstraint(['professorTitular_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descricao')
    )
    op.create_table('artefato',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(length=60), nullable=True),
    sa.Column('capacidade', sa.String(length=20), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('valorEstimado', sa.DECIMAL(precision=13, scale=2), nullable=True),
    sa.Column('numeroPatrimonio', sa.String(length=20), nullable=False),
    sa.Column('laboratorio_id', sa.Integer(), nullable=False),
    sa.Column('artefatoTipo_id', sa.Integer(), nullable=False),
    sa.Column('artefatoDono_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artefatoDono_id'], ['artefatoDono.id'], ),
    sa.ForeignKeyConstraint(['artefatoTipo_id'], ['artefatoTipo.id'], ),
    sa.ForeignKeyConstraint(['laboratorio_id'], ['laboratorio.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('descricao')
    )
    op.create_table('insumo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantidadeAtual', sa.Integer(), nullable=True),
    sa.Column('quantidadeMinima', sa.Integer(), nullable=True),
    sa.Column('descricao', sa.String(length=60), nullable=True),
    sa.Column('laboratorio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['laboratorio_id'], ['laboratorio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('insumo')
    op.drop_table('artefato')
    op.drop_table('laboratorio')
    op.drop_index(op.f('ix_usuario_nome'), table_name='usuario')
    op.drop_index(op.f('ix_usuario_email'), table_name='usuario')
    op.drop_table('usuario')
    op.drop_table('papel')
    op.drop_table('artefatoTipo')
    op.drop_table('artefatoDono')
    # ### end Alembic commands ###