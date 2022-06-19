# coding: utf-8
import json
import datetime
import requests


class Tools:
    @staticmethod
    def get_curr_time():
        return datetime.datetime.today().replace(microsecond=0).astimezone(
            datetime.timezone(datetime.timedelta(hours=8)))

    @staticmethod
    def get_timestamp(mode='today'):
        curr_time = Tools.get_curr_time()
        if mode == 'today':
            interval_tail = curr_time
            interval_head = curr_time.replace(hour=0, minute=0, second=0)
            start = str(interval_head.timestamp()).split('.')[0]
            end = str(interval_tail.timestamp()).split('.')[0]
            return start, end

        elif mode == 'week':
            interval_tail = curr_time - datetime.timedelta(days=1)
            interval_tail = interval_tail.replace(hour=23, minute=59, second=59)

            interval_head = curr_time - datetime.timedelta(days=1)
            interval_head = interval_head.replace(hour=0, minute=0, second=0) - datetime.timedelta(days=6)

            start = str(interval_head.timestamp()).split('.')[0]
            end = str(interval_tail.timestamp()).split('.')[0]
            return start, end

        elif mode == 'loyalty':
            interval_tail = curr_time
            interval_head = curr_time - datetime.timedelta(days=7)

            start = str(interval_head.timestamp()).split('.')[0]
            end = str(interval_tail.timestamp()).split('.')[0]
            return start, end

    @staticmethod
    def request_server(url):
        res = requests.get(url)
        return json.loads(res.text)

    @staticmethod
    def get_real_time_tokens() -> dict:
        result = dict()
        result['type'] = 'real-time-tokens'

        curr_time = Tools.get_curr_time()

        # Flow token
        start, end = Tools.get_timestamp('today')
        flow_tokens = dict()
        flow_tokens['start'] = start
        flow_tokens['end'] = end
        result['FLOW'] = flow_tokens

        # New User tokens
        new_user_tokens = dict()
        new_user_tokens['start'] = start
        new_user_tokens['end'] = end
        result['NEW_USER'] = new_user_tokens

        # all User tokens
        all_user_tokens = dict()
        all_user_tokens['start'] = 0
        all_user_tokens['end'] = str(curr_time.timestamp()).split('.')[0]
        result['ALL_USER'] = all_user_tokens

        # Loyalty tokens
        start, end = Tools.get_timestamp('loyalty')
        loyalty_tokens = dict()
        loyalty_tokens['start'] = start
        loyalty_tokens['end'] = end
        result['LOYALTY'] = loyalty_tokens

        return result

    @staticmethod
    def get_history_tokens() -> dict:
        result = dict()
        result['type'] = 'history-tokens'

        start, end = Tools.get_timestamp(mode='week')
        flow_tokens = dict()
        flow_tokens['start'] = start
        flow_tokens['end'] = end
        result['FLOW_HIST'] = flow_tokens
        new_user_tokens = dict()
        new_user_tokens['start'] = start
        new_user_tokens['end'] = end
        result['NEW_USER_HIST'] = new_user_tokens

        return result

    @staticmethod
    def get_tokens(mode='real-time'):
        if mode == 'real-time':
            return Tools.get_real_time_tokens()

        elif mode == 'history':
            return Tools.get_history_tokens()
