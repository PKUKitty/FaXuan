import itchat


def test_wechat():
    itchat.auto_login()
    itchat.send_msg('Hello, file helper', toUserName='filehelper')


if __name__ == '__main__':
    test_wechat()
