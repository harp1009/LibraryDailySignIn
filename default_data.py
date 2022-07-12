# fiddler抓包后找到/api/appointment/pub_add/路径上的POST请求
# header改成自己抓包得到的请求中的header
# header少了某一项服务器会报200 我也不知道是哪一项引起的 所以干脆全写上去了（
header = {
    "unionid": "oF-BrwC3vYqPMqzW7ipvwBqr35As",
    'Host': "appointment-backend-cdn.dataesb.com",
    'Connection': "keep-alive",
    'Content-Length': "173",
    'Accept': "application/json, text/plain, */*",
    'Accept-Language': "zh-CN",
    'unionid': "oF-BrwC3vYqPMqzW7ipvwBqr35As",
    'User-Agent': "Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/7436 MicroMessenger/8.0.15.2020(0x28000F3D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    'Content-Type': "application/json;charset=UTF-8",
    'Origin': "https://appointment-users.dataesb.com",
    'X-Requested-With': "com.tencent.mm",
    'Sec-Fetch-Site': "same-site",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Dest': "empty",
    'Referer': "https://appointment-users.dataesb.com/",
    'Accept-Encoding': "gzip, deflate"
}
# 图书馆ID 宜春市图书馆是114
subLibId = "114"
# 身份证号
card = ""
# 姓名
name = ""
# 手机
phone = ""

# 是否需要打开邮箱提醒？不需要的话以下选项不填
send_email = False
# 发信人邮箱
mail_sender = ""
# QQ邮箱授权码 需要自行申请
mail_auth_code = ""
# 收件人邮箱
mail_receiver = [""]
# smtp地址
mail_smtp_link = "smtp.qq.com"
# smtp端口
mail_smtp_port = 465
