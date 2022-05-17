"""empty message

Revision ID: b5e79e1fec1d
Revises: 
Create Date: 2022-05-11 10:01:48.030373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5e79e1fec1d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TrivaQuestions',
    sa.Column('Question_ID', sa.Integer(), nullable=False),
    sa.Column('Questions', sa.Text(), nullable=False),
    sa.Column('Awsers', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('Question_ID')
    )
    op.create_table('User',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    op.create_index(op.f('ix_User_username'), 'User', ['username'], unique=True)
    op.create_table('DailyQusetion',
    sa.Column('Question_served', sa.Integer(), nullable=False),
    sa.Column('Date', sa.Date(), nullable=True),
    sa.Column('User_fk', sa.Integer(), nullable=True),
    sa.Column('Q_if_fk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Q_if_fk'], ['TrivaQuestions.Question_ID'], ),
    sa.ForeignKeyConstraint(['User_fk'], ['User.Id'], ),
    sa.PrimaryKeyConstraint('Question_served')
    )
    op.create_table('Score',
    sa.Column('Score_id', sa.Integer(), nullable=False),
    sa.Column('Id_fk', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('score_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['Id_fk'], ['User.Id'], ),
    sa.PrimaryKeyConstraint('Score_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Score')
    op.drop_table('DailyQusetion')
    op.drop_index(op.f('ix_User_username'), table_name='User')
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_table('User')
    op.drop_table('TrivaQuestions')
    # ### end Alembic commands ###