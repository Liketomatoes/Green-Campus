"""Resource monitoring blueprint"""
import io, random, datetime
import matplotlib
matplotlib.use('Agg')  # headless
import matplotlib.pyplot as plt
from flask import Blueprint, send_file
from flask_login import login_required
from .sensors import ElectricSensor, WaterSensor

data_bp = Blueprint('data', __name__)

# In‑memory storage
DATA_STORE = []

def generate_random_data():
    """Generate 30 days of random electricity & water data"""
    global DATA_STORE
    DATA_STORE.clear()
    base = datetime.date.today() - datetime.timedelta(days=29)
    for i in range(30):
        day = base + datetime.timedelta(days=i)
        DATA_STORE.append({
            'date': day,
            'electric': random.randint(800, 1200),
            'water': random.randint(300, 600)
        })
    return DATA_STORE

@data_bp.route('/resource-monitor')
@login_required
def resource_monitor():
    data = generate_random_data()
    dates = [d['date'] for d in data]
    elec = [d['electric'] for d in data]
    water = [d['water'] for d in data]

    fig, ax = plt.subplots()
    ax.plot(dates, elec, label='Electricity (kWh)')
    ax.plot(dates, water, label='Water (m³)')

    for d in data:
        if d['electric'] > ElectricSensor.threshold:
            ax.plot(d['date'], d['electric'], 'ro')
        if d['water'] > WaterSensor.threshold:
            ax.plot(d['date'], d['water'], 'bo')

    ax.legend()
    ax.set_title('30‑Day Resource Consumption')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
