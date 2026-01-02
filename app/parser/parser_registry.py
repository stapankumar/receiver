from app.parser.agri_parser import parse_agri, parse_agri_summary
from app.parser.water_parser import parse_water
from app.parser.waste_parser import parse_waste
from app.parser.pond_parser import parse_pond
from app.parser.edu_parser import parse_edu

PARSER_REGISTRY = {
    "agri": {
        "parser": parse_agri,
        "summary": parse_agri_summary,
        "columns": {
            "Dev_SN": "Device Serial No.",
            "AirTemp": "Air Temperature (°C)",
            "AirHumi": "Air Humidity (%)",
            "SoilTemp": "Soil Temperature (°C)",
            "SoilHumi": "SSoil Humidity (%)",
            "Nitrogen": "Nitrogen (mg/kg)",
            "Phosphorus": "Phosphorus (mg/kg)",
            "Potassium": "Potassium (mg/kg)",
            "power_Status": "Power Status",
            "batt_Level": "Battery Level",
        }
    },
    "water": {
        "parser": parse_water,
        "columns": {
        }
    },
    "waste": {
        "parser": parse_waste,
        "columns": {
        }
    },
    "pond": {
        "parser": parse_pond,
        "columns": {
        }
    },
    "edu": {
        "parser": parse_edu,
        "columns": {
        }
    }
}