# -*- coding: utf-8 -*-

class ExceptCommon(Exception):
	def __init__(self, msg_id, param=[]):
		"""
		コンストラクタ

		Parameters
		----------
		msg_id : string
			メッセージID
		param : list, default []
			メッセージパラメータ
		"""
		self.msg_id = msg_id
		self.param = param
