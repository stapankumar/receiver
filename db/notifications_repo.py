import json
from db.connection import get_db_conn


def insert_notification(path, method, headers, payload):
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO "M2M_NOTIFICATIONS"."RESOURCE_NOTIFICATION"
        (path, method, headers, payload)
        VALUES (%s, %s, %s, %s)
        """,
        (
            path,
            method,
            json.dumps(dict(headers)),
            payload
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def fetch_latest():
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT path, method, headers, payload
        FROM "M2M_NOTIFICATIONS"."RESOURCE_NOTIFICATION"
        ORDER BY received_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def fetch_recent(limit):
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload, received_at
        FROM "M2M_NOTIFICATIONS"."RESOURCE_NOTIFICATION"
        ORDER BY received_at DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
