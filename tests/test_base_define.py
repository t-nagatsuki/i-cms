#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from functions.define.base_define import BaseDefine

if __name__ == "__main__":
	def_define = BaseDefine("data/test.xml")
	def_define.save_xml("output.xml", True)

