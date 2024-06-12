import sqlite3


def get_connection():
    return sqlite3.connect("db/logs_db.db")


def create_db():
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


def drop_db():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('drop table Log')
    connection.commit()


create_db()
print("База данных успешно подключена")
