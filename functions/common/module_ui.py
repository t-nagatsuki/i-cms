# -*- coding: utf-8 -*-

from tornado import web

class CommonHiddenField(web.UIModule):
	def render(self, prm_req={}, param={}, exclude=[]):
		for key in param.keys():
			prm_req[key] = param[key]
		return self.render_string("common/ui/common_hidden_field.html", prm_req=prm_req, param=param, exclude=exclude)

class DataTable(web.UIModule):
	def render(self, data):
		tbl_setting = {
			"tbl_class": []
		}
		# Tableクラス設定
		if data.get("tbl_setting", {}).get("bordered", False):
			tbl_setting["tbl_class"].append("bordered")
		if data.get("tbl_setting", {}).get("striped", False):
			tbl_setting["tbl_class"].append("striped")
		if data.get("tbl_setting", {}).get("responsive_table", False):
			tbl_setting["tbl_class"].append("responsive-table")
		return self.render_string("common/ui/data_table.html", data=data, tbl_setting=tbl_setting)

class ModalWindow(web.UIModule):
	def render(self, id, title=None, messages=[], buttons=[], note=None):
		data = {
			"window_id": id,
			"window_title": title,
			"window_messages": messages,
			"window_buttons": buttons,
			"window_note": note
		}
		return self.render_string(
			"common/ui/modal_window.html", 
			data=data
		)

class InputField(web.UIModule):
	def render(
		self, 
		title, 
		id, 
		key, 
		val, 
		readonly=False, 
		field_type="text", 
		field_step=None, 
		field_id=None, 
		place_holder=None,
		change_view_passward=True,
		max_length=None,
		button_icon=None,
		button_event=None,
		button_tips=None
	):
		data = {
			"input_title": title,
			"input_id": id,
			"input_key": key,
			"input_value": val,
			"place_holder": place_holder,
			"max_length": max_length
		}
		return self.render_string(
			"common/ui/input_field.html", 
			data=data, 
			readonly=readonly, 
			field_type=field_type,
			field_step=field_step,
			field_id=field_id,
			change_view_passward=change_view_passward,
			button_icon=button_icon,
			button_event=button_event,
			button_tips=button_tips
		)

class TextAreaField(web.UIModule):
	def render(
		self, 
		title, 
		id, 
		key, 
		val, 
		readonly=False, 
		field_id=None, 
		max_length=None
	):
		data = {
			"input_title": title,
			"input_id": id,
			"input_key": key,
			"input_value": val,
			"max_length": max_length
		}
		return self.render_string(
			"common/ui/textarea_field.html", 
			data=data, 
			readonly=readonly, 
			field_id=field_id
		)

class CheckField(web.UIModule):
	def render(
		self, 
		title, 
		id, 
		key, 
		val, 
		now_val,
		col_val,
		col_title,
		readonly=False, 
		field_id=None,
		column_num=2
	):
		data = {
			"input_title": title,
			"input_id": id,
			"input_key": key,
			"input_value": val,
			"now_value": now_val
		}
		return self.render_string(
			"common/ui/check_field.html", 
			data=data, 
			col_val=col_val,
			col_title=col_title,
			readonly=readonly, 
			field_id=field_id,
			column_num=column_num
		)

class RadioField(web.UIModule):
	def render(
		self, 
		title, 
		id, 
		key, 
		val, 
		now_val,
		col_val,
		col_title,
		readonly=False, 
		field_id=None
	):
		data = {
			"input_title": title,
			"input_id": id,
			"input_key": key,
			"input_value": val,
			"now_value": now_val
		}
		return self.render_string(
			"common/ui/radio_field.html", 
			data=data, 
			col_val=col_val,
			col_title=col_title,
			readonly=readonly, 
			field_id=field_id
		)

class SelectField(web.UIModule):
	def render(
		self, 
		title, 
		id, 
		key, 
		val, 
		now_val,
		col_val,
		col_title,
		readonly=False, 
		multiple=False,
		field_id=None,
		search=False
	):
		data = {
			"input_title": title,
			"input_id": id,
			"input_key": key,
			"input_value": val,
			"now_value": now_val
		}
		return self.render_string(
			"common/ui/select_field.html", 
			data=data, 
			col_val=col_val,
			col_title=col_title,
			readonly=readonly, 
			multiple=multiple,
			field_id=field_id,
			search=search
		)

class SwitchField(web.UIModule):
	def render(self, title, id, key, val, val_on, val_off, lbl_on, lbl_off, readonly=False, field_id=None, space_col_size=2, title_col_size=2):
		data = {
			"input_title": title,
			"input_id": id,
			"input_key": key,
			"input_value": val,
			"input_value_on": val_on,
			"input_value_off": val_off,
			"input_label_on": lbl_on,
			"input_label_off": lbl_off
		}
		return self.render_string(
			"common/ui/switch_field.html", 
			data=data, 
			readonly=readonly, 
			field_id=field_id,
			space_col_size=space_col_size,
			title_col_size=title_col_size,
			col_size=12-space_col_size*2-title_col_size
		)

class GetInputTypeColor(web.UIModule):
	def render(self, input_type):
		if input_type == -1:
			return "red accent-1"
		elif input_type == 0:
			return "green lighten-4"
		return ""
