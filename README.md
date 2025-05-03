# Green Campus Management System – Prototype

**Purpose (≤200 words)**  
This prototype demonstrates the feasibility of a Green Campus Management System by showcasing three critical functions:
1. **Resource Monitoring** – Track 30‑day electricity & water consumption with automatic anomaly alerts.  
2. **Energy‑Use Analysis** – Detect inefficient usage based on occupancy & schedules.  
3. **Green Transport Advisor** – Recommend eco‑friendly travel modes and offer mock car‑pool matches.

**How to Run**

```bash
# 1. Create venv & install deps
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Run application
export FLASK_APP=green_campus.app:create_app
flask run  # localhost:5000
```

Or open the folder in **PyCharm**, mark it as a Flask project, choose *create_app* as the factory, and click *Run*.

**Tests**

```bash
python -m unittest discover tests
```

**Tech Stack**

* Python 3.11, Flask, Flask‑Login, SQLAlchemy, matplotlib  
* Observer pattern for alerting, inheritance & association between classes  
* SQLite for quick persistence

**Implemented Features**

| Feature | Positive Test | Negative Test |
|---------|---------------|---------------|
| Resource sensors | `test_electric_positive` | `test_electric_negative` |
| Energy analysis  | `test_classroom_alert`   | `test_classroom_no_alert` |
| Transport module | `test_recommend_walk`    | `test_carpool_*` |

**Contributions**

| Member | % | Work Done |
|--------|---|-----------|
| Alice  | 50 | Core Flask app, sensors & tests |
| Bob    | 30 | Transport module, data blueprint |
| Carol  | 20 | Docs, test suite, Git hygiene |
