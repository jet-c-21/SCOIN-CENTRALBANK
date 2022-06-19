# coding: utf-8
import multiprocessing as mp

from ult.tools import Tools


class RealTimeHelper:
    GET_TX_API = 'http://3.87.137.58:8888/get_transactions_by_timestamp?start={}&end={}'
    GET_USER_API = 'http://3.87.137.58:8888/get_users_by_timestamp?start={}&end={}'

    def __init__(self, tokens: dict):
        self.tokens = tokens
        self.data = dict()
        self.data['type'] = 'real-time-data'

    @staticmethod
    def get_flow_data(tokens: dict, result):
        token = tokens['FLOW']
        url = RealTimeHelper.GET_TX_API.format(token['start'], token['end'])
        data = Tools.request_server(url)
        result.append(len(data))

    @staticmethod
    def get_new_user_data(tokens: dict, result):
        token = tokens['NEW_USER']
        url = RealTimeHelper.GET_USER_API.format(token['start'], token['end'])
        data = Tools.request_server(url)
        result.append(len(data))

    @staticmethod
    def get_all_user_data(tokens: dict, result):
        token = tokens['ALL_USER']
        url = RealTimeHelper.GET_USER_API.format(token['start'], token['end'])
        data = Tools.request_server(url)
        result.append(len(data))

    @staticmethod
    def get_loyalty_data(tokens: dict, result):
        record = dict()
        tokens = tokens['LOYALTY']
        start = tokens['start']
        end = tokens['end']

        # get all user count
        url = RealTimeHelper.GET_USER_API.format(0, end)
        all_user = len(Tools.request_server(url))

        # interval data
        url = RealTimeHelper.GET_TX_API.format(start, end)
        data = Tools.request_server(url)
        temp = set()
        for d in data:
            sender = d.get('sender')
            if sender:
                temp.add(sender)

        used = len(temp)
        un_used = all_user - used

        if un_used < 0:
            un_used = 0

        rate = int(round(used / (used + un_used), 2) * 100)

        record['loyalty'] = used
        record['disloyalty'] = un_used
        record['rate'] = rate

        result.append(record)

    def fetch(self):
        # Flow
        flow_result = mp.Manager().list()
        request_flow = mp.Process(target=RealTimeHelper.get_flow_data,
                                  args=(self.tokens, flow_result),
                                  name='REAL_TIME_FLOW')

        # New User
        new_user_result = mp.Manager().list()
        request_new_user = mp.Process(target=RealTimeHelper.get_new_user_data,
                                      args=(self.tokens, new_user_result),
                                      name='REAL_TIME_NEW_USER')

        # All User
        all_user_result = mp.Manager().list()
        request_all_user = mp.Process(target=RealTimeHelper.get_all_user_data,
                                      args=(self.tokens, all_user_result),
                                      name='REAL_TIME_ALL_USER')

        # Loyalty
        loyalty_result = mp.Manager().list()
        request_loyalty = mp.Process(target=RealTimeHelper.get_loyalty_data,
                                     args=(self.tokens, loyalty_result),
                                     name='REAL_TIME_NEW_USER')

        request_flow.start()
        request_new_user.start()
        request_all_user.start()
        request_loyalty.start()

        request_flow.join()
        request_new_user.join()
        request_all_user.join()
        request_loyalty.join()

        self.data['FLOW'] = flow_result[0]
        self.data['NEW_USER'] = new_user_result[0]
        self.data['ALL_USER'] = all_user_result[0]
        self.data['LOYALTY'] = loyalty_result[0]

        return self.data
