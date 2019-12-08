
from launchpad_manager import LaunchpadManager


class Menu:

	def __init__(self):
		self.__m = LaunchpadManager()

	def welcome(self):
		print("Welcome to use Launchpad-Listen-To-Me for MacOS!")
		print()
		print("Still bothering about the useless icons in launchpad?")
		print("I can help you let them go away!")
		print()
		print("\t\t\t\t\t\t\t\tby ACat")
		print()

	def menu(self):
		print("OK! Here are all of the things I can do for you:")
		print("\t1. List all the icons of the apps in your Launchpad")
		print("\t2. Remove the icon of the app you don't need")
		print("\t3. Store the current arrangement of your Launchpad")
		print("\t4. Restore the current arrangement of your Launchpad from a backup file")
		print("\t5. Reboot your Launchpad")
		print("\t6. Reset your Launchpad")
		print("\t7. Exit")

		# print("Notified:")
		# print("\tWhen all of the things have done")
		# print("\tplease enter number 6 to say goodbye to me,")
		# print("\tor your changes will be lost after the OS restarts.")
		print()
		print("Now, please input a number to tell me what you wanna do:")

	def list_icons(self):

		print("All the icons of the apps in your Launchpad by pages are as follow.")
		print("And, the group name appears in square brackets, like '[Others]'.")

		print()

		m = self.__m
		root = m.root
		groups = []

		for i, page in enumerate([page for page in root.children if page.id > 6]):
			print("== Page %s ==" % (i + 1))
			m.show_page(page.id)
			print()
			for item in page.children:
				if item.id in m.groups:
					groups.append(item)

		for group in groups:
			for i, page in enumerate(group.children):
				print("== Group [%s] Page %s ==" % (group.title, i + 1))
				m.show_page(page.id)
				print()

	def remove(self):

		m = self.__m

		print("You can remove the icon of the app from your Launchpad by input its number:")
		n = input()

		if not n.isdecimal():
			print("Sorry, you input something wrong.")
		else:
			n = int(n)
			if m.remove_app_icon(n):
				print("Successful!")
			else:
				print("Sorry, something wrong happened!")
		print()

	def store(self):
		m = self.__m
		print("Please input a file path to save a backup file for the arrangement of your Launchpad:")
		path = input()
		if m.store(path):
			print("Successful!")
		else:
			print("Sorry, something wrong happened!")
		print()

	def restore(self):
		m = self.__m
		print("Please input the path of the backup file to restore the arrangement of your Launchpad:")
		path = input()
		if m.restore(path):
			print("Successful!")
		else:
			print("Sorry, something wrong happened!")
		print()

	def reboot(self):
		self.__m.reboot()
		print("Now, your Launchpad has been rebooted!")
		print()

	def reset(self):
		self.__m.reset()
		print("Now, your Launchpad has been reset!")
		print()

	def exit(self):
		self.__m.close()
		print("Thank you for your use! Bye~")

	def run(self):

		self.welcome()
		self.menu()
		cmd = input()
		print()

		while True:
			if cmd == "1":
				self.list_icons()
			elif cmd == "2":
				self.remove()
			elif cmd == "3":
				self.store()
			elif cmd == "4":
				self.restore()
			elif cmd == "5":
				self.reboot()
			elif cmd == "6":
				self.reset()
			elif cmd == "7":
				break
			else:
				print("You input something wrong, please try again:")
				cmd = input()
				print()
				continue

			self.menu()
			cmd = input()
			print()

		self.exit()

if __name__ == "__main__":
	Menu().run()



