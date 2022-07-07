import sqlite3

conn = sqlite3.connnect('test.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE hamburger (
                name VARCHAR(32),
                price INT,
                kcal INT)
            """)
cur.execute("INSERT INTO hamburger VALUES ('버거킹', 13000, 878)")

conn.commit()

