# -*- coding: utf-8 -*-

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from functions.data.control_base import ControlBase

class ControlTinyDB(ControlBase):
	"""
	TinyDB制御クラス
	"""
	def __init__(self, db_path=None):
		"""
		コンストラクタ

		Parameters
		----------
		db_path : string
			DB保存パス
		"""
		super().__init__()
		if db_path is None:
			self.db = TinyDB(storage = MemoryStorage)
		else:
			self.db = TinyDB(db_path, sort_keys=True)

	def __del__(self):
		"""
		デストラクタ
		"""
		super().__del__()
		self.db.close()
	
	def query(self):
		"""
		クエリオブジェクト生成処理

		Returns
		-------
		Query
			クエリオブジェクト
		"""
		return Query()

	def drop_table(self, tbl_name):
		"""
		テーブル情報破棄処理
		
		Parameters
		----------
		tbl_name : string
			テーブル名
		"""
		self.db.drop_table(tbl_name)

	def drop_tables(self):
		"""
		全テーブル情報破棄処理
		"""
		self.db.drop_tables()

	def all(self, tbl_name):
		"""
		全テーブル情報取得処理
		
		Parameters
		----------
		tbl_name : string
			テーブル名
		"""
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return []
		return self.db.table(tbl_name).all()

	def get(self, tbl_name, where):
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return None
		return self.db.table(tbl_name).get(where)

	def search(self, tbl_name, where=None):
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return []
		if where is None:
			return self.db.table(tbl_name).all()
		else:
			return self.db.table(tbl_name).search(where)

	def insert(self, tbl_name, data):
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return
		self.db.table(tbl_name).insert(data)
	
	def insert_multiple(self, tbl_name, data):
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return
		self.db.table(tbl_name).insert_multiple(data)

	def update(self, tbl_name, dat_update):
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return
		for record in dat_update:
			if self.db.table(tbl_name).search(record["where"]):
				self.db.table(tbl_name).update(record["data"], record["where"])
			else:
				self.db.table(tbl_name).insert(record["data"])

	def delete(self, tbl_name, dat_delete):
		if not tbl_name in self.tables.keys():
			print("指定されたテーブル「{0}」は該当のデータベースに存在しません。".format(tbl_name))
			return
		for record in dat_delete:
			self.db.table(tbl_name).remove(record["where"])

	def escape(self, col_type, val):
		if not col_type in self.text_type:
			return "{0}".format(val)
		return "'{0}'".format(val)
