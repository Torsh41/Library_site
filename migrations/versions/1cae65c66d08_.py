"""empty message

Revision ID: 1cae65c66d08
Revises: d6affd863e32
Create Date: 2024-04-15 17:07:57.656187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cae65c66d08'
down_revision = 'd6affd863e32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TABLE books ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catalogues',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_catalogues_name', 'catalogues', ['name'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_categories_name', 'categories', ['name'], unique=False)
    op.create_table('books_maintaining',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('authors', sa.VARCHAR(length=128), nullable=True),
    sa.Column('series', sa.VARCHAR(length=128), nullable=True),
    sa.Column('categories', sa.VARCHAR(length=128), nullable=True),
    sa.Column('publishing_date', sa.INTEGER(), nullable=True),
    sa.Column('publishing_house', sa.VARCHAR(length=128), nullable=True),
    sa.Column('pages_count', sa.INTEGER(), nullable=True),
    sa.Column('isbn', sa.VARCHAR(length=64), nullable=True),
    sa.Column('comments', sa.VARCHAR(length=64), nullable=True),
    sa.Column('summary', sa.TEXT(), nullable=True),
    sa.Column('link', sa.VARCHAR(length=256), nullable=True),
    sa.Column('count', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_books_maintaining_name', 'books_maintaining', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('avatar', sa.BLOB(), nullable=True),
    sa.Column('city', sa.VARCHAR(length=64), nullable=True),
    sa.Column('gender', sa.VARCHAR(length=4), nullable=True),
    sa.Column('age', sa.INTEGER(), nullable=True),
    sa.Column('about_me', sa.TEXT(), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('confirmed', sa.BOOLEAN(), nullable=True),
    sa.Column('role', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_index('ix_users_timestamp', 'users', ['timestamp'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.create_table('topics',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('category_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_topics_name', 'topics', ['name'], unique=False)
    op.create_table('grades',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('grade', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('book_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('search_results',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cover', sa.BLOB(), nullable=True),
    sa.Column('isbn', sa.VARCHAR(length=64), nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('author', sa.VARCHAR(length=64), nullable=True),
    sa.Column('publishing_house', sa.VARCHAR(length=64), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('release_date', sa.DATE(), nullable=True),
    sa.Column('count_of_chapters', sa.INTEGER(), nullable=True),
    sa.Column('grade', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_search_results_name', 'search_results', ['name'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('read_state', sa.VARCHAR(length=64), nullable=True),
    sa.Column('cataloge_id', sa.INTEGER(), nullable=True),
    sa.Column('book_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['cataloge_id'], ['catalogues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cover', sa.BLOB(), nullable=True),
    sa.Column('isbn', sa.VARCHAR(length=64), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('author', sa.VARCHAR(length=128), nullable=True),
    sa.Column('publishing_house', sa.VARCHAR(length=128), nullable=True),
    sa.Column('description', sa.TEXT(length=512), nullable=True),
    sa.Column('release_date', sa.DATE(), nullable=True),
    sa.Column('count_of_chapters', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('category_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_books_name', 'books', ['name'], unique=False)
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('file', sa.BLOB(), nullable=True),
    sa.Column('answer_to_post', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('discussion_topic_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['discussion_topic_id'], ['topics.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    op.create_index('ix_posts_body', 'posts', ['body'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.TEXT(length=512), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('book_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comments_timestamp', 'comments', ['timestamp'], unique=False)
    # ### end Alembic commands ###
