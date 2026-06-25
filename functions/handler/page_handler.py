# -*- coding: utf-8 -*-

import traceback
from collections import OrderedDict
from functions.handler.base_handler import BaseHandler
from functions.common.except_common import ExceptCommon
from tornado.log import app_log
from tornado import web

class PageHandler(BaseHandler):
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
			
	def prepare(self):
		super().prepare()
		self.prm_cmn["color_role"] = {}
		self.prm_cmn["message"] = OrderedDict()
		self.prm_cmn["lst_breadcrumb"] = []
		for lv in self.ctrl_define["message_lv"]["def"].keys():
			self.prm_cmn["color_role"][lv] = self.ctrl_define["message_lv"]["def"][lv].get("value", "")
			self.prm_cmn["message"][lv] = []

	def proc_access(self, mode, args):
		try:
			if self.is_error:
				self.render("base.html", prm_cmn=self.prm_cmn)
				return
			operation = self.get_operation()
			if len(operation) > 0:
				self.prm_req["page"] = operation[0]["return_operation"]
			key = self.prm_get.get("page", None)
			if key is None:
				key = self.prm_req.get("page", "index")
			for page in self.pages:
				if key in page.page_handler:
					if self.prm_cmn.get("maintenance", "0") == "1" and not page.maintenance_use:
						if not page.check_login() or not self.prm_cmn.get("admin", False):
							self.render("common/maintenance.html", prm_cmn=self.prm_cmn, prm_req=self.prm_req)
							return
					if page.need_login:
						if not self.check_login():
							self.append_message("CE-0003", [key])
							self.prm_req["page"] = page.back_page
							self.proc_page(mode)
							return
						self.append_access_hist()
					if page.need_auth != "" and not page.need_auth in self.prm_cmn["account_auth"]:
						self.append_message("CE-0005", [key])
						self.prm_req["page"] = page.back_page_auth
						self.proc_page(mode)
						return
					if mode == "get":
						page.get_view(self, args)
					elif mode == "post":
						page.post_view(self, args)
					elif mode == "put":
						page.put_view(self, args)
					elif mode == "pacth":
						page.patch_view(self, args)
					elif mode == "delete":
						page.delete_view(self, args)
					return
			self.append_message("CE-0006", [key])
			self.render("common/error.html", prm_cmn=self.prm_cmn, prm_req=self.prm_req)
		except web.HTTPError as e:
			raise e
		except ExceptCommon as e:
			self.append_message(e.msg_id, e.param)
			self.render("base.html", prm_cmn=self.prm_cmn)
		except Exception as e:
			self.append_log(self.prm_cmn.get("account_id", "Non Login"), "alert")
			print(e)
			#print(traceback.format_exc())
			self.append_message("CE-9999", [str(e)])
			for m in str(traceback.format_exc()).splitlines():
				self.append_message("", [m], "alert")
			self.render("base.html", prm_cmn=self.prm_cmn)

	def add_breadcrumb(self, title, link=None, icon=None, param={}):
		self.prm_cmn["lst_breadcrumb"].append({
			"link": link,
			"icon": icon,
			"title": title,
			"param": param
		})

	def alert_message(self, msg_cd, msg_prm=[]):
		"""
		画面メッセージ出力処理(Alert)

		Parameters
		----------
		msg_cd : string
			出力するメッセージID。
		msg_prm : list of string ,default []
			メッセージに埋め込むパラメータ配列。
		"""
		self.append_message(msg_cd, msg_prm, "alert")

	def warning_message(self, msg_cd, msg_prm=[]):
		"""
		画面メッセージ出力処理(Warning)

		Parameters
		----------
		msg_cd : string
			出力するメッセージID。
		msg_prm : list of string ,default []
			メッセージに埋め込むパラメータ配列。
		"""
		self.append_message(msg_cd, msg_prm, "warning")

	def normal_message(self, msg_cd, msg_prm=[]):
		"""
		画面メッセージ出力処理(Normal)

		Parameters
		----------
		msg_cd : string
			出力するメッセージID。
		msg_prm : list of string ,default []
			メッセージに埋め込むパラメータ配列。
		"""
		self.append_message(msg_cd, msg_prm, "normal")

	def append_message(self, msg_cd, msg_prm=[], msg_type=""):
		"""
		画面メッセージ出力処理

		Parameters
		----------
		msg_cd : string
			出力するメッセージID。
		msg_prm : list of string ,default []
			メッセージに埋め込むパラメータ配列。msg_cdが未設定の場合は本パラメータに設定された項目を全て出力。
		msg_type : string, default ""
			出力するメッセージの種別。未設定の場合、メッセージ定義に設定されたメッセージレベルを使用する。
		"""
		if not msg_type in self.prm_cmn["message"].keys():
			self.prm_cmn["color_role"][msg_type] = ""
			self.prm_cmn["message"][msg_type] = []
		if msg_cd != "":
			def_message = self.ctrl_define["message"]["def"].get(msg_cd, {})
			if msg_type == "":
				msg_type = def_message.get("lv", "normal")
			message = "[{0}] {1}".format(msg_cd, def_message.get("text", "メッセージ未定義").format(msg_prm))
			self.prm_cmn["message"][msg_type].append(message)
			self.append_log(message, msg_type)
			return message
		else:
			for m in msg_prm:
				self.prm_cmn["message"][msg_type].append(m)
				self.append_log(m, msg_type)
		return "\n".join(self.prm_cmn["message"][msg_type])

