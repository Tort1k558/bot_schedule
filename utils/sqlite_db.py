import sqlite3 as sq


def sql_start():
    global conn
    conn = sq.connect('/app/database/users.db')
    if conn:
        print('Data base connected')
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, group_name TEXT)")
    conn.commit()


async def change_group_name(chat_id, group_name):
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE chat_id=?', (chat_id,))
    existing_row = cursor.fetchone()
    if existing_row:
        cursor.execute('UPDATE users SET group_name=? WHERE chat_id=?', (group_name, chat_id))
    else:
        cursor.execute('INSERT INTO users (chat_id, group_name) VALUES (?, ?)', (chat_id, group_name))
    conn.commit()


async def get_group_name(chat_id):
    cursor = conn.cursor()
    cursor.execute('SELECT group_name FROM users WHERE chat_id=?', (chat_id,))
    row = cursor.fetchone()
    return row[0] if row else None


async def get_id(chat_id):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE chat_id=?', (chat_id,))
    row = cursor.fetchone()
    return row[0] if row else None
