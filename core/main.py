import os
import sqlite3


class LaunchpadDB:

	def __init__(self, db_file):
		self.__db_file = db_file
		self.__db_conn = sqlite3.connect(db_file)
		self.__apps = []

	@property
	def db_conn(self):
		return self.__db_conn

	@property
	def apps(self):
		return self.__apps

	def read_db(self) -> bool:
		"""
		从数据库文件读取数据,
		若操作成功, 则将数据存储于 self.__apps 中,
		返回值代表该操作的成功与否
		"""
		if not self.__db_conn:
			return False
		cursor = self.__db_conn.execute("SELECT item_id, title FROM apps")
		for row in cursor:
			id, title = row
			self.__apps.append((id, title))
		return True

	def delete_app(self, id):
		"""
		根据 id 删除 app 记录
		"""
		conn = self.__db_conn
		cursor = conn.execute("DELETE FROM apps WHERE item_id=%s" % id)
		if cursor.rowcount == 0:
			return False

		conn.commit()
		return True

	def close(self):
		self.__db_conn.close()


def locate_launchpad_db(path = "/private/var/folders"):
	"""
	查找 launchpad db 数据库位置
	"""

	for dir in os.listdir(path):

		if not os.path.isdir(os.path.join(path, dir)):
			continue

		if dir == "com.apple.dock.launchpad":
			return os.path.join(path, dir, "db", "db")
		else:
			try:
				r = locate_launchpad_db(os.path.join(path, dir))
			except Exception as _:
				r = None
			if r is not None:
				return r


def reboot_launchpad():
	"""
	重启 Launchpad
	"""
	os.system("killall Dock")


if __name__ == "__main__":
	# launchpad_db = LaunchpadDB("/Users/acat/Desktop/db")
	launchpad_db = LaunchpadDB(locate_launchpad_db())
	launchpad_db.read_db()
	apps = launchpad_db.apps

	print("All of the APPs in your Launchpad are as follow:")
	for i, (_, title) in enumerate(apps):
		print("\t%s %s" % (i + 1, title))
	print("Input the number before the App's name to remove its icon, or input 'exit' to exit:")

	while True:
		str = input()

		if str == "exit":
			break

		elif str.isdecimal():
			n = int(str)
			if not 0 < n <= len(apps):
				print("Please input a number in the list:")
				continue

			deleted_id = apps[n - 1][0]
			if launchpad_db.delete_app(deleted_id):
				print("The icon for the APP has been already removed from your Launchpad.")
				break
			else:
				print("Something wrong happened! The icon for the APP CANNOT be removed from your Launchpad.")
				break

		else:
			print("Illegal input! Please input the number before the App's name to remove its icon, or input 'exit' to exit:")

	launchpad_db.close()
	reboot_launchpad()
	print("Thank you for using. Bye~")


