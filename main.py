import requests
import smtplib
from email.mime.text import MIMEText
import time
import datetime
import json
from default_data import *

class DailySignIn:
    # 预约情况
    sign_in_status = ""
    # 请求路径
    base_url = "https://appointment-users.dataesb.com"

    def sign_in(self):
        # 当前时间戳 毫秒级
        now = time.time()
        timestamp = str((int(round(now * 1000))))
        schedule_id = self.get_schedule_id()
        if len(schedule_id) == 0:
            return

        url = "/api/appointment/pub_add/"
        param = {
            'timestamp': timestamp,
            'callback': "#/index/114?counter=1657584000000"
        }

        try:
            for i in range(2):
                data = {
                    "subLibId": "114",
                    "scheduleId": schedule_id[i],
                    "children": 0,
                    "card": card,
                    "cardType": "IDCARD",
                    "name": name,
                    "phone": phone,
                    "childrenConfig": True,
                    "code": ""
                }
                json_data = json.dumps(data)

                when = ""
                if i == 0:
                    when = "上午"
                else:
                    when = "下午"

                response_data = requests.post(self.base_url+url, params=param, json=data, headers=apply_header)
                state = json.loads(response_data.text)['success']
                print(response_data.text)
                if state == True:
                    self.sign_in_status += when + "预约成功！"
                else:
                    self.sign_in_status += when + "预约失败！"
        except Exception as e:
            print(e)

    def get_schedule_id(self):
        now = time.time()
        timestamp = str((int(round(now * 1000))))
        schedule_id = []
        # 所预约的日期
        apply_date = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        url = "/api/appointment/schedule/"
        param = {
            'timestamp': timestamp,
            'callback': "#/index/114?counter=1657670400000",
            'subLibId': "114"
        }
        response_data = requests.get(self.base_url+url, headers=get_schedule_header, params=param)
        schedule = json.loads(response_data.text)['data']
        for item in schedule:
            date = str(item['startTime'])[0:10]
            if date == apply_date:
                schedule_id.append(item['id'])

        return schedule_id


class ErrorEmail():
    def __init__(self, msg_from, pass_word, msg_to):
        '''
        发送邮件实体类
        :param msg_from: # 发送方邮箱
        :param pass_word: # 填入发送方邮箱的授权码
        :param msg_to: # 收件人邮箱
        '''
        self.msg_from = msg_from
        self.pass_word = pass_word
        self.msg_to = msg_to

    def theme_content(self, theme, content):
        '''
        构建邮件主题和内容
        :param theme:  主题
        :param content:  内容
        :return:
        '''
        msg = MIMEText(content)
        msg['Subject'] = theme
        msg['From'] = self.msg_from  # join 作用群发邮件
        msg['To'] = ''.join(self.msg_to)
        return msg

    def send_message(self, host, port, msg):
        '''
        发送邮件方法
        :param host: 第三方邮件host
        :param port:端口号
        :param msg:MIMETexe 对象
        :return:
        '''
        try:
            sm = smtplib.SMTP_SSL(host, port)
            sm.login(self.msg_from, self.pass_word)
            sm.sendmail(self.msg_from, self.msg_to, msg.as_string())
        except Exception as e:
            print(e)
        finally:
            sm.quit()


daily_sign_in = DailySignIn()
daily_sign_in.sign_in()

# 如果星期一闭馆没有预约到的时候status为空 不发送邮件
if send_email and len(daily_sign_in.sign_in_status) != 0:
    date = datetime.datetime.now()
    title = "图书馆预约通知：{}".format(date.strftime("%Y-%m-%d %H:%M"))
    text = """
            *** 图书馆预约通知 ***
            预约时间：{}
            所预约时间：{}
            预约情况：{}
            """.format(date.strftime("%Y-%m-%d %H:%M"), (date + datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
                       daily_sign_in.sign_in_status)

    ee = ErrorEmail(mail_sender, mail_auth_code, mail_receiver)
    msg = ee.theme_content(title, text)
    ee.send_message(mail_smtp_link, mail_smtp_port, msg)