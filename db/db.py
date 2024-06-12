import sqlite3

DATABASE_FILE = "db/logs_db.db"


def get_connection():
    """Establish and return a connection to the SQLite database"""
    return sqlite3.connect(DATABASE_FILE)


def create_db():
    """Create database structure"""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
    create table if not exists Log (
    id integer primary key autoincrement,
    ip varchar(45) not null,
    datetime timestamp not null,
    action text not null,
    status integer,
    unique (ip, datetime, action)
    )
        """)
        connection.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")


def drop_db():
    """Drop database structure"""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('drop table Log')
    connection.commit()


create_db()
print("База данных успешно подключена")
