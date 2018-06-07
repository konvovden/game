from random import *
import os
import sys
from termcolor import colored, cprint
from colorama import init, Fore, Back, Style

init() 

MAX_WORLD_ITEMS_TYPES = 3 # Количество типов предметов
WORLD_ITEMS_AMOUNT = 5 # Количество предметов в мире

shop_buy_item_names = ['Доспехи', 'Меч' + Fore.GREEN + ' (+ 5 урона)' + Style.RESET_ALL]
shop_buy_item_prices = [2, 3]

inventory_item_names = ['Доспехи', 'Меч', 'Сердце орка']
inventory_item_prices = [2, 3, 1]


skills = [1, 1, 1, 1] 
# 0 - Сила
# 1 - Ловкость
# 2 - Удача
# 3 - Переносимый вес

skills_names = ['Сила', 'Ловкость', 'Удача', 'Переносимый вес']

a = ['', '', '']
# Список a - Описание персонажа
# 	0 - имя персонажа - str
# 	1 - пол персонажа - str
# 	2 - навыки персонажа - str
# 	Характеристики персонажа:
# 	3 - сила персонажа - int
# len(a)

move = 0
score = 0
exp = 0
level = 0
health = 100
damage = 5
money = 0

player_pos = [30,10]

place = 0

lose = 0
exit = 0

equiped_weapon = 0
equiped_weapon_slot = -1

mob_damage = 0
mob_health = 0
mob_level = 0

inventory = []


def LoadPlayer(file):
	global a 
	global skills
	global health
	global level
	global exp
	global score
	global inventory
	global place
	global move
	global money
	file_content = file.read()
	file_list = file_content.split('|')
	a[0] = file_list[0]
	a[1] = file_list[1]
	a[2] = file_list[2]
	skills[0] = int(file_list[3])
	skills[1] = int(file_list[4])
	skills[2] = int(file_list[5])
	skills[3] = int(file_list[6])
	health = int(file_list[7])
	level = int(file_list[8])
	exp = int(file_list[9])
	score = int(file_list[10])
	place = int(file_list[11])
	move = int(file_list[12])
	money = int(file_list[14])
	if(len(file_list[13]) != 2):
		 inventory_array = file_list[13].replace('[', '').replace(']', '').split(',')
		 for i in range(len(inventory_array)):
		 	inventory.append(int(inventory_array[i]))


	# for i in range(len(inventory)):
	# 	inventory[i] = int(inventory[i])
	file.close()
	print(InfoText() + 'Профиль успешно загружен!\n\n\n\n\n')

def SavePlayer():
	global a 
	global skills
	global health
	global level
	global exp
	global score
	global inventory
	global place
	global move
	file = open('save.txt', 'w')

	file_list = []
	file_list.append(a[0])
	file_list.append(a[1])
	file_list.append(a[2])
	file_list.append(skills[0])
	file_list.append(skills[1])
	file_list.append(skills[2])
	file_list.append(skills[3])
	file_list.append(health)
	file_list.append(level)
	file_list.append(exp)
	file_list.append(score)
	file_list.append(place)
	file_list.append(move)
	file_list.append(inventory)
	file_list.append(money)

	file_content = ''
	for i in range(len(file_list)):
		file_content += str(file_list[i]) + '|'
	file.write(file_content)
	file.close()






def CreatePlayer():
	global a
	a[0] = input('Ты кто? ')
	a[1] = input('Какой у тебя пол? ')
	a[2] = input('Что ты умеешь? ')
	print('Добро пожаловать в наш мир, '+ a[0] +'.')
	print('Такие навыки, как ' + a[2] + ' помогут тебе во время путешествия!')
	input('Нажмите Enter для продолжения.')
	SavePlayer()

