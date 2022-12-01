"""empty message

Revision ID: d099bf897298
Revises: 9e3edab3bf38
Create Date: 2022-11-28 20:29:26.421740

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd099bf897298'
down_revision = '9e3edab3bf38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    genres_enum = postgresql.ENUM('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genres_enum')
    genres_enum.create(op.get_bind())
    
    statesenum = postgresql.ENUM('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='statesenum')
    statesenum.create(op.get_bind())

    
    with op.batch_alter_table('Venue', schema=None) as batch_op:
       batch_op.drop_column('state')
       batch_op.drop_column('genres')
       batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
       batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
       batch_op.add_column(sa.Column('state', sa.Enum('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='statesenum'), nullable=True))
       batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
       batch_op.add_column(sa.Column('genres', sa.Enum('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genres_enum'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.Enum('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genresenum'),
               type_=postgresql.ENUM('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'HipHop', 'HeavyMetal', 'Instrumental', 'Jazz', 'MusicalTheatre', 'Pop', 'Punk', 'RB', 'Reggae', 'RocknRoll', 'Soul', 'Other', name='genres_enum'),
               nullable=True)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=sa.Enum('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='statesenum'),
               type_=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###