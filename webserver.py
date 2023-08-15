from settings import *
from flask import Flask, request, render_template
from utils import (
    db_read,
    hours_since_last_feeding,
    open_feeding_lid,
    db_write
)

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')


@app.route("/", methods=['GET'])
def index():
    feeding_timeline = db_read()
    try:
        last_feeding_time = feeding_timeline[0]['time']
    except:
        last_feeding_time = INITIAL_LAST_FEEDING_STRING

    data = {
        'feeding_options': FEEDING_OPTIONS,
        'strict_feeding_hours': FEEDING_INTERVAL_IN_HOURS,
        'feeding_timeline': feeding_timeline,
        'last_feeding_time': last_feeding_time
    }

    return render_template('index.html', **data)


@app.route("/feed", methods=['POST'])
def feed():
    success = True
    error = None
    feeding_type = request.form.get('feeding_type')
    last_feeding = request.form.get('last_feeding')
    strict_feeding = request.form.get('strict_feeding')

    if strict_feeding == 'true' and hours_since_last_feeding(last_feeding) < FEEDING_INTERVAL_IN_HOURS:
        error = f"עוד לא עברו {FEEDING_INTERVAL_IN_HOURS} שעות מאז האכלה אחרונה"
        success = False
    else:
        try:
            open_feeding_lid(feeding_type)
            db_write(feeding_type, request.remote_addr)

        except Exception as e:
            success = False
            error = str(e)

    return {"success": success, "msg": error}
