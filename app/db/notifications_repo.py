import json
from datetime import datetime, timedelta, timezone
from app.db.connection import get_db_conn

TABLE_DEFAULT = '"APPLICATION_DATA"."RESOURCE_NOTIFICATION"'

#IST handling
IST_OFFSET = timedelta(hours=5, minutes=30)
IST = timezone(IST_OFFSET)

def now_ist_naive():
    return datetime.now(IST).replace(tzinfo=None)

def insert_notification_usecase(table, path, method, headers, payload):
    conn = get_db_conn()
    cur = conn.cursor()

    query = f"""
        INSERT INTO {table}
        (path, method, headers, payload, received_at)
        VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(
        query,
        (
            path,
            method,
            json.dumps(dict(headers)),
            payload,
            now_ist_naive()
        )
    )

    conn.commit()
    cur.close()
    conn.close()

def insert_notification(path, method, headers, payload):
    conn = get_db_conn()
    cur = conn.cursor()

    query = f"""
        INSERT INTO {TABLE_DEFAULT}
        (path, method, headers, payload, received_at)
        VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(
        query,
        (
            path,
            method,
            json.dumps(dict(headers)),
            payload,
            now_ist_naive()
        )
    )

    conn.commit()
    cur.close()
    conn.close()

def fetch_recent_usecase(table, limit):
    conn = get_db_conn()
    cur = conn.cursor()

    query = f"""
        SELECT id, payload, received_at
        FROM {table}
        ORDER BY received_at DESC
        LIMIT %s
    """

    cur.execute(query, (limit,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def fetch_recent(limit):
    conn = get_db_conn()
    cur = conn.cursor()

    query = f"""
        SELECT id, payload, received_at
        FROM {TABLE_DEFAULT}
        ORDER BY received_at DESC
        LIMIT %s
    """

    cur.execute(query, (limit,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def fetch_latest():
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT path, method, headers, payload
        FROM "APPLICATION_DATA"."RESOURCE_NOTIFICATION"
        ORDER BY received_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def fetch_notifications_since_usecase(table, since):
    """
    Fetch notifications received since a given time.
    Args:
        table (str): Fully qualified table name
        since (datetime): Naive datetime (IST, matches DB)

    Returns:
        list[dict]: Each item contains payload and received_at
    """
    conn = get_db_conn()
    cur = conn.cursor()

    query = f"""
        SELECT payload, received_at
        FROM {table}
        WHERE received_at >= %s
        ORDER BY received_at ASC
    """

    cur.execute(query, (since,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    #normalize rows into dicts (clean contract for parser)
    results = []
    for payload, received_at in rows:
        results.append({
            "payload": payload,
            "received_at": received_at
        })

    return results