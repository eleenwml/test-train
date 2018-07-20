#coding:utf8

import requests
from hashlib import md5
import unittest
import pprint

m = md5()
m.update(b'123456')
print(m.update(b'e10adc3949ba59abbe56e057f20f883e'))


class LoginCase(unittest.TestCase):

    def setUp(self):
        api_url = 'http://test-api.tianhangbox.net'

        # api_url = 'http://yufabu-api.tianhangbox.com'
        # api_url = 'http://api.tianhangbox.com'

        self.login = api_url + '/login/appNewLogin'
        self.login_pars = {'mobilePhone': '18600000469', 'loginPsw': 'e10adc3949ba59abbe56e057f20f883e'}

        self.r = requests.post(self.login, self.login_pars)
        login_msg = self.r.json()
        # pprint.pprint(self.r.json())
        self.token = login_msg['data']['token']
        print(self.token)

        self.add_credit_employee = api_url + '/member/center/addemployee'
        self.query_credit_employee = api_url + '/member/center/getemployee'

    def tearDown(self):
        pass

    def test_add_credit_employee_charge(self):
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13286998500',
                'employeeNo': '001',
                'employeeLevel': '1', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('成功',msg)
        self.assertEqual('0',ret)
        # self.assertTrue( int(datas['employeeId']) > int(0))
        # self.assertEqual(pars['deptId'],datas['deptId'])
        # self.assertEqual('DENG',datas['englishName'])
        # self.assertEqual('JIAJIE','givenName')
        # self.assertEqual('13286993500',datas['mobilePhone'])
        # self.assertEqual('001',datas['employeeNo'])
        # self.assertEqual('1',datas['employeeLevel'])
        # self.assertEqual('','levelId_')

    def test_add_credit_employee(self):
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('成功',msg)
        self.assertEqual('0',ret)

    def test_add_credit_employee_lack_mobilePhone(self):
        '''电话号码为空'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('电话号码不能为空',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_lack_realName(self):
        '''缺少真实姓名'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('请输入真实姓名',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_lack_englishName(self):
        '''英文姓名填写不完整'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('英文姓名填写不完整',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_lack_givenName(self):
        '''英文姓名填写不完整'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('英文姓名填写不完整',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_lack_employeeNo(self):
        '''缺少员工编号'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('成功',msg)
        self.assertEqual('0',ret)

    def test_add_credit_employee_lack_employeeLevel(self):
        '''缺少员工等级'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('请选择员工等级',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_lack_status(self):
        '''缺少账号状态'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('缺少账号状态',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_lack_levelId_(self):
        '''缺少模板信息'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('缺少模板信息',msg)
        self.assertEqual('999999',ret)

    def test_add_credit_employee_mobilePhone_1328699350(self):
        '''验证电话号码低于11位不能绑定成功'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('电话号码位数不正确',msg)
        self.assertEqual('999999',ret)



    def test_add_credit_employee_mobilePhone_wrong(self):
        '''验证无效电话号码不能绑定成功'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '12345678901',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('请填写有效手机号码',msg)
        self.assertEqual('999999',ret)


    def test_add_credit_employee_mobilePhone_exist(self):
        '''验证已关联的电话号码不能绑定成功'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('请填写有效手机号码',msg)
        self.assertEqual('999999',ret)


    def test_add_credit_employee_realname_length4(self):
        '''验证已关联的电话号码不能绑定成功'''
        pars = {'token': self.token,
                'employeeId': int('0'),
                'deptId': int('261'),
                'realName': '邓嘉杰',
                'englishName': 'DENG',
                'givenName': 'JIAJIE',
                'mobilePhone': '13289993500',
                'employeeNo': '001',
                'employeeLevel': '0', # 0是普通员工，1是主管
                'status':'1',  # 0禁用 1启用
                #需要去数据库找或者新生成一个
                'levelId_':''
                }
        r = requests.post(self.add_credit_employee, pars)
        pprint.pprint(r.json())
        self.assertEqual('200',r.status_code)
        msg = r.json['msg']
        ret = r.json['ret']
        self.assertEqual('请填写有效手机号码',msg)
        self.assertEqual('999999',ret)


