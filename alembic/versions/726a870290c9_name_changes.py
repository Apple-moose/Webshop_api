"""Name changes

Revision ID: 726a870290c9
Revises: 416bd82378af
Create Date: 2024-07-26 12:53:15.301790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '726a870290c9'
down_revision: Union[str, None] = '416bd82378af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('createdAt', sa.DateTime(), nullable=True))
    op.add_column('categories', sa.Column('updatedAt', sa.DateTime(), nullable=True))
    op.drop_column('categories', 'created_At')
    op.drop_column('categories', 'updated_At')
    op.add_column('products', sa.Column('imageUrl', sa.String(), nullable=True))
    op.add_column('products', sa.Column('categoryId', sa.Integer(), nullable=False))
    op.add_column('products', sa.Column('createdAt', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('updatedAt', sa.DateTime(), nullable=True))
    op.drop_constraint('products_category_id_fkey', 'products', type_='foreignkey')
    op.create_foreign_key(None, 'products', 'categories', ['categoryId'], ['id'])
    op.drop_column('products', 'image_URL')
    op.drop_column('products', 'created_At')
    op.drop_column('products', 'category_id')
    op.drop_column('products', 'updated_At')
    op.add_column('reviews', sa.Column('userId', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('productId', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('createdAt', sa.DateTime(), nullable=True))
    op.add_column('reviews', sa.Column('updatedAt', sa.DateTime(), nullable=True))
    op.drop_index('ix_reviews_product_id', table_name='reviews')
    op.drop_index('ix_reviews_user_id', table_name='reviews')
    op.create_index(op.f('ix_reviews_productId'), 'reviews', ['productId'], unique=False)
    op.create_index(op.f('ix_reviews_userId'), 'reviews', ['userId'], unique=False)
    op.drop_constraint('reviews_product_id_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('reviews_user_id_fkey', 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'users', ['userId'], ['id'])
    op.create_foreign_key(None, 'reviews', 'products', ['productId'], ['id'])
    op.drop_column('reviews', 'user_id')
    op.drop_column('reviews', 'created_At')
    op.drop_column('reviews', 'product_id')
    op.drop_column('reviews', 'updated_At')
    op.add_column('users', sa.Column('imageUrl', sa.String(), nullable=True))
    op.add_column('users', sa.Column('createdAt', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updatedAt', sa.DateTime(), nullable=True))
    op.drop_column('users', 'image_URL')
    op.drop_column('users', 'created_At')
    op.drop_column('users', 'updated_At')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('updated_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('created_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('image_URL', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'updatedAt')
    op.drop_column('users', 'createdAt')
    op.drop_column('users', 'imageUrl')
    op.add_column('reviews', sa.Column('updated_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('reviews', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('reviews', sa.Column('created_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('reviews', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key('reviews_user_id_fkey', 'reviews', 'users', ['user_id'], ['id'])
    op.create_foreign_key('reviews_product_id_fkey', 'reviews', 'products', ['product_id'], ['id'])
    op.drop_index(op.f('ix_reviews_userId'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_productId'), table_name='reviews')
    op.create_index('ix_reviews_user_id', 'reviews', ['user_id'], unique=False)
    op.create_index('ix_reviews_product_id', 'reviews', ['product_id'], unique=False)
    op.drop_column('reviews', 'updatedAt')
    op.drop_column('reviews', 'createdAt')
    op.drop_column('reviews', 'productId')
    op.drop_column('reviews', 'userId')
    op.add_column('products', sa.Column('updated_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('products', sa.Column('created_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('image_URL', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.create_foreign_key('products_category_id_fkey', 'products', 'categories', ['category_id'], ['id'])
    op.drop_column('products', 'updatedAt')
    op.drop_column('products', 'createdAt')
    op.drop_column('products', 'categoryId')
    op.drop_column('products', 'imageUrl')
    op.add_column('categories', sa.Column('updated_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('categories', sa.Column('created_At', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('categories', 'updatedAt')
    op.drop_column('categories', 'createdAt')
    # ### end Alembic commands ###
