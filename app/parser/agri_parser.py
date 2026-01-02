import json
from datetime import datetime, timedelta, timezone

#IST handling
IST_OFFSET = timedelta(hours=5, minutes=30)
IST = timezone(IST_OFFSET)

def now_ist_naive():
    return datetime.now(IST).replace(tzinfo=None)

def parse_agri(payload):
    """
    Parse smart-agri notification payload
    """

    if not payload:
        return {}

    # if payload is string → JSON
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            return {}

    try:
        con = (
            payload["m2m:sgn"]
                   ["nev"]
                   ["rep"]
                   ["any"]
                   ["con"]
        )
    except (KeyError, TypeError):
        return {}

    if not isinstance(con, dict):
        return {}

    key_map = {
        "A_Humi": "AirHumi",
        "A_Temp": "AirTemp",
        "S_Humi": "SoilHumi",
        "S_Temp": "SoilTemp"
    }

    parsed = {}
    for k, v in con.items():
        parsed[key_map.get(k, k)] = v

    return parsed


def _safe_float(v):
    try:
        return float(v)
    except Exception:
        return None

def _calculate_total_pump_hours(pump_status_times, now):
    print(f"Calculating pump hours with {len(pump_status_times)} status points", flush=True)
    """
    pump_status_times: list of tuples (status, timestamp)
    status = "ON" or "OFF"
    timestamp = naive IST datetime
    Returns total pump running hours in float
    """
    if not pump_status_times:
        print("No pump status times available", flush=True)
        return 0.0

    total_seconds = 0
    for i in range(1, len(pump_status_times)):
        prev_status, prev_time = pump_status_times[i - 1]
        curr_status, curr_time = pump_status_times[i]
        if prev_status == "ON":
            delta_seconds = (curr_time - prev_time).total_seconds()
            if delta_seconds < 0:
                print(f"Negative time delta at index {i}: {prev_time} to {curr_time} = {delta_seconds}s", flush=True)
            else:
                print(f"Adding {delta_seconds}s from {prev_time} to {curr_time}", flush=True)
            total_seconds += delta_seconds

    #if last reading is ON, count till now
    if pump_status_times[-1][0] == "ON":
        last_time = pump_status_times[-1][1]
        delta_seconds = (now - last_time).total_seconds()
        if delta_seconds < 0:
            print(f"Negative time delta from last ON to now: {last_time} to {now} = {delta_seconds}s", flush=True)
        else:
            print(f"Adding {delta_seconds}s from last ON {last_time} to now {now}", flush=True)
        total_seconds += delta_seconds

    total_hours = round(total_seconds / 3600, 2)
    print(f"Total pump seconds: {total_seconds}, hours: {total_hours}", flush=True)
    return total_hours

def parse_agri_summary(rows):
    """
    rows: list of dicts
    {
        "payload": json | str,
        "received_at": naive datetime (IST)
    }

    Returns SINGLE JSON object:
    - Hourly averages (last 1 hour): Air + Soil
    - Daily averages (last 24 hours): NPK
    - Pump hours daily
    - Energy consumption daily
    """

    now = now_ist_naive()
    one_hour_ago = now - timedelta(hours=1)
    twenty_four_hours_ago = now - timedelta(hours=24)

    air_temp, air_humi = [], []
    soil_temp, soil_humi = [], []

    nitrogen, phosphorus, potassium = [], [], []
    pump_status_times = []  #list of tuples: (status, timestamp)
    print(f"Processing {len(rows)} rows for agri summary", flush=True)
    for row in rows:
        payload = row.get("payload")
        received_at = row.get("received_at")

        if not payload or not received_at:
            continue

        if received_at < twenty_four_hours_ago:
            continue

        # -------- Parse payload --------
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                continue

        try:
            con = payload["m2m:sgn"]["nev"]["rep"]["any"]["con"]
        except (KeyError, TypeError):
            continue

        if not isinstance(con, dict):
            continue

        app_type = con.get("App")

        # -------------------------------
        # Hourly averages (AIR + SOIL)
        # Ignore NPK packets
        # -------------------------------
        if received_at >= one_hour_ago and app_type != "NPK":

            air_temp.append(_safe_float(con.get("A_Temp")))
            air_humi.append(_safe_float(con.get("A_Humi")))
            soil_temp.append(_safe_float(con.get("S_Temp")))
            soil_humi.append(_safe_float(con.get("S_Humi")))

        # -------------------------------
        # Daily averages (NPK)
        # -------------------------------
        if app_type == "NPK":
            nitrogen.append(_safe_float(con.get("Nitrogen")))
            phosphorus.append(_safe_float(con.get("Phosphorus")))
            potassium.append(_safe_float(con.get("Potassium")))

        # -------------------------------
        # Pump running hours (daily)
        # -------------------------------
        if "Relay_Stat" in con and "Relay_4" in con["Relay_Stat"]:
            pump_status_times.append((con["Relay_Stat"]["Relay_4"], received_at))

    print(f"Collected {len(pump_status_times)} pump status points", flush=True)
    if pump_status_times:
        print(f"First status: {pump_status_times[0]}, Last status: {pump_status_times[-1]}", flush=True)

    def avg(values):
        values = [v for v in values if v is not None]
        return round(sum(values) / len(values), 2) if values else None

    total_pump_hours = _calculate_total_pump_hours(pump_status_times, now)
    energy_units = round(total_pump_hours * 1.5, 2) if total_pump_hours else None

    print(f"Final summary: TotalPumpRunningHours={total_pump_hours}, EnergyConsumptionUnits={energy_units}", flush=True)

    return {
        "AvgAirTemp": avg(air_temp),
        "AvgAirHumi": avg(air_humi),
        "AvgSoilTemp": avg(soil_temp),
        "AvgSoilHumi": avg(soil_humi),
        "AvgNitrogen": avg(nitrogen),
        "AvgPhosphorus": avg(phosphorus),
        "AvgPotassium": avg(potassium),
        "TotalPumpRunningHours": total_pump_hours,
        "EnergyConsumptionUnits": energy_units
    }
