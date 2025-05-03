from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .models import db, User
from .data_manager import data_bp
from .transport import TransportService, CarpoolService
from .sensors import AlertManager
import datetime

def create_app():
    app = Flask(__name__, template_folder="../templates")  # 确保模板路径正确
    app.config.update(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///data.db',
    )

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    alerts = []

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def ensure_tables_exist():
        if not hasattr(app, '_tables_created'):
            db.create_all()
            app._tables_created = True

    AlertManager.subscribe(lambda msg: alerts.append({
        'time': datetime.datetime.now(),
        'msg': msg
    }))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form['email']
            uname = request.form['username']
            pw = request.form['password']
            role = request.form['role']
            if User.query.filter_by(email=email).first():
                flash('Email already registered')
            else:
                u = User(email=email, username=uname, role=role)
                u.set_password(pw)
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('login'))
        return render_template_string('''
            <h2>Register</h2>
            <form method=post>
                Email: <input name=email><br>
                Username: <input name=username><br>
                Password: <input name=password type=password><br>
                Role:
                <select name=role><option value=user>User</option><option value=staff>Staff</option></select><br>
                <input type=submit value=Register>
            </form>
        ''')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            u = User.query.filter_by(email=request.form['email']).first()
            if u and u.check_password(request.form['password']):
                login_user(u)
                return redirect(url_for('index'))
            flash('Invalid credentials')
        return render_template_string('''
            <h2>Login</h2>
            <form method=post>
                Email: <input name=email><br>
                Password: <input name=password type=password><br>
                <input type=submit value=Login>
            </form>
            <p>Don't have an account? <a href="/register">Register here</a></p>
        ''')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def index():
        return render_template_string('''
            <h1>Welcome {{ user.username }} ({{ user.role }})</h1>
            <ul>
               <li><a href="/resource-monitor">Resource Monitor</a></li>
               <li><a href="/transport">Green Transport</a></li>
               <li><a href="/alerts">View Alerts</a></li>
               <li><a href="/logout">Logout</a></li>
            </ul>
        ''', user=current_user)

    @app.route('/alerts')
    @login_required
    def view_alerts():
        return render_template_string('''
            <h2>Alerts</h2>
            <ul>
               {% for a in alerts %}
                  <li>{{ a.time }} – {{ a.msg }}</li>
               {% endfor %}
            </ul>
            <a href="/">Back</a>
        ''', alerts=alerts)

    # Register blueprint routes
    app.register_blueprint(data_bp)

    @app.route('/transport', methods=['GET','POST'])
    @login_required
    def transport_route():
        service = TransportService()
        carpool = CarpoolService()

        if request.method == 'POST':
            o = request.form['origin']
            d = request.form['destination']
            times = service.get_times(o, d)

            if times['walk'] < 10:
                rec = 'Walk'
            elif times['bike'] < 20:
                rec = 'Bike'
            else:
                rec = 'Drive'

            carpool_list = []
            if rec == 'Drive' and request.form.get('want_carpool') == 'yes':
                if request.form.get('drive_self') == 'yes':
                    carpool_list = carpool.find_passengers(o, d)
                else:
                    carpool_list = carpool.find_drivers(o, d)

            return render_template("transport_result.html", rec=rec, times=times, carpool_list=carpool_list)

        return render_template("transport.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
