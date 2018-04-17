"""group

Revision ID: bf1e4b795a19
Revises: c6c1146500b8
Create Date: 2018-04-13 19:12:23.545451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf1e4b795a19'
down_revision = 'c6c1146500b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Groups',
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('groupname', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], )
    )
    op.create_index(op.f('ix_Groups_groupname'), 'Groups', ['groupname'], unique=True)
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('groupname', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_groupname'), 'group', ['groupname'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_group_groupname'), table_name='group')
    op.drop_table('group')
    op.drop_index(op.f('ix_Groups_groupname'), table_name='Groups')
    op.drop_table('Groups')
    # ### end Alembic commands ###