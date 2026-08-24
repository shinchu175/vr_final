from flask import Flask, render_template, redirect, url_for, request, session

from models import db, User
app = Flask(__name__)
app.secret_key = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# 🎥 VR Videos
videos = {
    "goa": "N6yibD27dok",
    "bali": "6SbH51yN-q8",
    "maldives": "jqq_ZdD5Zwg",
    "newyork": "YM6GTu_RcWM",
    "dubai": "20eGmjRlsmI",
    "london": "KGerjHMa90s",
    "taj": "8HV1JVgqPM0",
    "colosseum": "YgOt1n-ZYc0",
    "greatwall": "Lnj7qaPA2nE",
    "swiss": "xMZxgaslqn8",
    "grandcanon": "t3gur-osvzY",
    "northenlights": "V1JHr9YbpTo"
}
maps = {
    "goa": "https://www.google.com/maps?q=Goa&output=embed",
    "bali": "https://www.google.com/maps?q=Bali&output=embed",
    "maldives": "https://www.google.com/maps?q=Maldives&output=embed",
    "newyork": "https://www.google.com/maps?q=New+York&output=embed",
    "dubai": "https://www.google.com/maps?q=Dubai&output=embed",
    "london": "https://www.google.com/maps?q=London&output=embed",
    "taj": "https://www.google.com/maps?q=Taj+Mahal&output=embed",
    "colosseum": "https://www.google.com/maps?q=Colosseum&output=embed",
    "greatwall": "https://www.google.com/maps?q=Great+Wall+of+China&output=embed",
    "swiss": "https://www.google.com/maps?q=Switzerland&output=embed",
    "grandcanon": "https://www.google.com/maps?q=Grand+Canyon&output=embed",
    "northenlights": "https://www.google.com/maps?q=Norway+Northern+Lights&output=embed"
}


# 🔐 Check login
def is_logged_in():
    return 'user' in session

# 📖 READ USERS


# 🏠 HOME
@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

# 🌍 PLACES
@app.route('/places')
def places():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('places.html', user=session['user'])

# 🥽 VR VIEW
@app.route('/vr/<place>')
def vr_view(place):
    if not is_logged_in():
        return redirect(url_for('login'))

    video = videos.get(place)

    if not video:
        return "<h2>Place not found ❌</h2>"

    return render_template('vr_view.html', video=video, place=place)

@app.route('/map/<place>')
def map_view(place):
    if not is_logged_in():
        return redirect(url_for('login'))

    link = maps.get(place)

    if not link:
        return "<h2>Map not found ❌</h2>"

    return render_template('map.html', link=link, place=place)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        print("New Message:", name, email, message)

        return render_template('contact.html', success="Message sent ✅")

    return render_template('contact.html')   # ✅ correct

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username already exists in SQL
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template(
                'register.html',
                error="User already exists ❌"
            )

        # Create new user
        user = User(
            username=username,
            password=password
        )

        # Save user to database
        db.session.add(user)
        db.session.commit()

        # Login user automatically
        session['user'] = username

        return redirect(url_for('home'))

    return render_template('register.html')

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Find user in SQL database
        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session['user'] = username
            return redirect(url_for('home'))

        return render_template(
            'login.html',
            error="Invalid credentials ❌"
        )

    return render_template('login.html')
# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ▶️ RUN APP
if __name__ == '__main__':
    app.run(debug=True)