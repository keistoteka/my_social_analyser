"""Add temp_password_expires_at field to User model

Revision ID: 29d440c6635b
Revises: 
Create Date: 2025-06-11 13:17:36.913725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d440c6635b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_temporary_password', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('temp_password_expires_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('temp_password_expires_at')
        batch_op.drop_column('is_temporary_password')

    # ### end Alembic commands ###
