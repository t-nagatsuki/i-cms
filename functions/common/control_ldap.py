# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, ALL, NTLM
from tornado.options import options

class ControlLdap():
	"""
	LDAP制御クラス
	"""
	def __init__(self):
		"""
		コンストラクタ
		"""
		self.obj_connect = None
		self.my_data = {
			"user_id": "",
			"user_name": ""
		}
		
	def __del__(self):
		"""
		デストラクタ
		"""
		if self.obj_connect is not None and not self.obj_connect.closed:
			self.obj_connect.unbind()

	def connect(self, domain, user, password):
		"""
		LDAP接続処理
		
		Parameters
		----------
		domain : string
			ドメイン
		user : string
			ログインユーザ
		password : string
			ログインパスワード
		"""
		try:
			self.obj_server = Server(
				"ldap://{0}".format(options.ldap_host), 
				port=options.ldap_port, 
				get_info=ALL
			)
			self.obj_connect = Connection(
				self.obj_server,
				user="{0}\\{1}".format(domain, user),
				password=password,
				authentication=NTLM,
				check_names=True,
				read_only=True,
				auto_bind=True
			)
			list = self.obj_connect.extend.standard.paged_search(
				search_base="cn=users,dc=ht,dc=local",
				search_filter="(&(objectClass=user)(sAMAccountName={0}))".format(user),
				attributes = ["displayName", "description"],
				paged_size = 1,
				generator=True
			)
			for record in list:
				self.my_data["user_id"] = user
				self.my_data["user_name"] = record["attributes"]["displayName"]
			return True
		except:
			return False

	def get_user_name(self):
		"""
		ログインユーザ名取得処理
		"""
		return self.my_data["user_name"]

	def get_user_names(self):
		"""
		LDAP管理ユーザ名一覧取得処理
		"""
		result = {}
		list = self.obj_connect.extend.standard.paged_search(
			search_base="cn=users,dc=ht,dc=local",
			search_filter="(objectClass=user)",
			attributes = ["sAMAccountName", "displayName", "description"],
			paged_size = 1,
			generator=True
		)
		for record in list:
			result[record["attributes"]["sAMAccountName"]] = {
				"user_id": record["attributes"]["sAMAccountName"],
				"user_name": record["attributes"]["displayName"]
			}
		return result
