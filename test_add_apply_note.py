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
        self.login = api_url + '/login/appNewLogin'
        self.login_pars = {'mobilePhone': '13148862851', 'loginPsw': 'e10adc3949ba59abbe56e057f20f883e'}
        self.r = requests.post(self.login, self.login_pars)

        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        print(self.token)

        #填写差旅申请单
        self.add_apply_note = api_url + '/credit/add_apply_note'


    @classmethod
    def tearDownClass(self):
        pass



    def test_add_apply_note_air(self):
        '''填写机票差旅申请单'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'海口',
                'depDate':'2019-12-20',
                'orgCityCode':'SZX',
                'arrCityCode': 'HAK',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('提交成功',r.json()['msg'])
        # self.assertEqual('0',r.json()['tripWay'])
        # self.assertEqual('深圳', r.json()['orgCity'])
        # self.assertEqual('海口', r.json()['arrCity'])
        # self.assertEqual('2019-12-20', r.json()['depDate'])
        # self.assertEqual('SZX', r.json()['orgCityCode'])
        # self.assertEqual('HAK', r.json()['arrCityCode'])
        # self.assertEqual('项目需要', r.json()['reason'])



    def test_add_apply_note_air_orgcity_null(self):
        '''出发城市为空'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'',
                'arrCity':'海口',
                'depDate':'2019-12-20',
                'orgCityCode':'SZX',
                'arrCityCode': 'HAK',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('请填写出发城市',r.json()['msg'])




    def test_add_apply_note_air_arrcity_null(self):
        '''到达城市为空'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'',
                'depDate':'2019-12-20',
                'orgCityCode':'SZX',
                'arrCityCode': 'HAK',
                'reason':''}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('请填写到达城市',r.json()['msg'])




    def test_add_apply_note_air_depdate_null(self):
        '''出发日期为空'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'海口',
                'depDate':'',
                'orgCityCode':'SZX',
                'arrCityCode': 'HAK',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('请选择出行时间',r.json()['msg'])





    def test_add_apply_note_air_orgcitycode_null(self):
        '''出发城市三字码为空'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'海口',
                'depDate':'2019-12-20',
                'orgCityCode':'',
                'arrCityCode': 'HAK',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('请填写出发城市三字码',r.json()['msg'])




    def test_add_apply_note_air_arrcitycode_null(self):
        '''到达城市三字码为空'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'海口',
                'depDate':'2019-12-20',
                'orgCityCode':'SZX',
                'arrCityCode': '',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('请填写到达城市三字码',r.json()['msg'])





    def test_add_apply_note_air_orgcitycode_wrong(self):
        '''出发城市三字码错误'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'海口',
                'depDate':'2019-12-20',
                'orgCityCode':'AAA',
                'arrCityCode': 'HAK',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('出发城市三字码错误',r.json()['msg'])




    def test_add_apply_note_air_arrcitycode_wrong(self):
        '''到达城市三字码错误'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'海口',
                'depDate':'2019-12-20',
                'orgCityCode':'SZX',
                'arrCityCode': 'AAA',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('到达城市三字码错误',r.json()['msg'])




    def test_add_apply_note_air_same_city(self):
        '''到达城市三字码错误'''
        pars = {'tripWay':'0', #0:机票，1:火车票，2:酒店
                'orgCity':'深圳',
                'arrCity':'深圳',
                'depDate':'2019-12-20',
                'orgCityCode':'SZX',
                'arrCityCode': 'SZX',
                'reason':'项目需要'}
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        self.assertEqual('',r.json()['ret'])
        self.assertEqual('不能选择相同城市',r.json()['msg'])




    # def test_add_apply_note_train(self):
    #     '''填写火车票差旅申请单'''
    #     pars = {'tripWay': '1',  # 0:机票，1:火车票，2:酒店
    #             'orgCity': '深圳',
    #             'arrCity': '广州',
    #             'depDate': '2018-10-20',
    #             'reason': '项目需要'}
    #     r = requests.post(self.add_apply_note, pars)
    #     pprint.pprint(r.json())
    #     self.assertEqual('200', r.status_code)
    #     self.assertEqual('0', r.json()['ret'])
    #     self.assertEqual('提交成功', r.json()['msg'])
    #
    #
    #
    #
    # def test_add_apply_note_train_orgcity_null(self):
    #     '''出发站点为空'''
    #     pars = {'tripWay': '1',  # 0:机票，1:火车票，2:酒店
    #             'orgCity': '深圳',
    #             'arrCity': '广州',
    #             'depDate': '2018-10-20',
    #             'reason': '项目需要'}
    #     r = requests.post(self.add_apply_note, pars)
    #     pprint.pprint(r.json())
    #     self.assertEqual('200', r.status_code)
    #     self.assertEqual('0', r.json()['ret'])
    #     self.assertEqual('请选择出发站点', r.json()['msg'])
    #
    #
    #
    #
    #
    # def test_add_apply_note_train_arrcity_null(self):
    #     '''到达站点为空'''
    #     pars = {'tripWay': '1',  # 0:机票，1:火车票，2:酒店
    #             'orgCity': '深圳',
    #             'arrCity': '',
    #             'depDate': '2018-10-20',
    #             'reason': '项目需要'}
    #     r = requests.post(self.add_apply_note, pars)
    #     pprint.pprint(r.json())
    #     self.assertEqual('200', r.status_code)
    #     self.assertEqual('', r.json()['ret'])
    #     self.assertEqual('请选择到达站点', r.json()['msg'])
    #
    #
    #
    #
    # def test_add_apply_note_train_same_city(self):
    #     '''出发站点和到达站点相同'''
    #     pars = {'tripWay': '1',  # 0:机票，1:火车票，2:酒店
    #             'orgCity': '深圳',
    #             'arrCity': '深圳',
    #             'depDate': '2018-10-20',
    #             'reason': '项目需要'}
    #     r = requests.post(self.add_apply_note, pars)
    #     pprint.pprint(r.json())
    #     self.assertEqual('200', r.status_code)
    #     self.assertEqual('', r.json()['ret'])
    #     self.assertEqual('出发站点和到达站点不能相同', r.json()['msg'])
    #
    #
    #
    #
    # def test_add_apply_note_hotel(self):
    #     '''填写酒店差旅申请'''
    #     pars = {'tripWay': '2',  # 0:机票，1:火车票，2:酒店
    #             'arrCity': '深圳',
    #             'depDate': '2018-12-20',
    #             'leaveDate':'2018-12-21',
    #             'reason': '项目需要'}
    #     r = requests.post(self.add_apply_note, pars)
    #     pprint.pprint(r.json())
    #     self.assertEqual('200', r.status_code)
    #     self.assertEqual('0', r.json()['ret'])
    #     self.assertEqual('提交成功', r.json()['msg'])




if __name__ == '__main__':
    unittest.main()
