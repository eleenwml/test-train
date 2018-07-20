#coding=utf-8

import requests
import unittest
import pprint
from hashlib import md5

m = md5()
m.update(b'123456')
encodeStr = m.hexdigest()
print(encodeStr)
#print(m.update(b'e10adc3949ba59abbe56e057f20f883e'))

class SelectCreditemployeeCase(unittest.TestCase):

    def setUp(self):
        api_url = 'http://test-api.tianhangbox.net'
        self.login = api_url + '/login/appNewLogin'
        self.login_pars = {'mobilePhone': '18600000469', 'loginPsw':'e10adc3949ba59abbe56e057f20f883e'}
        self.r = requests.post(self.login,self.login_pars)

        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        print(self.token)

        #查询授信子会员
        self.select_creditemployee = api_url + '/credit/appcreditemployee'
        #获取本账号所有的差旅标准
        self.get_trip_levels = api_url + '/member/center/get_trip_levels'



    def tearDown(self):
        pass



    # @unittest.skip
    def test_get_select_creditemployee(self):
        pars = {'token':self.token,
                'kwyword':'',
                'status':'',
                'deptId':''}
        r = requests.post(self.select_creditemployee,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])


    def test_get_trip_levels(self):
        pars = {'token':self.token}
        r = requests.post(self.get_trip_levels,pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




if __name__ == '__main__':
    unittest.main()