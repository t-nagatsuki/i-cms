# -*- coding: utf-8 -*-

from glob import glob
from tornado.options import options
from functions.define.base_define import BaseDefine
from functions.data.control_tinydb import ControlTinyDB
from functions.data.control_sqlite import ControlSqlite
try:
        from functions.data.control_mysql import ControlMysql
except:
        pass

class ControlDB():
	"""
	DB制御クラス
	"""
	def __init__(self, ctrl_define):
		"""
		コンストラクタ
		
		Parameters
		----------
		ctrl_define : functions.define.base_define.BaseDefine
			外部定義制御クラス
		"""
		self.ctrl_db = {}
		def_db = ctrl_define["database"]["def"]
		for db in def_db.values():
			if db["db_type"] == "tinydb":
				if db.get("inmemory", "0") == "1":
					self.ctrl_db[db["id"]] = ControlTinyDB(None)
				else:
					self.ctrl_db[db["id"]] = ControlTinyDB(db["db_path"])
			elif db["db_type"] == "mysql":
				self.ctrl_db[db["id"]] = ControlMysql(
					db["db_host"],
					int(db.get("db_port", "3306")),
					db["db_user"], 
					db["db_password"], 
					db["db_name"],
					db["db_charset"]
				)
			elif db["db_type"] == "sqlite":
				if db.get("inmemory", "0") == "1":
					self.ctrl_db[db["id"]] = ControlSqlite()
				else:
					self.ctrl_db[db["id"]] = ControlSqlite(db["db_path"])
		
		for path in glob("{0}/tables/*.xml".format(options.define_path)):
			def_tbl = BaseDefine(path).dict
			for tbl in def_tbl.values():
				if not tbl["db"] in self.ctrl_db.keys():
					print("{0}はデータベース定義に存在していません。".format(tbl["db"]))
					continue
				self.ctrl_db[tbl["db"]].tables[tbl["id"]] = tbl

	def __del__(self):
		"""
		デストラクタ
		"""
		for db in self.ctrl_db.values():
			del db

	def __getitem__(self, key):
		"""
		DB取得プロパティ
		"""
		return self.ctrl_db.get(key, None)
