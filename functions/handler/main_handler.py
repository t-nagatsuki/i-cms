# -*- coding: utf-8 -*-

import traceback
from functions.handler.base_handler import BaseHandler
from tornado.log import app_log

class MainHandler(BaseHandler):
	def initialize(self, pages, ctrl_define):
		try:
			super().initialize(pages, ctrl_define)
			# ログイン状態管理
			self.prm_cmn["account_id"] = self.get_cookie_value("account_id")
			self.prm_cmn["account_password"] = self.get_cookie_value("account_password")
			self.prm_cmn["account_name"] = self.get_cookie_value("account_name")
			self.prm_cmn["login"] = False
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			app_log.error(e)
			app_log.error(traceback.format_exc())
