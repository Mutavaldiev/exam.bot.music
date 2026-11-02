from connection import *



async def create_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            insert into users(username, full_name, telegram_id) values
            ($1, $2, $3)
        """, username, full_name, str(telegram_id))
    except Exception as Error:
        print(f"Create user Error: {Error}")
    finally:
        await conn.close()





async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
            select * from users
            where telegram_id = $1
        """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user Error: {Error}")
        return None
    finally:
        await conn.close()





async def check_admin(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
            select * FROM users
            where telegram_id = $1 and is_admin = true
        """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Check admin Error: {Error}")
        return None
    finally:
        await conn.close()





async def add_song_db(title, artist, audio_file_id, author_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            insert into songs (title, artist, audio_file_id, author_id) values 
            ($1, $2, $3, $4)
        """, title, artist, audio_file_id, author_id)
        return True
    except Exception as Error:
        print(f"Add song Error: {Error}")
        return False
    finally:
        await conn.close()






async def get_all_songs():
    try:
        conn = await connection_db()
        songs = await conn.fetch("""
            select * from songs
            order by songs_id desc
        """)
        return songs
    except Exception as Error:
        print(f"Get all songs Error: {Error}")
        return []
    finally:
        await conn.close()




async def get_song_by_id(song_id):
    try:
        conn = await connection_db()
        song = await conn.fetchrow("""
            select * FROM songs
            where songs_id = $1
        """, song_id)
        return song
    except Exception as Error:
        print(f"Get song by id Error: {Error}")
        return None
    finally:
        await conn.close()




async def add_song_to_playlist(user_id, song_id):
    try:
        conn = await connection_db()
        result = await conn.execute("""
            insert into playlist_items(user_id, songs_id)
            select user_id, $2 from users
            where telegram_id = $1
        """, str(user_id), song_id)
        return True
    except Exception as Error:
        print(f"Add Error: {Error}")
        return False
    finally:
        await conn.close()






async def remove_song_from_playlist(user_id, song_id):
    try:
        conn = await connection_db()
        result = await conn.execute("""
            delete from playlist_items using users
            where users.user_id = playlist_items.user_id and users.telegram_id = $1 and playlist_items.songs_id = $2
        """, str(user_id), song_id)
        return True
    except Exception as Error:
        print(f"Remove Error: {Error}")
        return False
    finally:
        await conn.close()




async def get_user_playlist(user_id):
    try:
        conn = await connection_db()
        songs = await conn.fetch("""
            select songs.* FROM playlist_items
            join users on users.user_id = playlist_items.user_id
            join songs on songs.songs_id = playlist_items.songs_id
            where users.telegram_id = $1
        """, str(user_id))
        return songs
    except Exception as Error:
        print(f"Get playlist Error: {Error}")
        return []
    finally:
        await conn.close()




async def get_playlist_stats(user_id):
    try:
        conn = await connection_db()
        count = await conn.fetchval("""
            select count(*) from playlist_items
            join users ON users.user_id = playlist_items.user_id
            where users.telegram_id = $1
        """, str(user_id))
        return count
    except Exception as Error:
        print(f"Playlist stats Error: {Error}")
        return 0

    finally:
        await conn.close()



async def delete_song(song_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        delete from songs 
        where songs_id = $1""", song_id)
        return True
    except Exception as Error:
        print(Error)
        return False
    finally:
        await conn.close()