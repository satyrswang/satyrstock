from subprocess import call
code  = 222
now_price = 0.03
content = str(code) + " HIT " + str(now_price)
cmd = 'display notification \"' + \
    "Notificaton memo" + '\" with title \"'+str(content)+'\"'
call(["osascript", "-e", cmd])
