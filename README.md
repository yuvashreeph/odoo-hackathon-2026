# TransitOps — Fleet Management System (Odoo Hackathon 2026)

Shared project skeleton, per the team's Phase 0 architecture agreement.
**Everyone clones this exact structure.** Nobody creates new top-level
folders. This copy has **Member 3's part (Driver + Trip Management)**
already implemented and slotted into the shared layout.

## Folder structure (agreed by the team)

```
TransitOps/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
│
├── database/
│   └── mongo.py
│
├── models/
│   ├── driver.py          ← Member 3
│   ├── trip.py            ← Member 3
│   ├── user.py            (Member 1 — not yet added)
│   ├── vehicle.py         (Member 2 — not yet added)
│   ├── maintenance.py      (Member 2 — not yet added)
│   ├── fuel.py            (Member 4 — not yet added)
│   └── expense.py         (Member 4 — not yet added)
│
├── routes/
│   ├── driver.py          ← Member 3
│   ├── trip.py            ← Member 3
│   ├── auth.py            (Member 1 — not yet added)
│   ├── vehicle.py         (Member 2 — not yet added)
│   ├── maintenance.py      (Member 2 — not yet added)
│   ├── fuel.py            (Member 4 — not yet added)
│   ├── expense.py         (Member 4 — not yet added)
│   └── dashboard.py        (Member 4 — not yet added)
│
├── services/
│   ├── driver_service.py  ← Member 3
│   ├── trip_service.py    ← Member 3
│   ├── auth_service.py     (Member 1 — not yet added)
│   ├── vehicle_service.py  (Member 2 — not yet added)
│   └── dashboard_service.py (Member 4 — not yet added)
│
├── templates/              (Member 4 owns UI, empty for now)
├── static/{css,js,images}  (Member 4 owns UI, empty for now)
│
├── utils/
│   ├── constants.py        shared status enums — import from here, don't redefine
│   ├── response.py         success()/error() JSON helpers
│   ├── validators.py       ObjectId + date helpers
│   └── auth_stub.py        TEMPORARY stand-in for Member 1's real JWT decorator
│
└── sample_requests/         example JSON bodies for Member 3's endpoints
```

## Database schema (agreed by the team)

7 collections total. Field names, types, and status enums below are the
single source of truth — nobody renames or re-cases these.

| Collection | Owner | Key fields |
|---|---|---|
| `users` | Member 1 | name, email, password (hashed), role |
| `vehicles` | Member 2 | registrationNumber (unique), vehicleName, vehicleType, maxLoadCapacity, odometer, acquisitionCost, status, region |
| `drivers` | Member 3 | name, licenseNumber, licenseCategory, licenseExpiry, phone, safetyScore, status |
| `trips` | Member 3 | vehicleId, driverId, source, destination, cargoWeight, plannedDistance, actualDistance, fuelUsed, **revenue**, status, createdAt |
| `maintenance_logs` | Member 2 | vehicleId, maintenanceType, cost, date, status |
| `fuel_logs` | Member 4 | vehicleId, tripId, liters, cost, date |
| `expenses` | Member 4 | vehicleId, expenseType, amount, date |

Status enums (all in `utils/constants.py`):

```
VEHICLE_STATUS     = ["AVAILABLE", "ON_TRIP", "IN_SHOP", "RETIRED"]
DRIVER_STATUS      = ["AVAILABLE", "ON_TRIP", "OFF_DUTY", "SUSPENDED"]
TRIP_STATUS        = ["DRAFT", "DISPATCHED", "COMPLETED", "CANCELLED"]
MAINTENANCE_STATUS = ["ACTIVE", "COMPLETED"]
USER_ROLES         = ["Fleet Manager", "Driver", "Safety Officer", "Financial Analyst"]
EXPENSE_TYPES      = ["Toll", "Repair", "Insurance", "Parking", "Miscellaneous"]
```

### Collection relationships

```
users
   │
vehicles ──────────────┐
   │                    │
maintenance_logs        │
                         │
drivers                  │
   │                     │
   └────── trips ────────┘
              │
         fuel_logs
              │
         expenses
```

### Team responsibilities

| Member | Collections | APIs |
|---|---|---|
| 1 — Auth & Setup | `users` | `POST /register`, `POST /login`, `GET /profile` |
| 2 — Vehicle & Maintenance | `vehicles`, `maintenance_logs` | `GET/POST /vehicles`, `PUT/DELETE /vehicles/<id>`, `POST /maintenance`, `PUT /maintenance/close` |
| **3 — Driver & Trip (this module)** | `drivers`, `trips` | see below |
| 4 — Dashboard, Reports, Fuel & Expenses | `fuel_logs`, `expenses` | `POST/GET /fuel`, `POST/GET /expenses`, `GET /dashboard`, `GET /reports`, `GET /export/csv` |