def ShowInventory():
	global equiped_weapon
	global equiped_weapon_slot
	global inventory
	global exit
	os.system('cls')
	while True:
		print(InfoText() + 'Ваш инвентарь: \n')
		if len(inventory):
			for i in range(len(inventory)):
				if(i != equiped_weapon_slot):
					print(str(i+1) + '. ' + GetItemPowerColor(GetItemPower(inventory[i])) + GetItemName(inventory[i]) + ' (+' + str(GetItemPower(inventory[i])) + ' урона)' + Style.RESET_ALL)
				else:
					print(str(i+1) + '. ' + Fore.CYAN + GetItemName(inventory[i]) + ' (+' + str(GetItemPower(inventory[i])) + ' урона)' + Style.RESET_ALL)
		print(str(len(inventory)+1) + '. Назад')
		action = input('Введите номер предмета для использования: ')
		if action.isdigit() == False and action != 'exit':
			os.system('cls')
			print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
		elif action == 'exit':
			exit = 1
			break
		else:
			action = int(action) - 1
			if action >= len(inventory):
				os.system('cls')
				break;
			else: 
				UseItem(action)

def InfoText() -> str:
	return '[' + Fore.YELLOW + 'i' + Style.RESET_ALL + '] ' 

def UseItem(slot):
	global inventory
	global equiped_weapon
	global equiped_weapon_slot
	if (inventory[slot] >= 1000000) and (inventory[slot] <= 2000000):
		if equiped_weapon_slot != slot:
			equiped_weapon = inventory[slot]
			equiped_weapon_slot = slot

			CalculatePlayerDamage()
			os.system('cls')
			print(InfoText() + "Вы экипировали оружие '" + GetItemPowerColor(GetItemPower(inventory[slot])) + GetItemName(inventory[slot]) + Style.RESET_ALL + "'.")
		else:
			equiped_weapon = 0
			equiped_weapon_slot = -1
			CalculatePlayerDamage()
			os.system('cls')
			print(InfoText() + "Вы убрали из рук оружие '" + GetItemPowerColor(GetItemPower(inventory[slot])) + GetItemName(inventory[slot]) + Style.RESET_ALL + "'.")



locations = ['Деревня питонистов', 'Торговая лавка', 'Деревня орков']

def ShowLocations(without):
	global locations
	global place
	global exit
	global move
	temp_locations = locations.copy()
	temp_locations_nums = []
	for i in range(len(temp_locations)):
		temp_locations_nums.append(i)
	del temp_locations_nums[without]
	del temp_locations[without]
	os.system('cls')
	while True:
		print(InfoText() + 'Список доступных локаций:\n')
		for i in range(len(temp_locations)):
			print(str(i+1) + '. ' + temp_locations[i])
		print(str(len(temp_locations)+1) + '. Назад')

		action = input('Введите желаемую локацию: ')
		if action.isdigit() == False and action != 'exit':
			os.system('cls')
			print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
		elif action == 'exit':
			exit = 1
			break
		else:	
			action = int(action)-1
			if action != len(temp_locations):
				place = temp_locations_nums[action]
				os.system('cls')
				move = 0
			else:
				os.system('cls')
			break

def CalculatePlayerDamage():
	global damage
	global inventory
	damage = skills[0]*2.5
	if(equiped_weapon != 0):
		damage += GetItemPower(equiped_weapon)
	damage = int(damage)
def CalculateMobDamage() -> int:
	global inventory
	global move
	mob_damage = randint(1+int(round(0.3*move)), 10+int(round(0.3*move)))
	return mob_damage

