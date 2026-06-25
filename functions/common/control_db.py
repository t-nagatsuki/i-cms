# -*- coding: utf-8 -*-

import os
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
			db = self.__apply_env_overrides(db)
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

	def __apply_env_overrides(self, db):
		"""
		環境変数によるDB定義のオーバーライド処理
	
		database.xmlの各DB定義に対して、環境変数が設定されている場合はその値で上書きする。
		環境変数の命名規則: {DB_ID(大文字)}_{属性名(大文字)}
		例: db_control → DB_CONTROL_TYPE, DB_CONTROL_HOST, ...
	
		Parameters
		----------
		db : dict
			DB定義辞書
	
		Returns
		-------
		dict
			環境変数で上書きされたDB定義辞書
		"""
		prefix = db["id"].upper()
		env_map = {
			"db_type":    f"{prefix}_TYPE",
			"db_host":    f"{prefix}_HOST",
			"db_port":    f"{prefix}_PORT",
			"db_user":    f"{prefix}_USER",
			"db_password": f"{prefix}_PASSWORD",
			"db_name":    f"{prefix}_NAME",
			"db_charset": f"{prefix}_CHARSET",
			"db_path":    f"{prefix}_PATH",
			"inmemory":   f"{prefix}_INMEMORY",
		}
		for attr, env_key in env_map.items():
			val = os.environ.get(env_key)
			if val is not None:
				db[attr] = val
		return db
	
	def keys(self):
		return self.ctrl_db.keys()
	
