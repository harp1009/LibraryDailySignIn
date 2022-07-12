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

        data = {
            "subLibId": subLibId,
            "scheduleId": schedule_id,
            "children": 0,
            "card": card,
            "cardType": "IDCARD",
            "name": name,
            "phone": phone,
            "childrenConfig": True,
            "code": ""
        }

        json_data = json.dumps(data)
        base_url = "https://appointment-users.dataesb.com"
        url = "/api/appointment/pub_add/"

        param = {
            'timestamp': timestamp,
            'callback': "#/index/114?counter=1657584000000"
        }

        try:
            for i in range(2):
                when = ""
                if i == 0:
                    when = "上午"
                else:
                    when = "下午"

                schedule_id += i
                parsed_data = json.loads(json_data)
                response_data = requests.post(base_url + url, params=param, json=parsed_data, headers=header)
                state = json.loads(response_data.text)['success']
                print(response_data.text)
                if state == True:
                    print("True")
                    self.sign_in_status += when + "预约成功！" + '\n'
                else:
                    print("False")
                    self.sign_in_status += when + "预约失败！"
        except Exception as e:
            print(e)

    def get_schedule_id(self):
        now = datetime.datetime.now()

        # 用服务端给予的scheduleId进行申请 在2022.7.12上午9点时是1436463 每过一个时间段递增
        # 可以提前预约三天 每天两个时间段 算出三天后的scheduleId
        schedule_id_of_2022_7_12_morning = 1436463
        d1 = datetime.datetime.strptime((now + datetime.timedelta(days=3)).strftime("%Y-%m-%d"), '%Y-%m-%d')
        d2 = datetime.datetime.strptime('2022-7-12', '%Y-%m-%d')
        time_delta = d1 - d2
        schedule_id = time_delta.days * 2 + schedule_id_of_2022_7_12_morning
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

if send_email:
    daily_sign_in.sign_in()
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
