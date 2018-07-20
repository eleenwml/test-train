#coding=utf-8

import requests
import unittest
import pprint
from hashlib import md5

m = md5()
m.update(b'123456')
encodeStr = m.hexdigest()
print(encodeStr)

class AddTriplevelsCase(unittest.TestCase):

    def setUp(self):
        api_url = 'http://test-api.tianhangbox.net'
        self.login = api_url + '/login/appNewLogin'
        self.login_pars = {'mobilePhone': '18600000469', 'loginPsw':'e10adc3949ba59abbe56e057f20f883e'}
        self.r = requests.post(self.login,self.login_pars)

        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        print(self.token)

        #新增和编辑差旅标准
        self.add_trip_levels = api_url + '/member/center/add_trip_level'

    # @classmethod
    # def setUpClass(self):
    #     api_url = 'http://test-api.tianhangbox.net'
    #     self.login = api_url + '/login/appNewLogin'
    #     self.login_pars = {'mobilePhone': '13148862851', 'loginPsw':'e10adc3949ba59abbe56e057f20f883e'}
    #     self.r = requests.post(self.login,self.login_pars)
    #
    #     login_msg = self.r.json()
    #     # pprint.pprint(self.r.json())
    #     self.token = login_msg['data']['token']
    #     print(self.token)
    #
    #     #新增和编辑差旅标准
    #     self.add_trip_levels = api_url + '/member/center/add_trip_level'
    #
    # @classmethod
    # def tearDownClass(cls):
    #     pass

    def tearDown(self):
        pass



    def test_add_trip_levels_need_approved(self):
        '''需审批人部门'''
        pars = {'token':self.token,
                'levelId':'0', #0:新增，大于0:编辑
                'levelName':'普通差旅标准1',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'0',  #0部门负责人，1企业经办人,2指定人员
                'totalCreditAmount':'10000',
                'domeCabin':'经济舱',
                'priceLowestN':'5'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200,r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual( '成功',r.json()['msg'])
        # self.assertTrue(int(r.json()['levelId']) > int(0))
        # self.assertEqual(r.json()['data']['levelName'],'普通差旅标准1')
        # self.assertEqual(r.json()['data']['approveFlag'],'1')
        # self.assertEqual(r.json()['data']['approveType'],'0')
        # self.assertEqual(r.json()['data']['totalCreditAmount'],'10000')
        # self.assertEqual(r.json()['data']['domeCabin'],'经济舱')
        # self.assertEqual(r.json()['data']['priceLowestN'],'5')


    def test_add_trip_levels_need_approved_type1(self):
        '''审批企业经办人限额为空'''
        pars = {'token':self.token,
                'levelId':'0',  #0:新增，大于0:编辑
                'levelName':'普通差旅标准2',
                'approveFlag':'1',   #0:不需要审核 1:需要审核
                'approveType':'1',   #0部门负责人，1企业经办人,2指定人员
                'totalCreditAmount':'',
                'domeCabin':'头等舱',
                'priceLowestN':'2'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




    def test_add_trip_levels_need_approved_levelName_same(self):
        '''验证相同的差旅标准名称不能添加'''
        pars = {'token':self.token,
                'levelId':'0',  #0:新增，大于0:编辑
                'levelName':'普通差旅标准2',
                'approveFlag':'1',   #0:不需要审核 1:需要审核
                'approveType':'1',   #0部门负责人，1企业经办人,2指定人员
                'totalCreditAmount':'',
                'domeCabin':'头等舱',
                'priceLowestN':'2'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('999999', r.json()['ret'])
        self.assertEqual('已经存在相同的差旅标准名称', r.json()['msg'])



    def test_add_trip_levels_need_approved_type2null(self):
        '''审批企业指定人为空'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准3',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'2',  #0部门负责人，1企业经办人,2指定人员
                'approveId':'',
                'totalCreditAmount':'10000',
                'domeCabin':'不限',
                'priceLowestN':'98'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('请选择指定人', r.json()['msg'])



    def test_add_trip_levels_need_approved_type2(self):
        '''审批企业指定人不为空'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准4',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'2',  #0部门负责人，1企业经办人,2指定人员
                'approveId':'',
                'totalCreditAmount':'10000',
                'domeCabin':'经济舱,头等舱',
                'priceLowestN':'98'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_add_trip_levels_need_approved_type2_forbidden(self):
        '''审批企业指定人为禁用'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准4',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'2',  #0部门负责人，1企业经办人,2指定人员
                'approveId':'',
                'totalCreditAmount':'10000',
                'domeCabin':'经济舱,头等舱',
                'priceLowestN':'98'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('该员工目前已被禁用', r.json()['msg'])



    def test_add_trip_levels_need_approved_type2_notexist(self):
        '''审批企业指定人为不存在'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准4',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'2',  #0部门负责人，1企业经办人,2指定人员
                'approveId':'',
                'totalCreditAmount':'10000',
                'domeCabin':'经济舱,头等舱',
                'priceLowestN':'98'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('无此员工', r.json()['msg'])



    def test_add_trip_levels_need_approved_CreditAmount(self):
        '''审批额度大于总额度'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准5',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'1',
                'totalCreditAmount':'1000000',
                'domeCabin':'经济舱,头等舱,商务舱',
                'priceLowestN':'98'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('授信额度不得大于总额度', r.json()['msg'])




    def test_add_trip_levels_need_approved_more_priceLowestN(self):
        '''审批舱位价格范围超出2位数'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准7',
                'approveFlag':'1',  #0:不需要审核 1:需要审核
                'approveType':'0',
                'totalCreditAmount':'10000',
                'domeCabin':'商务舱,头等舱',
                'priceLowestN':'100'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('舱位价格不得大于99', r.json()['msg'])



    def test_add_trip_levels_need_approved_all_null(self):
        '''需审批全空'''
        pars = {'token':self.token,
                'levelId':'',
                'levelName':'',
                'approveFlag':'',
                'approveType':'',
                'totalCreditAmount':'',
                'domeCabin':'',
                'priceLowestN':''}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('1030', r.json()['ret'])
        self.assertEqual('参数错误', r.json()['msg'])



    def test_add_trip_levels_no_approved_all_null(self):
        '''不审批全空'''
        pars = {'token':self.token,
                'levelId':'',
                'levelName':'',
                'approveFlag':'',
                'rsrvForOther':'',
                'sendFlag':'',
                'sendType':'',
                'sendWho':'',
                'totalCreditAmount':'',
                'domeCabin':'',
                'priceLowestN':''}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('1030', r.json()['ret'])
        self.assertEqual('参数错误', r.json()['msg'])



    def test_add_trip_levels_no_approved(self):
        '''不审批推送部门不可预定限额为空'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准8',
                'approveFlag':'0',   #0:不需要审核 1:需要审核
                'rsrvForOther':'0',  #0：不可预定，1：可预订
                'sendFlag':'1',     #0：不推送，1：推送
                'sendType':'0',     #0:部门负责人，1：企业经办人，2:两者都推送，3：指定人员
                'totalCreditAmount':'',
                'domeCabin':'商务舱',
                'priceLowestN':'1'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])




    def test_add_trip_levels_no_approved_sendtype1(self):
        '''不审批推送企业可预定'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准9',
                'approveFlag':'0',
                'rsrvForOther':'1',
                'sendFlag':'1',
                'sendType':'1',  #0:部门负责人，1：企业经办人，2:两者都推送，3：指定人员
                'sendWho':'',
                'totalCreditAmount':'',
                'domeCabin':'商务舱',
                'priceLowestN':'1'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_add_trip_levels_no_approved_sendtype2(self):
        '''不审批推送两者'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准10',
                'approveFlag':'0',
                'rsrvForOther':'0',
                'sendFlag':'1',
                'sendType':'2',  #0:部门负责人，1：企业经办人，2:两者都推送，3：指定人员
                'totalCreditAmount':'',
                'domeCabin':'商务舱',
                'priceLowestN':'1'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_add_trip_levels_no_approved_sendtype3(self):
        '''不审批推送指定人不为空'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准11',
                'approveFlag':'0',
                'rsrvForOther':'0',
                'sendFlag':'1',
                'sendType':'3', #0:部门负责人，1：企业经办人，2:两者都推送，3：指定人员
                'sendWho':'',
                'totalCreditAmount':'',
                'domeCabin':'不限',
                'priceLowestN':'99'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('请选择指定人员',r.json()['msg'])




    def test_add_trip_levels_no_approved_sendwho_null(self):
        '''不审批推送指定人为空'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准12',
                'approveFlag':'0',
                'rsrvForOther':'0',
                'sendFlag':'1',
                'sendType':'3',  #0:部门负责人，1：企业经办人，2:两者都推送，3：指定人员
                'sendWho':'',
                'totalCreditAmount':'',
                'domeCabin':'经济舱,商务舱',
                'priceLowestN':'10'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('请选择指定人员', r.json()['msg'])



    def test_add_trip_levels_no_approved_ForOther(self):
        '''不审批推送可预定'''
        pars = {'token':self.token,
                'levelId':'0',
                'levelName':'普通差旅标准13',
                'approveFlag':'0',
                'rsrvForOther':'1',
                'sendFlag':'1',
                'sendType':'1',  #0:部门负责人，1：企业经办人，2:两者都推送，3：指定人员
                'totalCreditAmount':'',
                'domeCabin':'头等舱,商务舱',
                'priceLowestN':'10'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])


    def test_add_trip_levels_no_approved_nosend(self):
        '''不审批不推送可预定'''
        pars = {'token':self.token,
                'levelId': '0',
                'levelName': '普通差旅标准14',
                'approveFlag':'0',
                'rsrvForOther':'1',
                'sendFlag':'0',
                'totalCreditAmount':'10000',
                'domeCabin': '经济舱,商务舱',
                'priceLowestN': ''}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])



    def test_add_trip_levels_no_approved_type_CreditAmount(self):
        '''授信额度非整数'''
        pars = {'token':self.token,
                'levelId': '0',
                'levelName': '普通差旅标准15',
                'approveFlag':'0',
                'rsrvForOther':'0',
                'sendFlag':'0',
                'totalCreditAmount':'1000.5',
                'domeCabin': '经济舱,商务舱',
                'priceLowestN': ''}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual( '请输入正整数',r.json()['msg'])


    def test_add_trip_levels_no_approved_more_CreditAmount(self):
        '''授信额度>总额度'''
        pars = {'token':self.token,
                'levelId': '0',
                'levelName': '普通差旅标准16',
                'approveFlag':'0',
                'rsrvForOther':'0',
                'sendFlag':'0',
                'totalCreditAmount':'10000000',
                'domeCabin': '经济舱,商务舱',
                'priceLowestN': ''}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('授信额度不得大于总额度',r.json()['msg'])



    def test_add_trip_levels_no_approved_more_priceLowestN(self):
        '''舱位价格范围超出2字符'''
        pars = {'token':self.token,
                'levelId': '0',
                'levelName': '普通差旅标准17',
                'approveFlag':'0',
                'rsrvForOther':'0',
                'sendFlag':'0',
                'totalCreditAmount':'10000',
                'domeCabin': '经济舱,商务舱',
                'priceLowestN': '100'}
        r = requests.post(self.add_trip_levels, pars)
        pprint.pprint(r.json())
        self.assertEqual(200, r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('舱位价格不得超出2字符',r.json()['msg'])



    # def test_add_trip_levels_no_approved_less_priceLowestN(self):
    #     '''不审批舱位价格范围<1'''
    #     pars = {'token':self.token,
    #             'levelId': '0',
    #             'levelName': '普通差旅标准18',
    #             'approveFlag':'0',
    #             'rsrvForOther':'0',
    #             'sendFlag':'0',
    #             'totalCreditAmount':'10000',
    #             'domeCabin': '经济舱,商务舱',
    #             'priceLowestN': '0'}
    #     r = requests.post(self.add_trip_levels, pars)
    #     pprint.pprint(r.json())
    #     self.assertEqual('200', r.status_code)
    #     self.assertEqual('0',r.json()['ret'])
    #     self.assertEqual('舱位价格不得小于1',r.json()['msg'])




if __name__ == '__main__':
    unittest.main()