`models/`, `routes/`, and `services/` for Members 1, 2, and 4 are included
as **stub files** — each one documents exactly which APIs and business
rules that member needs to build, against the shared schema, so nothing
has to be renamed later. Only `driver`/`trip` files are fully implemented.

## My part (Member 3 — Driver & Trip Management)

Implements everything under "Integration Checklist → Member 3" in the
team doc:
- Driver CRUD (`routes/driver.py`, `services/driver_service.py`)
- Trip CRUD + dispatch/complete/cancel workflow
  (`routes/trip.py`, `services/trip_service.py`)
- 8-point dispatch validation
- Business rules enforced (status transitions, capacity checks)

It reads/writes the shared `drivers`, `trips`, and `vehicles` collections
using the field names and status enums the whole team agreed on
(`utils/constants.py`), so it plugs straight into whatever Member 1
(auth) and Member 2 (vehicles) build, with zero renaming.

## Setup

```bash
cd TransitOps
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # edit MONGO_URI if needed
```

You need a local or Atlas MongoDB instance. If testing standalone, seed a
`vehicles` document since trips reference it:

```js
db.vehicles.insertOne({
  registrationNumber: "TN09AB1234",
  vehicleName: "Tata Ace",
  maxLoadCapacity: 1500,
  status: "AVAILABLE"
})
```

## Run

```bash
python app.py
```

Server starts on `http://localhost:5000`.

```bash
curl http://localhost:5000/health
```

## Merging with the team

`utils/auth_stub.py` is a **stub** — it does not check tokens, it just
lets every request through, purely so this module runs standalone.

When Member 1's real auth is ready:
1. Delete `utils/auth_stub.py`.
2. In `routes/driver.py` and `routes/trip.py`, change
   `from utils.auth_stub import token_required`
   to
   `from services.auth_service import token_required`
   (or wherever Member 1 places the real decorator).
3. In `app.py`, keep the blueprint registrations for `drivers_bp` and
   `trips_bp` — just fold them into Member 1's shared `app.py` instead of
   running this one.
4. Nothing in `models/`, `services/driver_service.py`,
   `services/trip_service.py`, or the Mongo field/collection names needs
   to change — they already match the team's shared schema.

## API overview

### Driver endpoints (`/drivers`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/drivers` | List drivers. Supports `?search=` and `?status=` |
| GET | `/drivers/<id>` | Get one driver |
| POST | `/drivers` | Create driver |
| PUT | `/drivers/<id>` | Update driver (partial update) |
| DELETE | `/drivers/<id>` | Delete driver (blocked if `ON_TRIP` or linked to an active trip) |

### Trip endpoints (`/trips`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/trips` | List trips. Supports `?status=` |
| GET | `/trips/<id>` | Get one trip |
| POST | `/trips` | Create trip (always starts as `DRAFT`) |
| PUT | `/trips/<id>` | Update trip (`DRAFT` only) |
| DELETE | `/trips/<id>` | Delete trip (`DRAFT` only) |
| PUT | `/trips/<id>/dispatch` | Run 8-point validation, move to `DISPATCHED` |
| PUT | `/trips/<id>/complete` | Move `DISPATCHED` → `COMPLETED`, free driver/vehicle |
| PUT | `/trips/<id>/cancel` | Cancel a `DRAFT` or `DISPATCHED` trip, free driver/vehicle if it was dispatched |

## Dispatch validation (8-point, in order)

`PUT /trips/<id>/dispatch` runs all 8 checks and returns every failing
check at once as a 422 with an `errors` array:

1. Driver exists
2. Vehicle exists
3. Driver status is `AVAILABLE`
4. Vehicle status is `AVAILABLE`
5. Driver's license is not expired
6. Cargo weight ≤ vehicle `maxLoadCapacity`
7. Driver is not already `ON_TRIP`
8. Vehicle is not already `ON_TRIP`

On success, three documents update together: Trip → `DISPATCHED`,
Driver → `ON_TRIP`, Vehicle → `ON_TRIP`.

## Response shape (team standard)

```json
{ "success": true, "message": "...", "data": { ... } }
```
```json
{ "success": false, "message": "...", "errors": ["...", "..."] }
```

## Git workflow

```bash
git checkout -b trip
git add .
git commit -m "Driver + Trip management module (Member 3)"
git push origin trip
```
