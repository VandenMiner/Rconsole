main.py
Совместный доступ
Без общего доступа
Свойства системы
Тип
Текст
Размер
8 КБ
Занимает
8 КБ
Расположение
KvProject
Владелец
я
Изменено
2 июн. 2021 г. (я)
Открыто
08:14 (я)
Создано
2 июн. 2021 г. (Google Drive Web)
Добавить описание
Читателям разрешено скачивать файл
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.theming import ThemeManager

from kivy.config import Config

from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList

from kivy.storage.jsonstore import JsonStore

from mcrcon import MCRcon

#-------------------------------------------#
Config.set('graphics', 'width', '450')#	 |
Config.set('graphics', 'height', '700')#	|
Config.write()#							 |
#--------------------#----------------------#
sm = ScreenManager()#|
#--------------------#

autofill = JsonStore('autofill.json')

coloralias = [chr(167)+"1",chr(167)+"2",chr(167)+"3",chr(167)+"4",chr(167)+"5",chr(167)+"6",chr(167)+"7",chr(167)+"8",
			 chr(167)+"9",chr(167)+"r",chr(167)+"l",chr(167)+"a",chr(167)+"c",chr(167)+"e",chr(167)+"b",chr(167)+"d",
			 chr(167)+"f",chr(167)+"o",chr(167)+"n",chr(167)+"m",chr(167)+"k"]

rcon_ip = None
rcon_port = None
rcon_pass =  None

moderation_selectedplayer = None
moderation_selectedoption = None
moderation_selectedduration = None
moderation_selectreason = None

coreprotect_u = None
coreprotect_t = None
coreprotect_r = None
coreprotect_a = None
coreprotect_b = None
coreprotect_e = None

class Rconsole(Screen):
	def coreprotect_selectplayer(self, player):
		global coreprotect_u
		coreprotect_u = player
		self.w_coreprotect_mainscreenmanager.current = 'SelectOptions'
	def coreprotect_refreshplayerlist(self):
		with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
			resp = mcr.command("rconsoleplayerlist")
			resp = resp.split()
			listofplayers = MDList()
			for i in resp:
				print(i)
				listofplayers.add_widget(
					OneLineListItem(text=f"{i}",
					secondary_text_color=(1,1,1,.09),
					bg_color=(.176, .184, .212,1),
					on_release=lambda event: self.coreprotect_selectplayer(i)
					))
				try:
					self.w_coreprotect_playerlist.remove_widget(listofplayers)
				except:
					print(1)
				try:
					self.w_coreprotect_playerlist.add_widget(listofplayers)
				except:
					print(2)

	def coreprotect_getcurrentstats(self):
		self.w_selectedcoreprotect_u.text = "Selected blocks: " + str(coreprotect_u)
		self.w_selectedcoreprotect_t.text = "Selected blocks: " + str(coreprotect_t)
		self.w_selectedcoreprotect_r.text = "Selected blocks: " + str(coreprotect_r)
		self.w_selectedcoreprotect_a.text = "Selected blocks: " + str(coreprotect_a)
		self.w_selectedcoreprotect_b.text = "Selected blocks: " + str(coreprotect_b)
		self.w_selectedcoreprotect_e.text = "Selected blocks: " + str(coreprotect_e)



	def moderation_reset(self):
		self.w_moderation.current = "Players"
		moderation_selectedplayer = None
		moderation_selectedoption = None
		moderation_selectedduration = None
		moderation_selectreason = None
	def moderation_selectduration(self):
		global rcon_ip
		global rcon_port
		global rcon_pass	
		try:
			int(self.w_duration.text)
			with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
				resp = mcr.command(f"{moderation_selectedoption} {moderation_selectedplayer} {self.w_duration.text}m {moderation_selectreason}")
				for i in coloralias:
					print(i)
					print(resp)
					resp = resp.replace(i, "")
				self.w_console.text += resp
				self.w_mainnavigation.switch_tab('consoletab')
		except:
			MDDialog(title="Error!", text="Duration mus be an int!").open()

	def moderation_selectreason(self):
		global moderation_selectreason
		global moderation_selectedoption
		moderation_selectreason = self.w_reason.text
		if moderation_selectedoption == "warn":
			global rcon_ip
			global rcon_port
			global rcon_pass	
			with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
				resp = mcr.command(f"warn {moderation_selectedplayer} {moderation_selectreason}")
				for i in coloralias:
					print(i)
					print(resp)
					resp = resp.replace(i, "")
				self.w_console.text += resp
				self.w_mainnavigation.switch_tab('consoletab')
		else:
			self.w_moderation.current = "Duration"

	def moderation_selectoprtion(self, option):
		print(option)
		global moderation_selectedoption
		if option == "ban":
			self.w_moderation.current = "Reason"
			moderation_selectedoption = "tempban"
		if option == "warn":
			self.w_moderation.current = "Reason"
			moderation_selectedoption = "warn"
		if option == "mute":
			self.w_moderation.current = "Reason"
			moderation_selectedoption = "mute"

	def moderation_selectplayer(self, player):
		global moderation_selectedplayer
		moderation_selectedplayer = player
		print(moderation_selectedplayer)
		self.w_moderation.current = "Options"

	def moderation_refreshplayerlist(self):
		global rcon_ip
		global rcon_port
		global rcon_pass	
		with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
			resp = mcr.command("rconsoledeps:rconsoledepsplayerlist")
			resp = resp.split()
			listofplayers = MDList()
			for i in resp:
				listofplayers.add_widget(
					OneLineListItem(text=f"{i}",
					secondary_text_color=(1,1,1,.09),
					bg_color=(.176, .184, .212,1),
					on_release=lambda event: self.moderation_selectplayer(i)
					))
				try:
					self.w_playerlistscreen.remove_widget(listofplayers)
				except:
					pass
				try:
					self.w_playerlistscreen.add_widget(listofplayers)
				except:
					pass



	def refreshchat(self):
		global rcon_ip
		global rcon_port
		global rcon_pass		
		with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
			resp = mcr.command("rconsoledeps:rconsoledepschathisyory")
			
			
			for i in coloralias:
				print(i)
				print(resp)
				resp = resp.replace(i, "")

			self.w_chat.text=resp



	def sendcommand(self, command):
		global rcon_ip
		global rcon_port
		global rcon_pass		
		with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
			resp = mcr.command(command)
			for i in coloralias:
				print(i)
				print(resp)
				resp = resp.replace(i, "")
			self.w_console.text += f"{resp}"
		self.w_commandinput.text = ""

	def appendtocommand(self, text):
		Snackbar(text=f'Succesful added "{text}" to console line!').open()
		if self.w_commandinput.text == "":
			self.w_commandinput.text+=text
		else:
			self.w_commandinput.text+=f" {text}"

