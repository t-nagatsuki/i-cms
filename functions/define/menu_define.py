# -*- coding: utf-8 -*-

########################################################################
# モジュールのインポート
########################################################################

class MenuDefine:
	"""
	ポータルメニュー定義クラス
	"""
	def __init__(self, id, title, action, disabe=False, admin=False, auth=None, icon=None, order=-1, t_color="white-text", b_color="light-blue darken-1"):
		"""
		コンストラクタ

		Parameters
		----------
		id : string
			メニューID
		title : string
			メニュー表示名
		action : string
			メニュー遷移アクション名
		disabe : boolean
			活性状態
		admin : boolean
			管理者用メニュー
		auth : string
			メニュー表示権限
		icon : string
			メニューアイコン
		order : int
			メニュー表示順
		t_color : string
			文字列カラー
		b_color : string
			背景カラー
		"""
		self.menu_id = id
		self.menu_title = title
		self.menu_action = action
		self.menu_disable = disabe
		self.menu_admin = admin
		self.menu_auth = auth
		self.menu_icon = icon
		self.menu_order = order
		self.text_color = t_color
		self.back_color = b_color

	def __del__(self):
		"""
		デストラクタ
		"""
		pass
