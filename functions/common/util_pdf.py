# -*- coding: utf-8 -*-

import csv
import os.path
from glob import glob
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

class UtilPdf():
	def __init__(self, ctrl_define):
		self.lst_output_file_type = ctrl_define["csv2img"]["def"]

	def prot(self, id, output_path, input_data={}, input_path=""):
		define = self.lst_output_file_type[id]
		# 入力チェック
		if id == "":
			return [False, "CE-0007", ["PDF-ID"]]
		if output_path == "":
			return [False, "CE-0007", ["PDF出力パス"]]
		if not os.path.isdir(os.path.dirname(output_path)):
			return [False, "CE-0008", [os.path.dirname(output_path)]]
		if input_data != "" and not os.path.isdir(input_path):
			return [False, "CE-0008", [input_data]]
		
		# 入力ファイルチェック
		dict_input_file_path = {}
		for f in define.get("input_file", []):
			l = glob("{0}\\{1}".format(input_path, f.get("file", "")))
			if 1 > len(l):
				return [False, "CE-0009", [f.get("file", "")]]
			elif 1 < len(l):
				return [False, "CE-0010", [f.get("file", "")]]
			else:
				dict_input_file_path[f["id"]] = {
					"path": l[0],
					"delimiter": f.get("delimiter", "\t"),
					"k": f.get("key", "").split(",")
				}
		# 入力ファイル読込
		dict_input_file = {}
		for key in dict_input_file_path.keys():
			f = None
			try:
				f = open(dict_input_file_path[key]["path"], "r")
				dict_input_file[key] = {}
				for record in csv.reader(f, delimiter = dict_input_file_path[key]["delimiter"]):
					dk = []
					for k in dict_input_file_path[key]["k"]:
						dk.append(record[int(k)])
					dk = tuple(dk)
					if not dk in dict_input_file[key].keys():
						dict_input_file[key][dk] = []
					dict_input_file[key][dk].append(record)
			finally:
				f.close()
		
		prots = define.get("prot", [])[0]

		pdf_file = canvas.Canvas(output_path)
		pdf_file.saveState()
		
		# ページサイズ設定
		page_size = (21.0*cm, 29.7*cm)
		if define.get("size", "A4") == "A3":
			page_size = (42.0*cm, 29.7*cm)
		pdf_file.setPageSize(page_size)

		# フォント設定
		font_size = 10
		registerFont(TTFont("ipam", "static/fonts/ipam.ttf"))
		pdf_file.setFont("ipam", font_size)
		
		# テンプレートを取得
		template = define.get("template", "").split(",")
		for file in dict_input_file[prots["file"]].values():
			# テンプレートを描画
			page = 0
			if page <= len(template) and template[page] != "":
				pdf_file.drawImage(
					template[page],
					0.0*cm,
					0.0*cm,
					width=page_size[0],
					height=page_size[1]
				)
			
			dict_input_data = {}
			for record in file:
				for d in prots.get("d", []):
					if record[int(d["key"])] != d["value"]:
						continue
					if not d["id"] in dict_input_data.keys():
						dict_input_data[d["id"]] = []
					dict_input_data[d["id"]].append(record)
			for p in prots["p"]:
				if p["type"] == "data":
					d = ""
					if len(dict_input_data.get(p["data"], [])) > int(p["row"]) and len(dict_input_data.get(p["data"], [])[int(p["row"])]) > int(p["col"]):
						d = dict_input_data[p["data"]][int(p["row"])][int(p["col"])]
						if p.get("push", "") != "":
							d = p["push"] + d
						if p.get("append", "") != "":
							d += p["append"]
					pdf_file.drawString(int(p["x"]), int(p["y"]), d)
				if p["type"] == "array_y":
					y = 0
					for r in dict_input_data.get(p["data"], []):
						d = ""
						if len(r) > int(p["col"]):
							d = r[int(p["col"])]
						pdf_file.drawString(int(p["x"]), int(p["y"])-y, d)
						y += font_size + int(p.get("offset", 0))
				elif p["type"] == "fix":
					pdf_file.drawString(int(p["x"]), int(p["y"]), p["data"])
				elif p["type"] == "page":
					pdf_file.showPage()
					page += 1
					if len(template) > page and template[page] != "":
						pdf_file.drawImage(
							template[page],
							0.0*cm,
							0.0*cm,
							width=page_size[0],
							height=page_size[1]
						)
				elif p["type"] == "color":
					pdf_file.setFillColorRGB(float(p["r"]), float(p["g"]), float(p["b"]))
				elif p["type"] == "line":
					pdf_file.setLineWidth(int(p["width"]))
					pdf_file.line(int(p["x1"]), int(p["y1"]), int(p["x2"]), int(p["y2"]))
				elif p["type"] == "rect":
					pdf_file.rect(int(p["x"]), int(p["y"]), int(p["w"]), int(p["h"]), stroke=int(p["width"]), fill=p["f"]=="1")
				elif p["type"] == "font":
					font_size = int(p["size"])
					pdf_file.setFont("ipam", font_size)
			pdf_file.showPage()
		pdf_file.save()
		
		return [True]
