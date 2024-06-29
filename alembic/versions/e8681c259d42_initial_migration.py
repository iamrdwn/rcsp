"""Initial migration

Revision ID: e8681c259d42
Revises: 
Create Date: 2024-06-14 23:51:23.900913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8681c259d42'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('children',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('school', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_children_id'), 'children', ['id'], unique=False)
    op.create_index(op.f('ix_children_name'), 'children', ['name'], unique=False)
    op.create_table('donors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donors_email'), 'donors', ['email'], unique=True)
    op.create_index(op.f('ix_donors_id'), 'donors', ['id'], unique=False)
    op.create_index(op.f('ix_donors_name'), 'donors', ['name'], unique=False)
    op.create_table('donations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('donor_id', sa.Integer(), nullable=True),
    sa.Column('child_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['children.id'], ),
    sa.ForeignKeyConstraint(['donor_id'], ['donors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donations_id'), 'donations', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_donations_id'), table_name='donations')
    op.drop_table('donations')
    op.drop_index(op.f('ix_donors_name'), table_name='donors')
    op.drop_index(op.f('ix_donors_id'), table_name='donors')
    op.drop_index(op.f('ix_donors_email'), table_name='donors')
    op.drop_table('donors')
    op.drop_index(op.f('ix_children_name'), table_name='children')
    op.drop_index(op.f('ix_children_id'), table_name='children')
    op.drop_table('children')
    # ### end Alembic commands ###
