# -*- coding: utf-8 -*-
# @Time : 2023/6/15 21:19
# @Author : 祝佳祥
# @File : sms_sendmessage.py
# @Software: PyCharm
from ronglian_sms_sdk import SmsSDK

accId = '2c94811c8853194e0188bf0cd4652a0e'
accToken = '9de0e38b27e14e8580e81c5852ccaaba'
appId = '2c94811c8853194e0188bf0cd5ab2a15'

def send_message(mobile, data_code):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    datas = (f'{data_code}', '3')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)
