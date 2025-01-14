"""remove name column from freebies table

Revision ID: 4ecf6d961128
Revises: f0ede71968ab
Create Date: 2023-06-11 19:13:55.598121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ecf6d961128'
down_revision = 'f0ede71968ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('freebies', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('freebies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###
