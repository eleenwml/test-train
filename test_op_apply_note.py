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
        # 查询差旅申请单
        self.find_apply_note = api_url + '/credit/find_apply_note'
        #审核差旅申请单
        self.op_apply_note = api_url + '/credit/op_apply_note'


    @classmethod
    def tearDownClass(self):
        pass



    def login(self,mobilePhone):
        self.login_pars = {'mobilePhone': mobilePhone, 'loginPsw': 'e10adc3949ba59abbe56e057f20f883e'}
        self.r = requests.post(self.login, self.login_pars)

        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        token = self.r.json()['token']
        return token



    def add_apply_notes(self):
        '''填写差旅申请单'''
        token = self.login('13148862851')
        pars = {'token':token,
                'tripWay': '0',  # 0:机票，1:火车票，2:酒店
                'orgCity': '深圳',
                'arrCity': '海口',
                'depDate': '2019-12-20',
                'orgCityCode': 'SZX',
                'arrCityCode': 'HAK',
                'reason': '项目需要'
                }
        r = requests.post(self.add_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('提交成功', r.json()['msg'])




    def query_apply_note_self(self):
        '''审批人查询差旅申请单'''
        token = self.login('13148862851')
        pars = {'token':token,
                'status': '0' } # 0待审核，1，审核通过，2，审核不通过

        r = requests.post(self.find_apply_note,pars)
        pprint.pprint(r.json())

        return r.json()




    def get_select_apply_note_info(self):
        tripId_ = self.query_apply_note_self()
        tripId = tripId_['data']['tripWayList']['tripId_']

        for i in tripId:
            if int(i['tripId_']) == int(0):
                select_tripId = i
                return select_tripId
            else:
                raise Exception('找不到ID')





    def test_op_apply_note_pass(self):
        '''审核差旅申请单通过'''
        token = self.login('')
        tripId = self.query_apply_note_self()
        Id = tripId['data']['tripWayList']['tripId_']

        pars = {'token':token,
                'noteId':Id,
                'opType':'3'}  #1催单，2撤销，3审核通过，4审核驳回
        r = requests.post(self.op_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])

        #查询该申请单状态
        requests.post(self.find_apply_note,{'status':'3'})
        select_tripId = self.get_select_apply_note_info()

        self.assertEqual(select_tripId,Id)




    def test_op_apply_note_reject(self):
        '''审核差旅申请单驳回'''
        token = self.login('')
        tripId = self.query_apply_note_self()
        Id = tripId['data']['tripWayList']['tripId_']

        pars = {'token':token,
                'noteId':Id,
                'opType':'4'}  #1催单，2撤销，3审核通过，4审核驳回
        r = requests.post(self.op_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])

        # 查询该申请单状态
        requests.post(self.find_apply_note, {'status': '4'})
        select_tripId = self.get_select_apply_note_info()

        self.assertEqual(select_tripId,Id)




    def test_op_apply_note_reminder(self):
        '''申请人催单'''
        token = self.login('13148862851')
        tripId = self.query_apply_note_self()
        Id = tripId['data']['tripWayList']['tripId_']

        pars = {'token':token,
                'noteId':Id,
                'opType':'1'}  #1催单，2撤销，3审核通过，4审核驳回
        r = requests.post(self.op_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])

        # 查询该申请单状态
        requests.post(self.find_apply_note, {'status': '1'})
        select_tripId = self.get_select_apply_note_info()

        self.assertEqual(select_tripId,Id)




    def test_op_apply_note_cancel(self):
        '''申请人撤销'''
        token = self.login('13148862851')
        tripId = self.query_apply_note_self()
        Id = tripId['data']['tripWayList']['tripId_']

        pars = {'token':token,
                'noteId':Id,
                'opType':'2'}  #1催单，2撤销，3审核通过，4审核驳回
        r = requests.post(self.op_apply_note,pars)
        pprint.pprint(r.json())
        self.assertEqual('200', r.status_code)
        self.assertEqual('0', r.json()['ret'])
        self.assertEqual('成功', r.json()['msg'])

        # 查询该申请单状态
        requests.post(self.find_apply_note, {'status': '2'})
        select_tripId = self.get_select_apply_note_info()

        self.assertEqual(select_tripId,Id)





if __name__ == '__main__':
    unittest.main()
