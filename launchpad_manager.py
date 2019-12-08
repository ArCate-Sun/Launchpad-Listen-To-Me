import os
import shutil
import sqlite3

from launchpad_item import LaunchpadItem


class LaunchpadManager:

	def __init__(self):
		db_file = LaunchpadManager.__locate_launchpad_db()
		# db_file = "/Users/acat/Desktop/db"
		if db_file is None:
			raise Exception("Cannot find Launchpad db file!")

		db_conn = sqlite3.connect(db_file)

		self.__db_file = db_file
		self.__db_conn = db_conn
		self.__items = {}

		self.__load_arrangement()

	@staticmethod
	def __locate_launchpad_db(path = "/private/var/folders") -> str:
		"""
		查找 launchpad db 数据库位置
		"""

		if path.endswith("com.apple.dock.launchpad"):
			r = os.path.join(path, "db", "db")
			if os.path.exists(r):
				return r
			else:
				return None

		r = None
		for dir in os.listdir(path):

			curr = os.path.join(path, dir)

			if not os.path.isdir(curr):
				continue

			if os.access(curr, os.R_OK):
				r = LaunchpadManager.__locate_launchpad_db(curr)

			if r is not None:
				break
		return r

	def __load_arrangement(self):
		"""
		读取图标排列顺序
		"""

		conn = self.__db_conn

		apps = {}
		groups = {}
		items = {}

		# 读取表 apps
		result = conn.execute("SELECT item_id, title FROM apps")
		for id, title in result:
			apps[id] = title

		# 读取表 groups
		result = conn.execute("SELECT item_id, title FROM groups")
		for id, title in result:
			groups[id] = title

		# 读取表 items
		result = conn.execute("SELECT rowid, uuid, type, parent_id, ordering FROM items")
		for id, uuid, type, parent_id, ordering in result:
			item = LaunchpadItem()
			item.id = id
			item.uuid = uuid
			item.type = type
			item.parent = parent_id
			item.ordering = ordering
			if type == LaunchpadItem.TYPE_GROUP:
				item.title = groups[item.id]
			elif type == LaunchpadItem.TYPE_APP:
				item.title = apps[item.id]
			items[id] = item

		# 建立 APP 节点关系
		for item in items.values():
			if item.type != LaunchpadItem.TYPE_APP:
				item.children = [child for child in items.values() if child.parent == item.id]
				for child in item.children:
					child.parent = item
				item.children.sort(key = lambda x: x.ordering)

		self.__items = items

	@property
	def groups(self) -> dict:
		return {item.id : item for item in self.__items.values() if item.type == LaunchpadItem.TYPE_GROUP}

	@property
	def pages(self) -> dict:
		return {item.id : item for item in self.__items.values() if item.type == LaunchpadItem.TYPE_PAGE}

	@property
	def apps(self) -> dict:
		return {item.id : item for item in self.__items.values() if item.type == LaunchpadItem.TYPE_APP}

	@property
	def root(self) -> LaunchpadItem or None:
		if 1 in self.__items:
			return self.__items[1]
		else:
			return None

	def show_page(self, id):
		"""
		根据 id 展示页面
		"""

		if id not in self.pages:
			return

		page = self.pages[id]
		for i, item in enumerate(page.children):

			id = item.id
			title = item.title
			if item.type == LaunchpadItem.TYPE_GROUP:
				title = "[%s]" % title

			print("|%3s. %-15s\t" % (id, title), end="")
			if (i + 1) % 7 == 0 or i == len(page.children) - 1:
				print()

	def remove_app_icon(self, id) -> bool:
		"""
		根据 id 删除应用
		"""

		if id not in self.apps:
			return False

		conn = self.__db_conn
		cursor = conn.execute("DELETE FROM items WHERE rowid = %s" % id)
		if cursor.rowcount == 0:
			return False

		conn.commit()
		self.reboot()
		self.__load_arrangement()
		return True

	def close(self):
		self.__db_conn.close()
		self.__db_conn = None
		self.__db_file = None
		self.__items = {}

	def reboot(self) -> bool:
		"""
		重启 Launchpad
		@return 操作成功与否
		"""
		return os.system("killall Dock") == 0

	def reset(self) -> bool:
		"""
		重置 Launchpad 的图标排列
		@return 操作成功与否
		"""
		result = True
		result = result and os.system("defaults write com.apple.dock ResetLaunchPad -bool true") == 0
		result = result and os.system("killall Dock") == 0
		return result

	def store(self, backup_file_path) -> bool:
		"""
		保存当前布局至备份文件
		"""
		try:
			shutil.copyfile(self.__db_file, backup_file_path)
			return True
		except:
			return False

	def restore(self, backup_file) -> bool:
		"""
		从指定备份文件恢复布局
		"""
		try:
			dirname = os.path.dirname(self.__db_file)
			os.remove(os.path.join(dirname, "db-shm"))
			os.remove(os.path.join(dirname, "db-wal"))
			shutil.copy(backup_file, self.__db_file)
			self.reboot()
			return True
		except:
			return False


if __name__ == "__main__":
	m = LaunchpadManager()
	print(m.restore("/Users/acat/Desktop/db"))
	m.close()