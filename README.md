```
# Music Player Platform - Database Schema & Features

## Overview

The **Music Player Platform** is an application that allows users to listen to music, create playlists, rate songs, and discover albums. This platform connects users with their favorite songs, albums, and playlists, while offering the ability to rate and review songs, create personalized playlists, and explore a variety of music genres.

This project defines a **relational database schema** that powers the backend of the platform. The database structure stores and organizes data about users, songs, albums, ratings, and playlists, ensuring smooth interaction and access to music-related content.

---

## Features of the Music Player Platform

- **User Registration and Profile**: Users can create and manage their profiles.
- **Song Playback**: Users can play songs from albums, rated by genre, release date, etc.
- **Album & Song Library**: A vast collection of albums and songs with detailed metadata like artist, genre, duration, and more.
- **Playlist Creation**: Users can create, edit, and manage playlists by adding their favorite songs.
- **Rating and Reviews**: Users can rate songs from 1 to 5 stars, and write reviews for each song they rate.
- **Music Discovery**: Users can explore albums and songs by artist, genre, or popularity.
- **Personalized Experience**: Tailored playlists, song recommendations, and ratings based on user activity.

---

## Database Schema

The **Music Player Database** consists of several interconnected tables, each representing key components of the platform. Below are the main tables used in the schema:

### 1. User Table
This table stores information about users, such as their profile details and credentials.

```sql
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    address TEXT, 
    contact_number TEXT, 
    password TEXT NOT NULL
);
```

- **Primary Key**: `user_id`
- **Related Data**: Stores user details like name, address, contact number, and password.

---

### 2. Album Table
This table contains details about music albums, including their title, artist, genre, release date, and cover image URL.

```sql
CREATE TABLE IF NOT EXISTS Album (
    album_id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    artist TEXT NOT NULL, 
    genre TEXT, 
    release_date DATE, 
    cover_image_url TEXT
);
```

- **Primary Key**: `album_id`
- **Related Data**: Represents a music album, its genre, release date, and cover image.

---

### 3. Song Table
The `Song` table stores details about each song, including the title, duration, artist, genre, and the album it belongs to.

```sql
CREATE TABLE IF NOT EXISTS Song (
    song_id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    duration INTEGER, 
    album_id INTEGER, 
    artist TEXT NOT NULL, 
    genre TEXT, 
    release_date DATE, 
    FOREIGN KEY (album_id) REFERENCES Album(album_id)
);
```

- **Primary Key**: `song_id`
- **Foreign Key**: `album_id` references `Album(album_id)`
- **Related Data**: Represents individual songs, their durations, associated albums, and artists.

---

### 4. Rating Table
The `Rating` table stores user ratings for songs along with optional reviews and the timestamp of when the rating was given.

```sql
CREATE TABLE IF NOT EXISTS Rating (
    rating_id INTEGER PRIMARY KEY, 
    user_id INTEGER NOT NULL, 
    song_id INTEGER NOT NULL, 
    rating INTEGER CHECK (rating BETWEEN 1 AND 5), 
    review TEXT, 
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (user_id) REFERENCES User(user_id), 
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);
```

- **Primary Key**: `rating_id`
- **Foreign Keys**: 
  - `user_id` references `User(user_id)`
  - `song_id` references `Song(song_id)`
- **Related Data**: Stores ratings (1-5) and reviews for songs by users.

---

### 5. Playlist Table
The `Playlist` table allows users to create and manage their playlists, with each playlist belonging to a specific user.

```sql
CREATE TABLE IF NOT EXISTS Playlist (
    playlist_id INTEGER PRIMARY KEY, 
    user_id INTEGER NOT NULL, 
    name TEXT NOT NULL, 
    description TEXT, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);
```

- **Primary Key**: `playlist_id`
- **Foreign Key**: `user_id` references `User(user_id)`
- **Related Data**: Represents playlists created by users, including name and description.

---

### 6. PlaylistSong Table
This table establishes a many-to-many relationship between playlists and songs.

```sql
CREATE TABLE IF NOT EXISTS PlaylistSong (
    playlist_song_id INTEGER PRIMARY KEY, 
    playlist_id INTEGER NOT NULL, 
    song_id INTEGER NOT NULL, 
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id), 
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);
```

- **Primary Key**: `playlist_song_id`
- **Foreign Keys**: 
  - `playlist_id` references `Playlist(playlist_id)`
  - `song_id` references `Song(song_id)`
- **Related Data**: Links songs to playlists, allowing users to build customized playlists.

---

## Database Relationships

- **User to Playlist**: A user can create multiple playlists.
- **Album to Song**: An album contains multiple songs.
- **Song to Rating**: A song can receive ratings from multiple users.
- **Song to Playlist**: A song can be added to multiple playlists, and a playlist can contain multiple songs (many-to-many relationship).
  
---

## Example Use Cases

1. **Creating a Playlist**: A user can create a playlist and add their favorite songs.
   - **SQL**: Insert a new playlist into the `Playlist` table and associate songs through the `PlaylistSong` table.

2. **Rating a Song**: Users can rate songs from 1 to 5 and provide reviews.
   - **SQL**: Insert a rating into the `Rating` table, linking the `user_id` and `song_id`.

3. **Exploring Albums and Songs**: Users can browse albums and listen to songs.
   - **SQL**: Query the `Album` and `Song` tables to display albums and songs to the user.

---

## How to Use the Database

1. **Set up the Database**: Execute the provided SQL queries to create the tables in your database.
2. **Populate the Tables**: Insert sample data into the tables to test the platform.
3. **Query the Database**: Use SQL queries to interact with the data, such as retrieving songs, albums, playlists, or ratings.

---

## Future Enhancements

- **Advanced Search**: Implement search functionality for users to find songs, albums, or playlists by title, artist, or genre.
- **Social Features**: Allow users to share playlists and follow other users.
- **Song Recommendations**: Implement personalized song recommendations based on user ratings and listening history.
- **Activity Logs**: Track user activity like recently played songs, playlists, and ratings.

---

## Conclusion

The **Music Player Platform** database schema is designed to handle all essential aspects of a music player app, including user management, song discovery, playlist creation, and ratings. It supports a smooth and personalized user experience, enabling users to interact with their favorite songs and albums in various ways.
```
