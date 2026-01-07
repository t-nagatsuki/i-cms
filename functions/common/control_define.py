# -*- coding: utf-8 -*-

from tornado.options import options
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from functions.define.base_define import BaseDefine

class ControlDefine():
	"""
	外部定義制御クラス
	"""
	def __init__(self):
		"""
		コンストラクタ
		"""
		self.db = TinyDB(storage = MemoryStorage)
		self.reload()

	def __del__(self):
		"""
		デストラクタ
		"""
		self.db.close()

	def reload(self):
		"""
		再読込処理
		"""
		self.db.drop_tables()
		def_define = BaseDefine("{0}/define.xml".format(options.define_path)).dict
		for v in def_define.values():
			self.db.insert({
				"id": v["id"],
				"name": v.get("name", "名称未定義"),
				"path": v["path"],
				"def": BaseDefine("{0}/{1}".format(options.define_path, v["path"])).dict
			})

	def __getitem__(self, key):
		"""
		外部定義取得プロパティ
		"""
		que = Query()
		return self.db.get(que.id==key)
