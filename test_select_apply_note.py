#coding=utf-8

import requests
import unittest
import pprint
from hashlib import md5

m = md5()
m.update(b'123456')
encodeStr = m.hexdigest()
print(encodeStr)

class AddApplyNoteCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        api_url = 'http://test-api.tianhangbox.net'
        self.login_url = api_url + '/login/appNewLogin'


        #填写差旅申请单
        self.add_apply_note = api_url + '/credit/add_apply_note'

        #查询差旅申请单
        self.find_apply_note = api_url + '/credit/find_apply_note'


    @classmethod
    def tearDownClass(self):
        pass


    def login(self,mobilePhone):
        login_pars = {'mobilePhone':mobilePhone, 'loginPsw': 'e10adc3949ba59abbe56e057f20f883e'}
        r = requests.post(self.login_url,login_pars)
        login_msg = r.json()
        self.token = login_msg['data']['token']
        token = r.json()['token']
        return token



    def test_query_apply_notes_self(self):
        '''查看个人差旅申请单'''
        token = self.login('13148862851')
        pars = {'token':token,
                'tripWay': '0',  # 0:机票，1:火车票，2:酒店
                'orgCity': '深圳',
                'arrCity': '海口',
                'depDate': '2019-12-20',
                'orgCityCode': 'SZX',
                'arrCityCode': 'HAK',
                'reason': '项目需要'}
        r = requests.post(self.add_apply_note, pars)
        pprint.pprint(r.json())

        list_first_data_tripway = r.json()['data'][0]['tripWayList']['tripWay']

        self.assertEqual(self.get_air_apply_trip(),list_first_data_tripway)




    def test_query_apply_note_other(self):
        '''审批人查询差旅申请单'''
        token = self.login('')
        pars = {'token':token,
                'status': '0' } # 0待审核，1，审核通过，2，审核不通过

        r = requests.post(self.find_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])
        self.assertEqual('待审核', r.json()['data']['statusStr'])




    def get_air_apply_trip(self):
        trip_way = self.select_apply_note()

        for i in trip_way:
            if int(i['tripWay']) == int(0):
                air_apply = i
                return air_apply
            else:
                raise Exception('找不到出行方式')




    def select_apply_note(self):
        pars = {}
        r = requests.post(self.find_apply_note,pars)
        pprint.pprint(r.json())

        self.assertEqual('200',r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功',r.json()['msg'])

        data = r.json()['data'][0]
        # self.assertEqual('0',r.json()['data']['status'])
        # self.assertEqual('项目需要',r.json()['data']['reason'])

        return data['tripWayList']






if __name__ == '__main__':
    unittest.main()