def ShowCharacterMenu():
	global a
	global health
	global damage
	global score
	global exp
	global level
	global money
	global skills
	global exit

	os.system('cls')
	cicle_exit = 0
	while True:
		if cicle_exit != 0:
			break
		print(InfoText() + 'Информация о персонаже:\n')

		print('Имя:\t\t\t' + Fore.GREEN + a[0] + Style.RESET_ALL)
		print('Пол:\t\t\t' + Fore.GREEN + a[1] + Style.RESET_ALL)
		print('Умения:\t\t' + Fore.GREEN + a[2] + Style.RESET_ALL + '\n')

		print(InfoText() + 'Навыки персонажа:\n')

		print('Сила:\t\t\t' + Fore.GREEN + str(skills[0]) + Style.RESET_ALL)
		print('Ловкость:\t\t' + Fore.GREEN + str(skills[1]) + Style.RESET_ALL)
		print('Удача:\t\t\t' + Fore.GREEN + str(skills[2]) + Style.RESET_ALL)
		print('Переносимый вес:\t' + Fore.GREEN + str(skills[3]) + Style.RESET_ALL + '\n')

		print('Здоровье:\t\t' + Fore.GREEN + str(health) + Style.RESET_ALL)
		print('Уровень:\t\t' + Fore.GREEN + str(level) + Style.RESET_ALL)
		print('Очки умений:\t\t' + Fore.GREEN + str(exp) + Style.RESET_ALL)
		print('Счёт:\t\t\t' + Fore.GREEN + str(score) + Style.RESET_ALL + '\n')

		print('1. Улучшение навыков персонажа\n2. Назад')

		action = input('Введите желаемое действие: ')
		if action.isdigit() == False and action != 'exit':
			os.system('cls')
			print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
		elif action == 'exit':
			exit = 1
			break
		else:
			action = int(action)
			if action == 1:
				os.system('cls')
				while True:
					print(InfoText() + 'Количество EXP: ' + Fore.GREEN + str(exp) + Style.RESET_ALL)
					print('1. Сила:\t\t\t' + Fore.GREEN + str(skills[0]) + Style.RESET_ALL, end ='\t')
					if exp < int(round(skills[0]*0.5)):
						print(Fore.RED + str(1 + int(round(skills[0]*0.5))) + ' exp'+ Style.RESET_ALL)
					else:
						print(Fore.GREEN + str(1 + int(round(skills[0]*0.5))) + ' exp'+ Style.RESET_ALL)
					print('2. Ловкость:\t\t\t' + Fore.GREEN + str(skills[1]) + Style.RESET_ALL, end = '\t')
					if(exp < int(round(skills[1]*0.5))):
						print(Fore.RED + str(1 + int(round(skills[1]*0.5))) + ' exp'+ Style.RESET_ALL)
					else:
						print(Fore.GREEN + str(1 + int(round(skills[1]*0.5))) + ' exp'+ Style.RESET_ALL)
					print('3. Удача:\t\t\t' + Fore.GREEN + str(skills[2]) + Style.RESET_ALL, end = '\t')
					if(exp < int(round(skills[2]*0.5))):
						print(Fore.RED + str(1 + int(round(skills[2]*0.5))) + ' exp'+ Style.RESET_ALL)
					else:
						print(Fore.GREEN + str(1 + int(round(skills[2]*0.5))) + ' exp'+ Style.RESET_ALL)
					print('4. Переносимый вес:\t\t' + Fore.GREEN + str(skills[3]) + Style.RESET_ALL, end = '\t')
					if(exp < int(round(skills[3]*0.5))):
						print(Fore.RED + str(1 + int(round(skills[3]*0.5))) + ' exp'+ Style.RESET_ALL)
					else:
						print(Fore.GREEN + str(1 + int(round(skills[3]*0.5))) + ' exp'+ Style.RESET_ALL)

					print('5. Назад')
 
					action = input('Введите желаемый навык: ')

					if action.isdigit() == False and action != 'exit':
						os.system('cls')
						print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
					elif action == 'exit':
						exit = 1
						cicle_exit = 1
						break
					else:
						action = int(action)
						if action < 5:
							if(exp < 1 + int(round(skills[action-1]*0.5))):
								os.system('cls')
								print(Fore.RED + 'У Вас недостаточно EXP!' + Style.RESET_ALL)
							else:
								exp -= 1 + int(round(skills[action-1]*0.5))
								level += 1
								os.system('cls')
								print(Fore.GREEN + "Вы улучшили навык '" + skills_names[action-1] + "' до " + str(skills[action-1]+1) + ' за ' + str(1 + int(round(skills[action-1]*0.5))) + ' EXP!' + Style.RESET_ALL)
								skills[action-1] += 1
						else:
							os.system('cls')
							cicle_exit = 1
							break;
			elif action == 2:
				os.system('cls')
				cicle_exit = 1
				break


items_properties_names = []
items_properties_rates = []
items_charact_names = []
items_charact_rates = []
items_names_names = []
items_names_rates = []

MAX_ITEM_CHARACT = 0
MAX_ITEMS_NAMES = 0
MAX_ITEM_PROPERTIES = 0

