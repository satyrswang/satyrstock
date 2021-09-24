import time

import itchat



itchat.auto_login(hotReload=True)
# 发送给指定联系人
itchat.send('bbb,', toUserName='filehelper')

# while True:
#     itchat.send('Hello,', toUserName='filehelper')
#     time.sleep(4)
