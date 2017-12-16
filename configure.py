import os
import platform as _platform
import shutil
import sys

platform = "(NULL)"
firmware = "(NULL)"

def is_number(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def copy_to(from_dir, from_name, to_dir, to_name):
	shutil.copy(os.path.join(from_dir, from_name), to_dir)
	os.rename(os.path.join(to_dir, from_name), os.path.join(to_dir, to_name))

def delete_file(path):
	if os.path.isfile(path):
		os.remove(path)

def screen_clear():
	if _platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def title_print():
	screen_clear()
	print("setaria build environment configure tool")

def data_print():
	print("Target platform:", platform)
	print("Target firmware:", firmware)
	print()

def do_action1():
	title_print()
	print("Please enter the number of the target platform you want to change.")
	print()
	data_print()
	print("0. Back to the menu")
	print("1. x86-64 (x64, amd64, IA-32e)")
	print()

	loop = True
	while loop:
		print(">>> ", end="")
		number = input()
		if is_number(number):
			number = int(number)
		else:
			print("Unknown value. Please retry.")
			print()
			continue

		if number == 0:
			loop = False
		elif number == 1:
			global platform
			platform = "x86-64"
			loop = False
		else:
			print("Unknown number. Please retry.")
			print()

def do_action2():
	title_print()
	print("Please enter the number of the target firmware you want to change.")
	print()
	data_print()
	print("0. Back to the menu.")
	print("1. BIOS")
	print()

	loop = True
	while loop:
		print(">>> ", end="")
		number = input()
		if is_number(number):
			number = int(number)
		else:
			print("Unknown value. Please retry.")
			print()
			continue

		if number == 0:
			loop = False
		elif number == 1:
			global firmware
			firmware = "BIOS"
			loop = False
		else:
			print("Unknown number. Please retry.")
			print()

def do_action3():
	title_print()
	print("Please wait...")
	print()
	data_print()

	global platform
	global firmware

	can_do = True

	if platform == "(NULL)":
		print("The target platform isn't set up.\n")
		can_do = False
	elif firmware == "(NULL)":
		print("The target firmware isn't set up.\n")
		can_do = False

	if not can_do:
		print("Press Enter to return to the menu.")
		input()
		return

	if platform == "x86-64":
		error = do_action3_x86_64(firmware)
		if error:
			print("If the error persists, contact the developer.")
			print("Press Enter to return to the menu.")
			input()
			return

	print("Done!")
	print()

	print("Press Enter to exit.")
	input()
	exit()

def do_action3_x86_64(firmware):
	copy_to("./make/x86", "root", "./", "makefile")

	if firmware == "BIOS":
		copy_to("./make/x86-64", "boot_bios", "./arch/x86/boot", "makefile")

	return False

def do_action4():
	title_print()
	print("Please wait...")
	print()
	data_print()

	delete_file("./arch/x86/boot/makefile")
	delete_file("./makefile")

	delete_file("./run.bat")
	delete_file("./run.sh")

	print("Done!")

	print("Press Enter to return to the menu.")
	input()

def do_action5():
	title_print()
	print()
	data_print()

	global platform
	global firmware

	can_do = True

	if platform == "(NULL)":
		print("The target platform isn't set up.\n")
		can_do = False
	elif firmware == "(NULL)":
		print("The target firmware isn't set up.\n")
		can_do = False

	if not can_do:
		print("Press Enter to return to the menu.")
		input()
		return

	if firmware == "BIOS":
		if platform == "x86-64":
			desc = "qemu-system-x86_64 -L . -m 64 -fda ./setaria.img -localtime -M pc"

			f = open("./run.bat", "w")
			f.write(desc)
			f.close()

			f = open("./run.sh", "w")
			f.write(desc)
			f.close()

	print("Done!")

	print("Press Enter to return to the menu.")
	input()

def mainmenu():
	loop_main = True
	while loop_main:
		title_print()
		print()
		data_print()

		print("Please enter the desired action number.")
		print()
		print("1. Change the target platform")
		print("2. Change the target firmware")
		print("3. Configure build environment")
		print("4. Reset the build environment")
		print("5. Generate run.bat/sh files for QEMU execution")
		print("6. Exit")
		print()

		loop = True
		while loop:
			print(">>> ", end="")
			number = input()
			if is_number(number):
				number = int(number)
			else:
				print("Unknown value. Please retry.")
				print()
				continue

			if number == 1:
				do_action1()
				loop = False
			elif number == 2:
				do_action2()
				loop = False
			elif number == 3:
				do_action3()
				loop = False
			elif number == 4:
				do_action4()
				loop = False
			elif number == 5:
				do_action5()
				loop = False
			elif number == 6:
				print()
				loop = False
				loop_main = False
			else:
				print("Unknown number. Please retry.")
				print()

if __name__ == "__main__":
	mainmenu()
