# -*- coding: utf-8 -*-

import json
import uuid
import traceback
from datetime import datetime
from tornado import websocket, escape, ioloop
from tornado.log import app_log
from collections import OrderedDict
from functions.common.control_db import ControlDB

class SocketHandler(websocket.WebSocketHandler):
	def initialize(self, sockets, ctrl_define):
		self.clients = [];
		self.sockets = sockets
		self.ctrl_define = ctrl_define
		# DB制御
		self.ctrl_db = ControlDB(self.ctrl_define)
		# 汎用パラメータ
		self.prm_cmn = OrderedDict()
		# ログイン情報管理
		self.prm_cmn["account_id"] = self.get_cookie_value("account_id")

	def open(self, *args, **kwargs):
		if self not in self.clients:
			self.clients.append(self)
	
	async def on_message(self, json_message):
		loop = ioloop.IOLoop.current()
		result = await loop.run_in_executor(None, self.async_process, json_message)
		self.write_message(result)

	def async_process(self, json_message):
		try:
			message = json.loads(json_message)
			self.prm_req = message
			key = message.get("mode", None)
			for socket in self.sockets:
				if key in socket.socket_handler:
					result = socket.exec_process(self, message)
					result["mode"] = key
					return result
			result = {
				"mode": key,
				"status": "error",
				"message": ["alert", "実行対象の処理が存在しません。"]
			}
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			result = {
				"mode": key,
				"status": "error",
				"message": self.append_message("CE-9999", [str(e)])
			}
			for m in str(traceback.format_exc()).splitlines():
				self.append_message("", [m], "alert")
		return result

	def on_close(self):
		if self in self.clients:
			self.clients.remove(self)
	
	def append_message(self, msg_cd, msg_prm=[], msg_type=""):
		"""
		メッセージ取得処理
		
		Parameters
		----------
		msg_cd : string
			出力するメッセージID。
		msg_prm : list of string ,default []
			メッセージに埋め込むパラメータ配列。msg_cdが未設定の場合は本パラメータに設定された項目を全て出力。
		msg_type : string, default ""
			出力するメッセージの種別。未設定の場合、メッセージ定義に設定されたメッセージレベルを使用する。
		"""
		if msg_cd != "":
			def_message = self.ctrl_define["message"]["def"].get(msg_cd, {})
			if msg_type == "":
				msg_type = def_message.get("lv", "normal")
			message = "[{0}] {1}".format(msg_cd, def_message.get("text", "メッセージ未定義").format(msg_prm))
			self.append_log(message, msg_type)
			return [msg_type, message]
		else:
			for m in msg_prm:
				self.append_log(m, msg_type)

	def append_log(self, message, msg_type="normal"):
		"""
		APPログ出力処理
		
		Parameters
		----------
		message : string
			出力するログメッセージ。
		msg_type : string, default normal
			ログレベル(alert,warning,normal,debug)。
		"""
		if msg_type == "alert":
			app_log.error(message)
		elif msg_type == "warning":
			app_log.warning(message)
		elif msg_type == "normal":
			app_log.info(message)
		else:
			app_log.debug(message)

	def get_cookie_value(self, key):
		"""
		cookie取得処理
		
		Parameters
		----------
		key : string
			cookieのキー値
		"""
		value = self.get_secure_cookie(key)
		if not value: return None
		return escape.xhtml_escape(value)

	def set_cookie_value(self, key, value):
		"""
		cookie設定処理
		
		Parameters
		----------
		key : string
			cookieのキー値
		value : string
			cookieの設定値
		"""
		self.set_secure_cookie(key, escape.xhtml_escape(value))

	def get_operation_id(self):
		"""
		操作ID取得処理
		"""
		operation_id = uuid.uuid4().hex
		return operation_id

	def get_operation(self):
		"""
		操作履歴取得処理
		"""
		operation_id = self.get_operation_id()
		return self.ctrl_db["db_control"].select("tbl_operation_hist", { "operation_id": operation_id })

	def append_operation(self, op, return_op):
		"""
		操作履歴追加処理
		
		Parameters
		----------
		op : string
			操作名
		return_op : string
			表示操作
		"""
		self.ctrl_db["db_control"].begin()
		operation_id = self.get_operation_id()
		operation_data = {
			"operation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"operation_id": operation_id,
			"account_id": self.prm_cmn["account_id"],
			"operation": op,
			"return_operation": return_op,
			"args": json.dumps(self.prm_req)
		}
		self.ctrl_db["db_control"].insert("tbl_operation_hist", [operation_data])
		self.ctrl_db["db_control"].commit()
