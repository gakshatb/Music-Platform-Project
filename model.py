import sqlite3

############################################### Database setup ###################################################
# Creating database
con=sqlite3.connect("database.db")

# Initializing tables
con=sqlite3.connect("database.db")
con.execute("create table if not exists user(pid integer primary key,name text,address text,contact text,pwd text)")
con.execute("create table if not exists song(sid integer primary key,title text,singer text,date text,lyrics text,duration number, genre text, uploader text)")
con.execute("create table if not exists album(playlist_name text, sid text, user text)")
con.execute("create table if not exists rating (user_name text,sid integer references song(sid), rating integer, PRIMARY KEY (user_name, sid))")
con.execute("create table if not exists creator(pid integer primary key autoincrement,name text)")
con.close()

# DBConnection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
##################################################################################################################