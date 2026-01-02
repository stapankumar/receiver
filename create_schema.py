from app.db.connection import get_db_conn

INIT_SQL_FILE = "init.sql"

def init_db():
    conn = get_db_conn()
    cur = conn.cursor()

    with open(INIT_SQL_FILE, "r") as f:
        sql = f.read()

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    print("Schema and tables initialization successful.")


if __name__ == "__main__":
    init_db()
