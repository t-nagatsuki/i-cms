# -*- coding: utf-8 -*-

from tornado import escape, template
from tornado.options import options

class BasePage():
    """
    基底画面クラス

    Attributes
    ----------
    handler_url : string
        この画面クラスが処理を行うリクエストURL。
    page_handler : list of string
        この画面クラスが処理を行うリクエストパラメータ「page」のリスト。
    portal_menu : functions.define.menu_define.MenuDefine
        ポータル画面に表示するメニュー設定。
        ※何も表示しない場合はNoneを設定。
    maintenance_use : boolean
        この画面はメンテナンス中にも使用可能か否か。
        True : 可能
        False : 不可能
    need_login : boolean
        この画面の表示はログインが必要か否か。
        True : 必要
        False : 不要
    back_page : string
        need_loginが"True"でログインされていない際に表示する画面の「page」。
    need_auth : string
        この画面の表示に必要な権限名。
    back_page_auth : string
        need_auth"True"で権限を持っていない際に表示する画面の「page」。
    page_dir : string
        templateの基準ディレクトリ。
        ※通常画面であれば"template/main"から先、管理画面であれば"template/admin"から先を指定すること。
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.handler_url = "/"
        self.page_handler = []
        self.portal_menu = None
        self.maintenance_use = False
        self.need_login = True
        self.back_page = "index"
        self.need_auth = ""
        self.back_page_auth = "index"
        self.page_dir = None

    def set_req(self, handler, keys, i):
        prm_req = handler.prm_req
        dict = {}
        for key in keys:
            if "ref" in key[2]:
                val = prm_req.get("{0}_{1}".format(key[0], i), None)
                if key[1] == "text":
                    if val is None:
                        val = ""
                    else:
                        val = escape.xhtml_unescape(val)
                elif key[1] == "int":
                    if val is None or val == "":
                        val = ""
                    else:
                        val = int(val)
                dict[key[0]] = val
            if "up" in key[2]:
                val = prm_req.get("B_{0}_{1}".format(key[0], i), None)
                if key[1] == "text":
                    if val is None:
                        val = ""
                    else:
                        val = escape.xhtml_unescape(val)
                elif key[1] == "int":
                    if val is None or val == "":
                        val = ""
                    else:
                        val = int(val)
                dict["B_{0}".format(key[0])] = val
        return dict

    def get_view(self, handler, args):
        self.view(handler, args)

    def post_view(self, handler, args):
        self.view(handler, args)

    def put_view(self, handler, args):
        self.view(handler, args)

    def patch_view(self, handler, args):
        self.view(handler, args)

    def delete_view(self, handler, args):
        self.view(handler, args)

    def view(self, handler, args):
        lst_obj = []
        if handler.prm_cmn.get("define_page") is not None:
            self.append_obj(handler.prm_cmn["define_page"].get("obj", []), lst_obj)
            t = template.Template("\r\n".join(lst_obj))
            handler.prm_cmn["generate_page"] = t.generate(prm_cmn=handler.prm_cmn, prm_req=handler.prm_req, ctrl_define=handler.ctrl_define)
        base_dir = ""
        if self.page_dir is not None:
            base_dir = "{0}/".format(self.page_dir)
        handler.set_header("content-security-policy", "default-src 'self' 'unsafe-inline' 'unsafe-eval'; base-uri 'self';")
        handler.render(
            "main/{0}{1}.html".format(
                base_dir,
                handler.prm_req.get("page", "index")
            ),
            prm_cmn=handler.prm_cmn,
            prm_req=handler.prm_req,
            ctrl_define=handler.ctrl_define
        )

    def append_obj(self, define, lst_obj):
        for obj in define:
            # 開きタグ
            if obj.get("tag", "") != "":
                tag = []
                tag.append("<{0}".format(obj["tag"]))
                for k in obj.keys():
                    if k in ["tag", "html", "obj"]:
                        continue
                    if obj.get(k, "") != "":
                        tag.append(" {0}=\"{1}\"".format(k, obj[k]))
                    else:
                        tag.append(" {0}".format(k))
                tag.append(">")
                lst_obj.append("".join(tag))
            # innerHTML
            if obj.get("html", "") != "":
                lst_obj.append(obj["html"])
            # 子要素
            self.append_obj(obj.get("obj", []), lst_obj)
            # 閉じタグ
            if obj.get("tag", "") != "":
                lst_obj.append("</{0}>".format(
                    obj["tag"]
                ))
