# Music Player Database Schema

## Overview
This project defines a relational database schema for a music player application. The database is designed to store and manage information about users, albums, songs, ratings, playlists, and the relationships between them.

## Database Tables
### 1. **User Table**
Stores user details such as name, contact information, and password.
- **Relationships:**
  - Users can create multiple playlists.
  - Users can rate songs.

### 2. **Album Table**
Represents music albums, including title, artist, genre, release date, and cover image URL.
- **Relationships:**
  - Contains songs associated with the album.

### 3. **Song Table**
Contains information about songs, including title, duration, artist, genre, and release date.
- **Relationships:**
  - Belongs to an album (optional).
  - Can be rated by users.
  - Can be added to playlists.

### 4. **Rating Table**
Stores user ratings and reviews for songs, along with a timestamp.
- **Relationships:**
  - Links users to songs through ratings.

### 5. **Playlist Table**
Represents user-created playlists, including name, description, and creation date.
- **Relationships:**
  - Belongs to a user.
  - Can contain multiple songs.

### 6. **PlaylistSong Table**
Establishes a many-to-many relationship between playlists and songs.
- **Relationships:**
  - Links songs to playlists.

## Key Features
- **User Management**: Tracks user details and allows them to create playlists and rate songs.
- **Albums and Songs**: Stores detailed information about albums and their associated songs.
- **Ratings and Reviews**: Allows users to provide feedback on songs with a rating system.
- **Playlists**: Enables users to create and manage personalized playlists.
- **Relational Links**: Ensures seamless connectivity between users, songs, albums, ratings, and playlists.

## Database Schema
- **Primary Keys**:
  - `user_id`, `album_id`, `song_id`, `rating_id`, `playlist_id`, `playlist_song_id`
- **Foreign Keys**:
  - `album_id` in `Song` references `Album`.
  - `user_id` in `Rating` references `User`.
  - `song_id` in `Rating` references `Song`.
  - `user_id` in `Playlist` references `User`.
  - `playlist_id` and `song_id` in `PlaylistSong` reference `Playlist` and `Song`.

## Example Use Cases
1. **User Rating a Song**:
   - Insert a record in the `Rating` table linking a `user_id` to a `song_id` with a score and optional review.
2. **Creating a Playlist**:
   - Add a record in the `Playlist` table for a user.
   - Use the `PlaylistSong` table to associate songs with the playlist.
3. **Viewing Songs in an Album**:
   - Query the `Song` table where `album_id` matches a specific album.

## Future Enhancements
- **Search Functionality**: Allow users to search songs by title, artist, or genre.
- **User Activity Tracking**: Add a log for recently played songs or playlists.
- **Social Features**: Enable users to share playlists and view top-rated songs.

## How to Use
1. Set up the database using the provided SQL queries.
2. Populate the tables with data using `INSERT` statements or a migration script.
3. Query the database to interact with users, albums, songs, ratings, and playlists.

This schema forms the backbone of a feature-rich music player app, ready for integration into a broader application framework.
