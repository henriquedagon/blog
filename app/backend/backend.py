import psycopg2
from PIL import Image
from io import BytesIO


##################################################################################
# database
def conn_str():
    return "dbname='blog' user='postgres' password='postgres123++' host='localhost' port='5432'"

# --------------------------------
# Posts class
class Posts:
    '''Class for managing posts'''
    def __init__(self, db):
        '''(create and) connect to posts table'''
        self.conn = psycopg2.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''create table if not exists posts
                                            (
                                                id serial primary key, 
                                                title VARCHAR(100) not null, 
                                                post VARCHAR(1000) not null, 
                                                categories VARCHAR(1000) not null, 
                                                img_filename VARCHAR(1000) not null, 
                                                image_name VARCHAR(1000) not null,
                                                author VARCHAR(100) not null, 
                                                date VARCHAR(10) not null
                                            )''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert(self, title, post, categories, img_filename, image_name, author, date):
        self.cursor.execute(f'''insert into posts
                    (title, post, categories, img_filename, image_name, author, date) values 
                    ('{title}', '{post}', '{categories}', '{img_filename}', '{image_name}', '{author}', '{date}')''')
        self.conn.commit()

    def view(self):
        self.cursor.execute(f'''select title, post, categories, img_filename, image_name, author, date 
                                from posts
                                order by date desc''')
        rows = self.cursor.fetchall()
        return rows

# --------------------------------
# Posts class
class Users:
    '''Class for authenticate users'''
    def __init__(self, db):
        '''(create and) connect to users table'''
        self.conn = psycopg2.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''create table if not exists users
                                            (
                                                id serial primary key, 
                                                usr VARCHAR(100) not null, 
                                                pass VARCHAR(100) not null, 
                                                grp integer not null 
                                            )''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert(self, user, password, group):
        self.cursor.execute(f'''insert into users
                    (usr, pass, grp) values 
                    ('{user}', '{password}', '{group}')''')
        self.conn.commit()

    def verify(self, user, password):
        self.cursor.execute(f'''select '{user}', '{password}' from users 
                                where usr='{user}'
                                    and pass='{password}' ''')
        rows = self.cursor.fetchall()
        return rows == [(user, password)]



##################################################################################
# image

def image2byte(image):
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()

def file2byte(filename):
    with open(filename, 'rb') as f:
        b = bytearray(f.read())
    return b

def byte2image(b):
    return Image.open(BytesIO(b))


if __name__ == '__main__':
    posts = Posts(conn_str())
    print('posts:',posts.view())

    users = Users(conn_str())
    print('verify admin:',users.verify('administrador','12345'))