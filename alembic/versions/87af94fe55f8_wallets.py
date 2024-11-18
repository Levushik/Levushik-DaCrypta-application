"""wallets

Revision ID: 87af94fe55f8
Revises: e5c8082d93bc
Create Date: 2024-07-21 14:30:55.766750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87af94fe55f8'
down_revision: Union[str, None] = 'e5c8082d93bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallets',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('owner_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('mnemonics', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('disposed', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wallets_owner_id'), 'wallets', ['owner_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wallets_owner_id'), table_name='wallets')
    op.drop_table('wallets')
    # ### end Alembic commands ###
