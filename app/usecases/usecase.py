from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone

from app.db.notifications_repo import (
    insert_notification_usecase,
    fetch_recent_usecase,
    fetch_notifications_since_usecase   
)

from app.parser.usecase_parser import parse_usecase_notification, parse_usecase_summary
from app.usecases.registry import USECASE_REGISTRY
from app.parser import parser_registry

PARSER_REGISTRY = parser_registry.PARSER_REGISTRY

usecase_bp = Blueprint("usecase",__name__)

# -----------------------------
# IST handling (naive DB safe)
# -----------------------------
IST_OFFSET = timedelta(hours=5, minutes=30)
IST = timezone(IST_OFFSET)

def now_ist_naive():
    return datetime.now(IST).replace(tzinfo=None)


@usecase_bp.route("/notify/<usecase>", methods=["POST"])
def receive_usecase(usecase):
    config = USECASE_REGISTRY.get(usecase)
    if not config:
        return jsonify({
            "error": "Unknown usecase",
            "usecase": usecase
        }), 404

    table = config["table"]
    
    print("\nUsecase Notification received!", flush=True)
    print(f"URL Path: {request.path}", flush=True)
    print(f"Method: {request.method}", flush=True)
    print(f"Headers:\n{request.headers}", flush=True)
    try:
        payload = request.get_data(as_text=True)
        print(f"Raw Payload:\n{payload}", flush=True)

        insert_notification_usecase(
            table,
            request.path,
            request.method,
            request.headers,
            payload
        )

        print("usecase Notification stored", flush=True)

    except Exception as e:
        print(f"Failed to decode payload: {e}", flush=True)

    return "Usecase notification received and stored successfully", 200


@usecase_bp.route("/data/<usecase>", methods=["GET"])
def get_parsed_usecase_data(usecase):
    config = USECASE_REGISTRY.get(usecase)
    if not config:
        return jsonify({
            "error": "Unknown usecase",
            "usecase": usecase
        }), 404

    table = config["table"]
    parser_type = config["parser"]

    rows = fetch_recent_usecase(table, 50)
    
    #print(f"Fetched {len(rows)} rows from {table}", flush=True)
    #print(rows, flush=True)

    parsed_results = []

    columns = PARSER_REGISTRY.get(parser_type).get("columns")
    parsed_results.append(columns)

    for r in rows:
        parsed_con = parse_usecase_notification(parser_type, r[1])

        response_obj = {}

        #flatten sensor data
        if isinstance(parsed_con, dict):
            response_obj.update(parsed_con)

        #append metadata
        response_obj["notification_id"] = r[0]
        response_obj["received_at"] = r[2].isoformat()


        parsed_results.append(response_obj)

    return jsonify(parsed_results)


@usecase_bp.route("/data/<usecase>/summary", methods=["GET"])
def get_usecase_summary(usecase):
    """
    Returns a SINGLE JSON object with:
    - Hourly averages (last 1 hour)
    - Daily averages (last 24 hours)
    Timezone: IST (naive, DB-safe)
    """

    config = USECASE_REGISTRY.get(usecase)
    if not config:
        return jsonify({
            "error": "Unknown usecase",
            "usecase": usecase
        }), 404

    table = config["table"]
    parser_type = config["parser"]

    now_ist = now_ist_naive()
    since_24h = now_ist - timedelta(hours=24)

    #fetch raw rows (parsing happens later)
    rows = fetch_notifications_since_usecase(table, since_24h)

    summary = parse_usecase_summary(parser_type, rows)

    return jsonify(summary)
