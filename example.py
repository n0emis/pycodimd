from pycodimd import CodiMD

cmd = CodiMD('https://md.noemis.me')
#cmd.login('user@example.com','CorrectHorseBatteryStaple')
cmd.load_cookies()
print(cmd.history()[-1]['text'])  # Print Name of latest Note
