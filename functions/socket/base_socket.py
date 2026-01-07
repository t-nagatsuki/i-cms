# -*- coding: utf-8 -*-

class BaseSocket():
	"""
	基底ソケットクラス
	
	Attributes
	----------
	page_handler : list of string
		このソケットクラスが処理を行うリクエストパラメータ「mode」のリスト。
	"""
	def __init__(self):
		"""
		コンストラクタ
		"""
		self.socket_handler = []
	
	def exec_process(self, handler, message):
		pass