class Login(Screen):
	def readytologin(self):
		global rcon_ip
		global rcon_port
		global rcon_pass
		checkcount = 0
		ints = [1,2,3,4,5,6,7,8,9,0]
		if self.w_rcon_ip.text == "":
			self.w_rcon_ip.text = "-"
			checkcount = 0
			Snackbar(text="[Error] Empty ip").open()
		else:
			rcon_ip = self.w_rcon_ip.text
			checkcount += 1
		if self.w_rcon_port.text == "":
			checkcount = 0
			Snackbar(text="[Error] Empty port").open()
			self.w_rcon_port.text = "-"
		else:
			rcon_port = self.w_rcon_port.text
			checkcount += 1
		if self.w_rcon_pass.text == "":
			checkcount = 0
			Snackbar(text="[Error] Empty password").open()
			self.w_rcon_pass.text = "-"
		try:
			rcon_port = int(self.w_rcon_port.text)
			checkcount += 1
		except:
			checkcount = 0
			Snackbar(text=f'[Error] Rcon not int').open()
			self.w_rcon_port.text = "Must be a int!"
		else:
			rcon_pass = self.w_rcon_pass.text
			checkcount += 1
		try:
			with MCRcon(host=rcon_ip, port=int(rcon_port), password=rcon_pass) as mcr:
				resp = mcr.command('connectiontorcontest')
			checkcount += 1
		except:
			Snackbar(text="[Error] Can't connect to server").open()
			checkcount = 0
		if checkcount == 5:
			autofill.put('ip', value=rcon_ip)
			autofill.put('port', value=str(rcon_port))
			autofill.put('pass', value=rcon_pass)
			sm.switch_to(Rconsole())
	def autofillfields(self):
		self.w_rcon_ip.text = autofill.get('ip')['value']
		self.w_rcon_port.text = autofill.get('port')['value']
		self.w_rcon_pass.text = autofill.get('pass')['value']
class MainApp(MDApp):
	def build(self):
		sm.add_widget(Login(name = 'Login'))
		sm.add_widget(Rconsole(name = 'Rconsole'))

		return sm

MainApp().run()
