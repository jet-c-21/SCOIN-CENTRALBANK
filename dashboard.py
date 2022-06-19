import datetime
import json
import threading
import time

from flask import Flask, request
from flask_cors import CORS

from ult.history_helper import HistoryHelper
from ult.real_time_helper import RealTimeHelper
from ult.tools import Tools

REAL_TIME_UPDATE = 0.5

app = Flask(__name__)
CORS(app)

HISTORY = dict()
REAL_TIME = dict()


def real_time_updater():
    global REAL_TIME
    interval = REAL_TIME_UPDATE * 60
    threading.Timer(interval, real_time_updater).start()

    tokens = Tools.get_tokens()
    real_time_helper = RealTimeHelper(tokens)
    REAL_TIME = real_time_helper.fetch()

    print('Real-Time-Update')


def history_updater():
    global HISTORY

    tokens = Tools.get_tokens('history')
    history_helper = HistoryHelper(tokens)
    HISTORY = history_helper.fetch()

    print('First History Update')

    first_run = False

    while not first_run:
        curr_time = Tools.get_curr_time()
        next_time = curr_time + datetime.timedelta(days=1)
        next_time = next_time.replace(hour=0, minute=0, second=0)

        wait_time = (next_time - curr_time).total_seconds()

        time.sleep(wait_time)

        tokens = Tools.get_tokens('history')
        history_helper = HistoryHelper(tokens)
        HISTORY = history_helper.fetch()


@app.route('/data', methods=['GET', 'POST'])
def send_data():
    global REAL_TIME, HISTORY
    if request.method == 'GET':
        data = dict()
        data['sc-real-time'] = REAL_TIME
        data['sc-history'] = HISTORY

        return json.dumps(data)




def server():
    app.debug = False
    app.run(host='0.0.0.0', port=7777)


if __name__ == '__main__':
    threading.Thread(target=history_updater).start()
    threading.Thread(target=real_time_updater).start()
    threading.Thread(target=server).start()
