# coding=utf-8
import itchat
import time
import requests
import hashlib
from db_Control import *

# 图灵机器人
def get_response(msg, FromUserName):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = '6b01d8138e02440cae31c6c08e12d942'
    # data中有userd才能实现上下文一致的聊天效果。
    hash = hashlib.md5()
    userid = hash.update(FromUserName.encode('utf-8'))
    data = {'key': apikey,
            'info': msg,
            'userid': userid
            }
    try:
        req = requests.post(api_url, data=data).json()
        return req.get('text')
    except:
        return

#适合 个人间聊天
# @itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
# def Tuling_robot(msg):
#     response = get_response(msg['Content'], msg['FromUserName'])
#     itchat.send(response, msg['FromUserName'])

#群聊
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'], isGroupChat=True)
def text_reply(msg):
  if msg['isAt']:
    #如果艾特机器人并且模板正确，则连接数据库查询此条状态
    if '问题描述' in msg['Content'] and '用户姓名' in msg['Content'] and '手机号' in msg['Content']\
            and '身份证号' in msg['Content']:
        details = msg['Content'].split('\n')
        de_name = details[1].split('：')[1]
        de_phone = details[2].split('：')[1]
        de_idno = details[3].split('：')[1]

        stateReslult = queryState(de_name,de_idno)

        if stateReslult == 'WARN':
            itchat.send(u'@%s 您好，未查得[%s%s]的申请信息，请核对姓名和身份证号！'%
                        (msg['ActualNickName'],de_name,de_idno),msg['FromUserName'])
        elif stateReslult == '发送失败':
            itchat.send(u'@%s 您好，用户[%s]发送资方失败，请联系技术支持处理。' %
                        (msg['ActualNickName'],de_name), msg['FromUserName'])
        else:
            itchat.send(u'@%s 您好，查得[%s]用户的申请状态：%s' %
                        (msg['ActualNickName'], de_name, stateReslult), msg['FromUserName'])
    # 否则提示发送正确格式
    else:
        model_1 = "问题描述：\n用户姓名：\n手机号：\n身份证号："
        itchat.send(u'@%s\u2005您好，请按照如下模板回复'%(msg['ActualNickName']), msg['FromUserName'])
        itchat.send(model_1,msg['FromUserName'])

#返回图片，录音，视频
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    fileDir = '%s%s'%(msg['Type'], int(time.time()))
    msg['Text'](fileDir)
    itchat.send('%s received'%msg['Type'], msg['FromUserName'])
    itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', fileDir), msg['FromUserName'])

#自动同意陌生人好友申请
# @itchat.msg_register('Friends')
# def add_friend(msg):
#     itchat.add_friend(**msg['Text'])
#     itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

itchat.auto_login(hotReload=True)
itchat.run()
