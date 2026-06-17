from fastapi import FastAPI
from models import CallResult
from database import init_db, save_call, get_all_calls
from fmcsa import verify_carrier
from negotiate import negotiate_rate
import json
from pathlib import Path

app = FastAPI(title="HappyRobot FDE Case Study API")

init_db()

LOADS_FILE = Path(__file__).parent / "loads.json"


@app.get("/")
def health_check():
    return {"status": "healthy"}


@app.get("/fmcsa/validate")
def validate_carrier(mc_number: str):
    return verify_carrier(mc_number)


@app.get("/loads/{reference_number}")
def get_load(reference_number: str):
    with open(LOADS_FILE, "r") as f:
        loads = json.load(f)

    for load in loads:
        if load["reference_number"] == reference_number:
            return load

    return {"error": "Load not found"}


@app.get("/negotiate")
def negotiate(load_rate: float, carrier_offer: float):
    return negotiate_rate(load_rate, carrier_offer)


@app.post("/save_call")
def save_call_result(call: CallResult):
    save_call(call)
    return {"message": "Call saved successfully"}


@app.get("/metrics")
def get_metrics():
    rows = get_all_calls()

    total_calls = len(rows)
    booked_loads = sum(1 for row in rows if row[7] == "BOOKED")
    failed_negotiations = sum(1 for row in rows if row[7] == "NEGOTIATION_FAILED")

    final_rates = [row[6] for row in rows if row[6] and row[6] > 0]
    average_final_rate = round(sum(final_rates) / len(final_rates), 2) if final_rates else 0

    return {
        "total_calls": total_calls,
        "booked_loads": booked_loads,
        "failed_negotiations": failed_negotiations,
        "average_final_rate": average_final_rate
    }


@app.get("/calls")
def get_calls():
    rows = get_all_calls()

    return [
        {
            "mc_number": row[0],
            "carrier_name": row[1],
            "load_id": row[2],
            "origin": row[3],
            "destination": row[4],
            "carrier_offer": row[5],
            "final_rate": row[6],
            "outcome": row[7],
            "sentiment": row[8],
            "created_at": row[9]
        }
        for row in rows
    ]