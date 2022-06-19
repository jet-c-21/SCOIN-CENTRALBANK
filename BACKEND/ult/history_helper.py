# coding: utf-8
import multiprocessing as mp
from ult.tools import Tools
import json
import datetime
import pandas as pd


class HistoryHelper:
    GET_TX_API = 'http://3.87.137.58:8888/get_transactions_by_timestamp?start={}&end={}'
    GET_USER_API = 'http://3.87.137.58:8888/get_users_by_timestamp?start={}&end={}'

    def __init__(self, tokens: dict):
        self.tokens = tokens
        self.data = dict()
        self.data['type'] = 'history-data'

    @staticmethod
    def get_flow_data(tokens: dict, result):
        record = dict()
        token = tokens['FLOW_HIST']
        start = token['start']
        end = token['end']

        url = HistoryHelper.GET_TX_API.format(start, end)
        data = Tools.request_server(url)

        start_date = datetime.datetime.fromtimestamp(int(start))
        # end_date = datetime.datetime.fromtimestamp(int(end))

        labels = list()

        date_group = '{}/{}'.format(start_date.month, start_date.day)
        labels.append(date_group)

        # data = json.load(open('D:/TX.json'))  # READ $

        for i in range(1, 7):
            temp_date = start_date + datetime.timedelta(days=i)
            # print(temp_date.timestamp())
            date_group = '{}/{}'.format(temp_date.month, temp_date.day)
            labels.append(date_group)

        df = pd.DataFrame(columns=['sender', 'receiver', 'tx', 'timestamp', 'date'])
        for d in data:
            sender = d.get('sender')
            receiver = d.get('receiver')
            tx = d.get('hash')
            ts = d.get('timestamp')

            date_str = None
            if ts:
                temp_date = datetime.datetime.fromtimestamp(int(ts))
                date_str = '{}/{}'.format(temp_date.month, temp_date.day)

            df.loc[len(df)] = [sender, receiver, tx, ts, date_str]

        date_count = dict(df['date'].value_counts())

        # count val
        val = list()
        for ds in labels:
            if ds in date_count.keys():
                count = int(date_count[ds])
                val.append(count)
            else:
                val.append(0)

        record['labels'] = labels
        record['data'] = val

        result.append(record)

    @staticmethod
    def get_new_user_data(tokens: dict, result):
        record = dict()
        token = tokens['NEW_USER_HIST']
        start = token['start']
        end = token['end']

        url = HistoryHelper.GET_USER_API.format(start, end)
        data = Tools.request_server(url)

        start_date = datetime.datetime.fromtimestamp(int(start))
        # end_date = datetime.datetime.fromtimestamp(int(end))

        labels = list()

        date_group = '{}/{}'.format(start_date.month, start_date.day)
        labels.append(date_group)

        # data = json.load(open('D:/US.json'))  # READ $

        for i in range(1, 7):
            temp_date = start_date + datetime.timedelta(days=i)
            date_group = '{}/{}'.format(temp_date.month, temp_date.day)
            labels.append(date_group)

        df = pd.DataFrame(columns=['username', 'timestamp', 'date'])
        for d in data:
            name = d.get('username')
            ts = d.get('created_at')

            date_str = None
            if ts:
                temp_date = datetime.datetime.fromtimestamp(int(ts))
                date_str = '{}/{}'.format(temp_date.month, temp_date.day)

            df.loc[len(df)] = [name, ts, date_str]

        date_count = dict(df['date'].value_counts())

        # count val
        val = list()
        for ds in labels:
            if ds in date_count.keys():
                count = int(date_count[ds])
                val.append(count)
            else:
                val.append(0)

        record['labels'] = labels
        record['data'] = val

        # print(val)
        result.append(record)

    def fetch(self):
        # Flow
        flow_result = mp.Manager().list()
        request_flow = mp.Process(target=HistoryHelper.get_flow_data,
                                  args=(self.tokens, flow_result),
                                  name='HISTORY_TIME_FLOW')

        # New User
        new_user_result = mp.Manager().list()
        request_new_user = mp.Process(target=HistoryHelper.get_new_user_data,
                                      args=(self.tokens, new_user_result),
                                      name='HISTORY_TIME_NEW_USER')

        request_flow.start()
        request_new_user.start()

        request_flow.join()
        request_new_user.join()

        self.data['FLOW_HIST'] = flow_result[0]
        self.data['NEW_USER_HIST'] = new_user_result[0]

        return self.data
