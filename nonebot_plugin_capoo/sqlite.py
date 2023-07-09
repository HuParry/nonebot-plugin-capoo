import sqlite3

# 数据库中存的是 md5 码和 picture以capoo为根目录的路径
def check_md5(conn: sqlite3.Connection, cursor: sqlite3.Cursor, fmd5: str, pic_name: str) -> bool:
    cursor.execute('SELECT * FROM Picture WHERE md5 = ?', (fmd5,))
        
    status = cursor.fetchone()
    if status is not None:
        return False
    
    cursor.execute('INSERT INTO Picture (md5, img_url) VALUES (?, ?)', (fmd5, pic_name))
    conn.commit()
    return True