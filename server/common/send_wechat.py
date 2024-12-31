import json
import datetime
import urllib.request


class Weixin:
    def __init__(self, url, corpid, agentid, corpsecret, touser):
        token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
        self.token = json.loads(urllib.request.urlopen(token_url).read().decode())['access_token']
        self.response = None
        self.url = url
        self.touser = touser
        self.agentid = agentid

    def send_message(self, url, data):
        send_url = '%s/cgi-bin/message/send?access_token=%s' % (url, self.token)
        self.response = urllib.request.urlopen(urllib.request.Request(url=send_url, data=data)).read()

    def text_messages(self, subject, message):
        values = {
            "touser": self.touser,
            "msgtype": 'text',
            "agentid": self.agentid,
            "text": {'content': str(subject) + str(message)},
            "safe": 0
        }

        self.send_message(self.url, bytes(json.dumps(values), 'utf-8'))

    def card_messages(self, subject, message, url):
        values = {
            "touser": self.touser,
            "msgtype": 'textcard',
            "agentid": self.agentid,
            "textcard": {
                "title": subject,
                "description": message,
                "url": url,
                "btntxt": "查看全部"
            },
            "safe": 0
        }

        self.send_message(self.url, bytes(json.dumps(values), 'utf-8'))


def send_inform(subject, message, card_url: str = ""):
    touser = "@all"
    # agentid = 1000020
    agentid = 1000021  # TEST
    # corpsecret = "0fJZYwHuz4DVXWp2vnaXRifG2KMXBgSAVHDyTUJ-l9A"
    corpsecret = "br2PlFzK0XUV5Kd1M-qqOhces_MQBSBaKCG5B0BD4e4"  # TEST
    corpid = "wwff1e411ead6e2c20"
    url = "https://qyapi.weixin.qq.com"
    obj = Weixin(url, corpid, agentid, corpsecret, touser)
    if card_url:
        obj.card_messages(subject, message, card_url)
    else:
        obj.text_messages(subject, message)

    print("=== %s ===" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(subject, message)
    print(obj.response)


if __name__ == "__main__":
    msg = """
        ◆ 白班：张某某（13888888888）
        ◆ 夜班：李四（13888888888）
        ◆ 网络：王某某（13888888888）
        ◆ 应用：刘六（13888888888）
        ◆ 安全：七七七（13888888888）
    """

    send_inform("值班通知", msg, "www.baidu.com")
