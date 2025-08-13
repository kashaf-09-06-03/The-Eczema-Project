import sqlite3

def create_table():
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT ,
            title TEXT NOT NULL ,
            content TEXT NOT NULL ,
            time DATETIME DEFAULT CURRENT_TIMESTAMP)  
            ''')
    # cur.execute("DELETE FROM posts") 
    con.commit()
    con.close()
    
def add_posts(Title , Content):
    con =sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("INSERT INTO posts (title , content )  VALUES (? ,?)", (Title , Content))
    con.commit()
    con.close()   

def get_posts():
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("SELECT title , content , time FROM posts ORDER BY time DESC")

    posts=cur.fetchall()
    con.commit()
    con.close()
    
    return posts 
    