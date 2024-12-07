import sqlite3
from config import dataconfig as data


############################################### Database setup ###################################################

# Creating database
con=sqlite3.connect(data.DATABASE)


con.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL,
    name TEXT NOT NULL, 
    email TEXT NOT NULL, 
    phone_number TEXT NOT NULL, 
    password TEXT NOT NULL,
    avatar TEXT NOT NULL DEFAULT ('default_avatar.png'),
    is_admin BOOLEAN DEFAULT (FALSE)
);''')


con.execute('''
CREATE TABLE IF NOT EXISTS Song (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    duration INTEGER,
    album_id INTEGER,
    lyrics TEXT,
    artist TEXT NOT NULL,
    uploader TEXT NOT NULL,
    genre TEXT,
    release_date DATE,
    FOREIGN KEY (album_id) REFERENCES Album(album_id)
);''')


con.execute('''
CREATE TABLE IF NOT EXISTS Album (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT NOT NULL, 
    artist TEXT NOT NULL, 
    genre TEXT, 
    release_date DATE, 
    cover_image_url TEXT
);''')


con.execute('''
CREATE TABLE IF NOT EXISTS Rating (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER NOT NULL, 
    song_id INTEGER NOT NULL, 
    rating INTEGER CHECK (rating BETWEEN 1 AND 5), 
    review TEXT, 
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (user_id) REFERENCES User(user_id), 
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);''')


con.execute('''
CREATE TABLE IF NOT EXISTS Playlist (
    playlist_id INTEGER PRIMARY KEY, 
    user_id INTEGER NOT NULL, 
    name TEXT NOT NULL, 
    description TEXT, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);''')


con.execute('''
CREATE TABLE IF NOT EXISTS PlaylistSong (
    playlist_song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER NOT NULL, 
    song_id INTEGER NOT NULL, 
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id), 
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);''')


con.close()


# DBConnection
def get_db_connection():
    conn = sqlite3.connect(data.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

##################################################################################################################
