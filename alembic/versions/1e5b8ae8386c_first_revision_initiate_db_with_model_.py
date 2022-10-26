"""First revision: initiate db with model schema

Revision ID: 1e5b8ae8386c
Revises: 
Create Date: 2022-10-26 12:19:54.844182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e5b8ae8386c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio_data',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('ticks', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('selected_tick', sa.Integer(), nullable=False),
    sa.Column('step_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('user_data',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_data')
    op.drop_table('audio_data')
    # ### end Alembic commands ###