#coding=utf-8

import requests
import unittest
import pprint
from hashlib import md5

m = md5()
m.update(b'123456')
encodeStr = m.hexdigest()
print(encodeStr)

class ModifyTripLevelCase(unittest.TestCase):

    def setUp(self):
        api_url = 'http://test-api.tianhangbox.net'
        self.login = api_url + '/login/appNewLogin'
        self.login_pars = {'mobilePhone': '18600000469', 'loginPsw':'e10adc3949ba59abbe56e057f20f883e'}
        self.r = requests.post(self.login,self.login_pars)

        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        print(self.token)

        #添加/编辑差旅
        self.add_trip_levels = api_url + '/member/center/add_trip_level'
        # 获取本账号所有的差旅标准
        self.get_trip_levels = api_url + '/member/center/get_trip_levels'


    def tearDown(self):
        pass


    def add_trip_level(self):
        pars = {'token':self.token,
                'levelId': '0',
                'levelName': '普通差旅标准18',
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        return pars['levelName']



    def query_trip_level(self):
        pars = {'token':self.token}
        r = requests.post(self.get_trip_levels,pars)
        pprint.pprint(r.json())
        # Id = r.json()['data']['id']

        return r.json()


    def get_trip_level_info(self):
        Id = self.query_trip_level()
        id1 = Id['data']['id']

        for i in id1:
            if int(i(['id']) == id1):
                tripID = i
                return int(tripID)
            else:
                raise Exception('找不到ID')



    def test_modify_trip_level_name(self):
        tripId = self.query_trip_level()
        level_name_list = list(tripId['data'])

        for level_data in level_name_list:
            data_name = level_data['levelName']
            # add_level_name = self.add_trip_level()
            if data_name == 'VIP差旅标准':
                self.level_data = level_data
                break
            else:
                raise Exception('找不到该数据')

        pars = {'token':self.token,
                'levelId': self.level_data['id'],
                'levelName': 'VIP差旅标准',
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])
        # self.assertEqual(Id,r.json()['levelId'])
        # self.assertEqual('VIP差旅标准', r.json()['levelName'])
        # self.assertEqual('1', r.json()['approveFlag'])
        # self.assertEqual('0', r.json()['approveType'])
        # self.assertEqual('10000', r.json()['totalCreditAmount'])
        # self.assertEqual('经济舱', r.json()['domeCabin'])
        # self.assertEqual('5', r.json()['priceLowestN'])




    def test_modify_trip_level_approve(self):
        '''需审批改为不审批'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId':'17',
                'levelName':'普通差旅标准1',
                'approveFlag':'0',  #0:不需要审核 1:需要审核
                'rsrvForOther':'0',
                'sendFlag':'1',
                'sendType':'0',
                'sendWho':'',
                'totalCreditAmount':'10000',
                'domeCabin':'经济舱',
                'priceLowestN':'5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_modify_trip_level_type(self):
        '''修改审批人为企业经办人'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': 'VIP差旅标准',
                'approveFlag': '1',
                'approveType': '1',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200,r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




    def test_modify_trip_level_type2(self):
        '''修改审批人为指定人员'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': 'VIP差旅标准1',
                'approveFlag': '1',
                'approveType': '2',
                'approveId':'',
                'totalCreditAmount': '10000',
                'domeCabin': '头等舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_modify_trip_level_type2_null(self):
        '''修改审批人为指定人员为空'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': 'VIP差旅标准1',
                'approveFlag': '1',
                'approveType': '2',
                'approveId':'',
                'totalCreditAmount': '10000',
                'domeCabin': '头等舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('999999', r.json()['ret'])
        self.assertEqual('请选择指定人员审核', r.json()['msg'])



    def test_modify_trip_level_totalCreditAmount(self):
        '''修改每月限额'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': 'VIP差旅标准3',
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '20000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




    def test_modify_trip_level_totalCreditAmount_morethan(self):
        '''修改每月限额大于授信总额'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': 'VIP差旅标准',
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '2000000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('授信额度不得大于总额度', r.json()['msg'])


    def test_modify_trip_level_domeCabin(self):
        '''修改舱位'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': '普通差旅标准1',
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '头等舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




    def test_modify_trip_level_priceLowestN(self):
        '''修改舱位价格范围'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': '普通差旅标准1',
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '12'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_modify_trip_level_send(self):
        '''修改不审批不推送可预订'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': '普通差旅标准1',
                'approveFlag':'1',
                'rsrvForOther':'1',
                'sendFlag':'0',
                'totalCreditAmount':'10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_modify_trip_level_ForOther(self):
        '''修改不审批不推送不可预订'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': '普通差旅标准1',
                'approveFlag': '1',
                'rsrvForOther': '0',
                'sendFlag': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




    def test_modify_trip_level_wrong(self):
        '''修改无该字段却传该值'''
        # Id = self.add_trip_level()
        pars = {'token':self.token,
                'levelId': '17',
                'levelName': '普通差旅标准1',
                'approveFlag': '1',
                'approveType': '2',
                'rsrvForOther': '0',
                'sendFlag': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('999999', r.json()['ret'])
        self.assertEqual('请选择指定人员审核', r.json()['msg'])





if __name__ == '__main__':
    unittest.main()