def LoadItems():
	os.system('cls')
	global items_properties_names
	global items_properties_rates
	global items_charact_names
	global items_charact_rates
	global items_names_names
	global items_names_rates
	global MAX_ITEM_PROPERTIES
	global MAX_ITEMS_NAMES
	global MAX_ITEM_CHARACT
	if os.path.isfile('properties.txt'):
		file = open('properties.txt', 'r')
		file_content = file.read()
		file_content = file_content.split('\n')
		MAX_ITEM_PROPERTIES = len(file_content)
		for i in range(len(file_content)):
			file_content[i] = file_content[i].split(' ')
			items_properties_names.append(file_content[i][0])
			items_properties_rates.append(float(file_content[i][1]))
		file.close()
		print(Fore.GREEN + 'Свойства предметов успешно загружены! Всего ' + str(MAX_ITEM_PROPERTIES) + ' предметов' + Style.RESET_ALL)
	else:
		print(Fore.MAGENTA + 'Свойства предметов не загружены!' + Style.RESET_ALL)
		sys.exit()

	if os.path.isfile('charact.txt'):
		file = open('charact.txt', 'r')
		file_content = file.read()
		file_content = file_content.split('\n')
		MAX_ITEM_CHARACT = len(file_content)
		for i in range(len(file_content)):
			file_content[i] = file_content[i].split(' ')
			items_charact_names.append(file_content[i][0])
			items_charact_rates.append(float(file_content[i][1]))
		file.close()
		print(Fore.GREEN + 'Характеристики предметов успешно загружены! Всего ' + str(MAX_ITEM_CHARACT) + ' предметов' + Style.RESET_ALL)
	else:
		print(Fore.MAGENTA + 'Характеристики предметов не загружены!' + Style.RESET_ALL)
		sys.exit()
	if os.path.isfile('names.txt'):
		file = open('names.txt', 'r')
		file_content = file.read()
		file_content = file_content.split('\n')
		MAX_ITEMS_NAMES = len(file_content)
		for i in range(len(file_content)):
			file_content[i] = file_content[i].split(' ')
			items_names_names.append(file_content[i][0])
			items_names_rates.append(float(file_content[i][1]))
		file.close()
		print(Fore.GREEN + 'Имена предметов успешно загружены! Всего ' + str(MAX_ITEMS_NAMES) + ' предметов' +  Style.RESET_ALL)
	else:
		print(Fore.MAGENTA + 'Имена предметов не загружены!' + Style.RESET_ALL)
		sys.exit()




