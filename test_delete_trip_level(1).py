#coding=utf-8

import requests
import unittest
import pprint
from hashlib import md5

m = md5()
m.update(b'123456')
encodeStr = m.hexdigest()
print(encodeStr)

class DelectTripLevelCase(unittest.TestCase):

    def setUp(self):
        api_url = 'http://test-api.tianhangbox.net'
        self.login = api_url + '/login/appNewLogin'
        self.login_pars = {'mobilePhone': '18600000469', 'loginPsw':'e10adc3949ba59abbe56e057f20f883e'}
        self.r = requests.post(self.login,self.login_pars)

        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        print(self.token)

        #添加差旅
        self.add_trip_levels = api_url + '/member/center/add_trip_level'
        # 获取本账号所有的差旅标准
        self.get_trip_levels = api_url + '/member/center/get_trip_levels'
        #删除差旅标准
        self.delete_trip_level = api_url + '/member/center/del_trip_level'



    def tearDown(self):
        pass


    def add_trip_level(self):
        levelName1 = '普通差旅标准2'
        pars = {'token':self.token,
                'levelId': '0',
                'levelName': levelName1,
                'approveFlag': '1',
                'approveType': '0',
                'totalCreditAmount': '10000',
                'domeCabin': '经济舱',
                'priceLowestN': '5'}
        r = requests.post(self.add_trip_levels, pars)

        pprint.pprint(r.json())
        return r.json()


    def query_trip_level(self):
        pars = {'token':self.token}
        r = requests.post(self.get_trip_levels, pars)
        levelId = self.add_trip_level()
        for i in levelId:
         if int(i(['levelId']) == 37):
            levelId_ = i
            return int(levelId_)
         else:
            raise Exception('找不到ID')



    def test_delete_trip_level(self):
        Id = self.add_trip_level()
        levelId = Id['data']['levelId']
        pars = {'token':self.token,
                'levelId':levelId}
        # pars = {'token':self.token,
        #         'levelId':'38'}
        r = requests.post(self.delete_trip_level,pars)
        pprint.pprint(r.json())
        self.assertEqual(200,r.status_code)
        self.assertEqual('0',r.json()['ret'])
        self.assertEqual('成功',r.json()['msg'])

        # #遍历是否删除成功
        # levelId = r.json()['data']['levelId']
        # for i in levelId:
        #     if int(i(['levelId']) == 37):
        #         levelId_ = i
        #         return int(levelId_)
        #     else:
        #         raise Exception('找不到ID')


        # requests.post(self.get_trip_levels,{'token':self.token,'levelId':'38'})

        # self.assertEqual(37,levelId)






if __name__ == '__main__':
    unittest.main()