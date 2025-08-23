import sqlite3

def create_table():
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT ,
            title TEXT NOT NULL ,
            content TEXT NOT NULL ,
            image TEXT,
            time DATETIME DEFAULT CURRENT_TIMESTAMP)  
            ''')
    # cur.execute("DELETE FROM posts") 
    con.commit() 
    con.close()
    
def add_posts(Title , Content , image=None):
    con =sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute( "INSERT INTO posts (title , content ,image)  VALUES (? ,?,?)", (Title , Content,image))
    con.commit()
    con.close()   

def get_posts():
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("SELECT id , title , content , image, time FROM posts ORDER BY time DESC")
    posts=cur.fetchall()
    con.commit()
    con.close()
    return posts 
    
def delet_posts(post_id):
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("DELETE FROM posts WHERE id=?", (post_id,))
    con.commit()
    con.close()
    
def search(search_query):
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("SELECT id, title, content, time FROM posts WHERE title LIKE ? ORDER BY time DESC" ,('%'+search_query+'%' ,))
    result=cur.fetchall()
    return result