def GetItemName(itemid) -> str:
	global items_properties_names
	global items_properties_rates
	global items_charact_names
	global items_charact_rates
	global items_names_names
	global items_names_rates

	propertyid = (itemid // 10000) % 100
	charactid = (itemid // 100) % 100
	namesid = itemid % 100

	name = ''
	name += items_properties_names[propertyid]
	name += ' '
	name += items_charact_names[charactid]
	name += ' '
	name += items_names_names[namesid]
	return name

def GetItemPower(itemid) -> int:
	global items_properties_names
	global items_properties_rates
	global items_charact_names
	global items_charact_rates
	global items_names_names
	global items_names_rates

	itemid = itemid % 1000000
	propertyid = itemid // 10000
	charactid = (itemid // 100) % 100
	namesid = itemid % 100

	power = 1
	power *= items_properties_rates[propertyid]
	power *= items_charact_rates[charactid]
	power += items_names_rates[namesid]
	return int(power)

def GetItemPowerColor(power) -> str:
	global items_properties_rates
	max_ = 0
	min_ = 10000000
	for i in range(len(items_properties_rates)):
		if items_properties_rates[i] > max_: 
			max_ = items_properties_rates[i]
		if items_properties_rates[i] < min_:
			min_ = items_properties_rates[i]
	if (power <= (max_ - min_) // 3):
		return Fore.RED
	elif (power <= (max_ - min_) // 3 *2):
		return Fore.YELLOW
	else:
		return Fore.GREEN

def GenerateNewItem() -> int:
	returned = '1'

	gen = randint(0, MAX_ITEM_PROPERTIES-1)
	if gen < 10:
		gen = '0'+ str(gen)
	returned += gen

	gen = randint(0, MAX_ITEM_CHARACT-1)
	if gen < 10:
		gen = '0'+ str(gen)
	returned += gen

	gen = randint(0, MAX_ITEMS_NAMES-1)
	if gen < 10:
		gen = '0'+ str(gen)
	returned += gen
	return int(returned)

def GenerateNewMob():
	global mob_damage
	global mob_health
	global mob_level
	global level
	global move

	mob_level = randint(1+int(move*0.5), 10+int(move*0.5))
	mob_damage = randint(int(mob_level*2.5), mob_level*5)
	mob_health = randint(mob_level*25, mob_level*50)

levels = []
LEVELS_COUNT = 0

def LoadLevels():
	global levels
	global LEVELS_COUNT
	i = 0
	while True:
		i += 1
		if(os.path.isfile('levels/'+str(i)+'.txt')):
			LEVELS_COUNT += 1
			levels.append([])

			file = open('levels/' + str(i) + '.txt', 'r')
			file_content = file.read()
			levels[LEVELS_COUNT-1] = file_content.split('\n')

			file.close()
		else:
			break

def ShowLevel(levelid):
	global levels
	global LEVELS_COUNT
	if levelid > LEVELS_COUNT:
		print(Fore.RED + 'Ошибка! Номер уровня больше максимального!' + Style.RESET_ALL)
		return
	levelid -= 1
	for i in range(len(levels[levelid])):
		string = ' ' * 10
		for j in range(len(levels[levelid][i])):
			string += GetBlockSymbol(int(levels[levelid][i][j]))
		print(string)

		# string = ' ' * 10
		# string += levels[levelid][i]
		# print(string)

def GetBlockSymbol(blocknum) -> str:
	returned = ''
	if blocknum == 0:
		returned = ' '
	elif blocknum == 1:
		returned = Fore.WHITE + Style.DIM + '#' + Style.RESET_ALL
	elif blocknum == 2:
		returned = Fore.BLUE + Style.BRIGHT + '@' + Style.RESET_ALL
	return returned

def UpdateLevel(levelid):
	global levels
	global player_pos
	player_pos = [10, 30]
	levelid = levelid - 1
	while True:
		levels[levelid][player_pos[0]][player_pos[1]] = 2
		ShowLevel(levelid)
		input()
		break




LoadLevels()
UpdateLevel(1)

sys.exit()

LoadItems()



if os.path.isfile('save.txt'):
	file = open('save.txt', 'r')
	LoadPlayer(file)
else:
	CreatePlayer()


while True:
	SavePlayer()
	if lose != 0:
		os.system('cls')
		print(Fore.RED + 'Ты умер! Игра закончена! ' + Style.RESET_ALL + 'Счёт: ' + str(score))
		break
	if exit != 0:
		os.system('cls')
		print(InfoText() + 'Вы вышли из игры!')
		break;
	if place != 1: print(InfoText(), "Вы находитесь в локации '" + locations[place] + "'.\n")
	if place == 0:
		print('Доступные действия:\n1. Отправиться в ...\n2. Инвентарь\n3. Персонаж\n4. Выйти из игры')
		action = input('Ввежите желаемое действие: ')

		if action.isdigit() == False and action != 'exit':
			os.system('cls')
			print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
		elif action == 'exit':
			exit = 1
		else:
			if int(action) == 1:
				ShowLocations(place)
			elif int(action) == 2:
				ShowInventory()
			elif int(action) == 3:
				ShowCharacterMenu()
			elif int(action) == 4:
				exit = 1
	elif place == 1:
		shop_stage = 0
		while True:
			if shop_stage == 0:
				print(InfoText(), "Вы находитесь в локации '" + locations[place] + "'.\n")
				print('Доступные действия:\n1. Купить\n2. Продать\n3. Персонаж\n4. Переместиться в...')
				action = input('Введите желаемое действие: ')
				if action.isdigit() == False and action != 'exit':
					os.system('cls')
					print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
				elif action == 'exit':
					exit = 1
					break
				else:
					if int(action) == 3:
						ShowCharacterMenu()
						break
					elif int(action) == 4:
						os.system('cls')
						ShowLocations(place)
						break
					shop_stage = int(action)
					os.system('cls')
			elif shop_stage == 1:
				print('Ты зашёл внутрь и заговорил с торговцем.\n')
				print(Fore.YELLOW, '- Что ты желаешь купить?')
				items = []
				for i in range(3):
					items.append(GenerateNewItem())
					print(Style.RESET_ALL + str(i+1)+'. ' + GetItemPowerColor(GetItemPower(items[i])) + GetItemName(items[i]) + ' (+ ' + str(GetItemPower(items[i])) + ' урона)', end = '\t\t\t')
					if(money >= int(2.28*GetItemPower(items[i]))):
						print(Fore.GREEN + str(int(2.28*GetItemPower(items[i]))))
					else:
						print(Fore.RED + str(int(2.28*GetItemPower(items[i]))))
				print(Style.RESET_ALL + '3. Назад')
				print(Style.RESET_ALL + 'Введите желаемый предмет: ')
				item = input()
				if item.isdigit() == False and item != 'exit':
					os.system('cls')
					print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
				elif item == 'exit':
					exit = 1
					break
				else:
					item = int(item)
					if(item == 3):
						shop_stage = 0
						os.system('cls')
						continue
					elif(int(2.28*GetItemPower(items[item-1])) > money):
						os.system('cls')
						print(Fore.RED + 'У Вас недостаточно денег для покупки предмета!\n' + Style.RESET_ALL)
					else:
						inventory.append(items[item-1])
						money -= int(2.28*GetItemPower(items[item-1]))
						os.system('cls')
						print(Fore.GREEN +"Вы купили предмет '" + GetItemName(items[item-1]) + "' за " + str(int(2.28*GetItemPower(items[item-1]))) + ".\n" + Style.RESET_ALL)
						items[item-1] = GenerateNewItem()
			elif shop_stage == 2:
				print('Ты зашёл внутрь и заговорил с торговцем.')
				print(Fore.YELLOW, '- Что ты желаешь продать?' + Style.RESET_ALL)
				if len(inventory) != 0:
					for i in range(len(inventory)):
						# print(Style.RESET_ALL + str(i+1) + '. ' + inventory_item_names[inventory[i]] + '\t\t' + Fore.GREEN + str(inventory_item_prices[inventory[i]]) + Style.RESET_ALL)
						if inventory[i] >= 1000000 and inventory[i] <= 1999999:
							print(str(i+1) + '. ' + GetItemPowerColor(GetItemPower(inventory[i])) + GetItemName(inventory[i]) + ' (+ ' + str(GetItemPower(inventory[i])) + ' урона)\t\t\t' + Fore.GREEN + str(int(2*GetItemPower(inventory[i]))) + Style.RESET_ALL)
				print(str(len(inventory)+1) + '. Назад')
				print('Введите желаемый предмет: ')
				item = input()
				if item.isdigit() == False and item != 'exit':
					os.system('cls')
					print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
				elif item == 'exit':
					exit = 1
					break
				else:
					item = int(item)-1
					if item == len(inventory):
						shop_stage = 0
						os.system('cls')
					else:
						money += inventory_item_prices[inventory[item]]
						os.system('cls')
						print(Fore.GREEN + "Вы продали предмет '" + inventory_item_names[inventory[item]] + "' за " + str(inventory_item_prices[inventory[item]]) + '.\n')
						del inventory[item]
	elif place == 2:
		if move != 0:
			print(InfoText() + 'Вы прошли по локации уже ' + str(move*10) + ' шагов.')
		print('Доступные действия: \n1. Войти в подземелье\n2. Инвентарь\n3. Персонаж\n4. Переместиться в...')
		action = input('Введите желаемое действие: ')
		if action.isdigit() == False and action != 'exit':
			os.system('cls')
			print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
		elif action == 'exit':
			exit = 1
		else:
			action = int(action)
			if action == 1:
				mobnum = randint(1, 2)
				if mobnum == 1: 
					os.system('cls')
					while True:
						print(InfoText(), 'Вы нашли мешок с неизвестным содержимым.\n')
						print('Доступные действия: \n1. Открыть\n2. Пройти мимо')

						action = input('Ввежите желаемое действие: ')

						if action.isdigit() == False and action != 'exit':
							os.system('cls')
							print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
						elif action == 'exit':
							exit = 1
							break
						else:
							action = int(action)
							if action == 1:
								score += 1
								os.system('cls')
								loot = randint(0, 1)
								if loot == 0:
									print(Fore.RED + 'Вы ничего не нашли!\n' + Style.RESET_ALL)
									break
								elif loot == 1:
									lootamount = randint(1, 100)
									money += lootamount
									print(Fore.GREEN + 'Вы нашли золото! Деньги +' + str(lootamount) + ' (' + str(money) + ').\n' + Style.RESET_ALL)
									break
							elif action == 2:
								os.system('cls')
								print(InfoText() + 'Вы прошли мимо сумки\n')
								break
					move += 1
				elif mobnum == 2:
					os.system('cls')
					cicle_exit = 0
					GenerateNewMob()
					while True:
						if cicle_exit != 0:
							break
						print(InfoText() + 'Вы столкнулись с орком! Уровень: ' + Fore.RED + str(mob_level) + Style.RESET_ALL + '\n')
						print('Доступные действия:\n1. Сразиться\n2. Убежать')
						action = input('Введите желаемое действие: ')
						if action.isdigit() == False and action != 'exit':
							os.system('cls')
							print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
						elif action == 'exit':
							exit = 1
							break
						else:
							action = int(action)
							if action == 2:
								if randint(0, 3) == 0:
									health -= 5
									os.system('cls')
									print('Тебе не удалось убежать от орка. ' + Fore.RED + 'Здоровье -5 (' + str(health) + ').\n' + Style.RESET_ALL)
									break
									if health <= 0:
										lose = 1
								else:
									score += 1
									os.system('cls')
									print('Тебе удалось сбежать от орка! ' + Fore.GREEN + 'Очки +1 (' + str(score) + ').\n')
									break
							else:
								os.system('cls')
								while True:
									if mob_health <= 0:
										score += 5
										move += 1
										os.system('cls')
										print('Вы победили орка! ' + Fore.GREEN + 'Счёт +5 (' + str(score) + ').\n' + Style.RESET_ALL)
										cicle_exit = 1
										break
									elif health <= 0:
										lose = 1
										cicle_exit = 1
										break
									CalculatePlayerDamage()
									print(InfoText() + 'Вы сражаетесь с орком!\n')
									print(Fore.GREEN + 'Ваше здоровье: ' + str(health) + '. Ваш урон: ' + str(damage) + '.')
									print(Fore.RED + 'Здоровье моба: ' + str(mob_health) + '. Урон моба: ' + str(mob_damage) + '.' + Style.RESET_ALL)
									print('Доступные действия:\n1. Ударить\n2. Инвентарь\n3. Сбежать')
									action = input('Введите желаемое действие: ')
									if action.isdigit() == False and action != 'exit':
										os.system('cls')
										print(Fore.RED + 'Введите число!\n\n' + Style.RESET_ALL)
									elif action == 'exit':
										exit = 1
										cicle_exit = 1
										break
									else:
										action = int(action)
										os.system('cls')
										if action == 1:
											mob_health -= damage
											health -= mob_damage
										elif action == 2:
											ShowInventory()
										else:
											if randint(0, 3) == 0:
												health -= 5
												os.system('cls')
												print('Тебе не удалось убежать от орка. ' + Fore.RED + 'Здоровье -5 (' + str(health) + ').\n' + Style.RESET_ALL)
												cicle_exit
												break
											else:
												score += 1
												os.system('cls')
												print('Тебе удалось сбежать от орка! ' + Fore.GREEN + 'Очки +1 (' + str(score) + ').\n' + Style.RESET_ALL)
												cicle_exit = 1
												break
			elif action == 2:
				ShowInventory()
			elif action == 3:
				ShowCharacterMenu()
			elif action == 4:
				os.system('cls')
				ShowLocations(place)





