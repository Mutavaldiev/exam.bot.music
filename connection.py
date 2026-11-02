from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()
pasw = os.getenv("DATABASE_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="music",
            password=pasw
        )
        return conn
    except Exception as Error:
        print(f"Connection Error: {Error}")

async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            user_id serial primary key,
            full_name varchar(100),
            username varchar(100),
            telegram_id text,
            is_admin boolean default false,
            created_at timestamp default now(),
            is_active boolean default true
        );

        create table if not exists songs(
            songs_id serial primary key,
            author_id int,
            title varchar(200),
            artist varchar(200),
            audio_file_id text,
            created_at timestamp default now(),
            is_active boolean default true
        );

        create table if not exists playlist_items(
            playlist_items_id serial primary key,
            user_id int references users(user_id),
            songs_id int references songs(songs_id),
            added_at timestamp default now(),
            created_at timestamp default now(),
            is_active boolean default true
        )

      """)
        print("Table created")
    except Exception as Error:
        print(f"Create Error: {Error}")
    finally:
        await conn.close()





async def send_photo(telegram_id, file_id, file_name):
    try:
        conn = await connection_db()
        await conn.execute("""
        INSERT INTO files(file_id, file_name, telegram_id) Values
        ($1, $2, $3)
                           """, file_id, file_name, str(telegram_id))
    except Exception as Error:
        print(f"Create photo error: {Error}")
    finally:
        await conn.close()





async def get_photo(telegram_id):
    try:
        conn = await connection_db()
        photos = await conn.fetch("""
        select * from files where telegram_id = $1
                           """, str(telegram_id))
        return photos
    except Exception as Error:
        print(f"get photo error: {Error}")
    finally:
        await conn.close()