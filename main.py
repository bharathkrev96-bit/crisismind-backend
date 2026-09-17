from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CrisisMind Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

hospitals = [
    {"id": "HA", "name": "Hospital A", "lat": 13.06, "lng": 80.25, "icu_beds": 2, "ward_beds": 12, "beds": 40, "address": "Anna Salai, Chennai"},
    {"id": "HB", "name": "Hospital B", "lat": 13.10, "lng": 80.29, "icu_beds": 5, "ward_beds": 20, "beds": 60, "address": "North Beach Road, Chennai"},
]

shelters = [
    {"id": "SA", "name": "Shelter A", "lat": 13.05, "lng": 80.22, "capacity": 300, "occupied": 270, "type": "Government School", "address": "Kodambakkam, Chennai"},
    {"id": "SB", "name": "Shelter B", "lat": 13.11, "lng": 80.27, "capacity": 500, "occupied": 195, "type": "Community Hall", "address": "Tondiarpet, Chennai"},
]

blocked_roads = ["Road A (Zone 3 - Junction 1)"]

patients = [
    {"id": "P1", "name": "Patient P1", "severity": "critical", "zone": "Zone 3"},
    {"id": "P2", "name": "Patient P2", "severity": "critical", "zone": "Zone 3"},
    {"id": "P3", "name": "Patient P3", "severity": "high", "zone": "Zone 1"},
    {"id": "P4", "name": "Patient P4", "severity": "medium", "zone": "Zone 4"},
    {"id": "P5", "name": "Patient P5", "severity": "low", "zone": "Zone 2"},
]

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


@app.get("/")
def home():
    return {"message": "CrisisMind backend running"}


@app.get("/api/hospitals")
def get_hospitals():
    return hospitals


@app.get("/api/shelters")
def get_shelters():
    return shelters


@app.get("/api/patients")
def get_patients():
    return sorted(patients, key=lambda p: SEVERITY_ORDER.get(p["severity"], 99))


@app.get("/api/agents/medical")
def medical_agent():
    critical = [p for p in patients if p["severity"] == "critical"]
    return {
        "agent": "Medical Agent",
        "finding": f"{len(critical)} critical patients detected in the affected zone.",
        "patients": critical,
    }


@app.get("/api/agents/hospital")
def hospital_agent():
    best = max(hospitals, key=lambda h: h["icu_beds"])
    return {
        "agent": "Hospital Agent",
        "finding": f"{best['name']} selected — {best['icu_beds']} ICU beds available.",
        "selected_hospital": best,
    }


@app.get("/api/agents/shelter")
def shelter_agent():
    result = []
    for s in shelters:
        pct = round(s["occupied"] / s["capacity"] * 100)
        result.append({"name": s["name"], "occupancy_pct": pct})
    return {"agent": "Shelter Agent", "shelters": result}