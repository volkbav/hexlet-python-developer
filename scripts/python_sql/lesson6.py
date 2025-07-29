from psycopg2.extras import DictCursor

from db_connection import get_connection

conn = get_connection()


# BEGIN (write your solution here)
def create_post(conn, data_post):
    with conn.cursor() as curs:
        query = """INSERT INTO posts (
        title, content, author_id, created_at)
        VALUES (%(title)s, %(content)s, %(author_id)s, NOW())
        RETURNING id;"""
        curs.execute(query, data_post)
        post_id = curs.fetchone()[0]
        conn.commit()
    return post_id


def add_comment(conn, data_comment):
    with conn.cursor() as curs:
        query = """INSERT INTO comments (
        post_id, author_id, content, created_at)
        VALUES (%(post_id)s, %(author_id)s, %(content)s, NOW())
        RETURNING id;"""
        curs.execute(query, data_comment)
        comment_id = curs.fetchone()[0]
        conn.commit()
    return comment_id

def get_latest_posts(conn, post_count):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        posts_query = """SELECT 
        p.id, p.title, p.content, p.author_id,
        p.created_at
        FROM posts AS p
        ORDER BY p.created_at DESC
        LIMIT %s;"""
        
        comments_query = """SELECT 
            c.id, c.content, c.created_at
        FROM comments AS c
        WHERE c.id=%s
        ORDER BY c.created_at;"""

        curs.execute(posts_query, (post_count,))
        posts = curs.fetchall()
        result = []
        for post in posts:
            curs.execute(comments_query, (post['id'],))
            comments = curs.fetchall()

            post_data = {
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'author_id': post['author_id'],
                'created_at': post['created_at'],
                'comments': comments
            }
            result.append(post_data)

        return result
 #       for row in rows:
 #           curs.execute(comments_query, row['id'])

        

# END


print(get_latest_posts(conn, 3))
# []
#post = {'title': 'My Super Post', 'content': 'text', 'author_id': 42}
#print(create_post(conn, post))
# 1
#comment = {'post_id': 1, 'author_id': 42, 'content': 'wow such post'}
#print(add_comment(conn, comment))
# [{
# 'id': 1,
# 'title': 'My Super Post',
# 'content': 'text',
# 'author_id': 42,
# 'created_at': datetime.datetime(2022, 7, 19, 14, 32, 37, 123857),
# 'comments': [
#  {
#   'id': 1,
#   'author_id': 42,
#   'content': 'wow such post',
#   'created_at': datetime.datetime(2022, 8, 19, 14, 32, 37, 135319)
#   }
#  ]}]

conn.close()

