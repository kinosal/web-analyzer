"""empty message

Revision ID: 644fd5404cf7
Revises:
Create Date: 2021-06-10 15:56:27.330642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '644fd5404cf7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('artist_name', sa.String(), nullable=True),
    sa.Column('artist_source', sa.String(), nullable=True),
    sa.Column('external_id', sa.String(), nullable=True),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url')
    # ### end Alembic commands ###
