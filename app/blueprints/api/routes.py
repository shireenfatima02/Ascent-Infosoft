import json
from pathlib import Path
from flask import jsonify, current_app

from . import bp


def _load_location_data():
    override = current_app.config.get("DATA_PATH")
    if override:
        p = Path(override)
    else:
        p = Path(current_app.root_path).parent / "data" / "countries+states+cities.json"
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # pragma: no cover
        current_app.logger.error(f"Failed to load location data: {e}")
        return []


@bp.route("/countries")
def get_countries():
    countries = _load_location_data()
    return jsonify([{"id": c.get("id"), "name": c.get("name")} for c in countries])


@bp.route("/states/<int:country_id>")
def get_states(country_id):
    countries = _load_location_data()
    country = next((c for c in countries if c.get("id") == country_id), None)
    if not country:
        return jsonify([])
    return jsonify([{"id": s.get("id"), "name": s.get("name")} for s in country.get("states", [])])


@bp.route("/cities/<int:state_id>")
def get_cities(state_id):
    countries = _load_location_data()
    for country in countries:
        for state in country.get("states", []):
            if state.get("id") == state_id:
                return jsonify([{"id": c.get("id"), "name": c.get("name")} for c in state.get("cities", [])])
    return jsonify([])

