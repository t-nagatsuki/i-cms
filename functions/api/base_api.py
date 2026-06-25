# -*- coding: utf-8 -*-

class BaseApi():
    def __init__(self):
        """
        コンストラクタ
        """
        self.handler_url = "/"
        self.maintenance_use = False
        self.need_login = True
        self.need_auth = ""

    def get_response(self, handler, args):
        handler.set_http_status(404)
        handler.view_json({
            "message": handler.get_message("CE-0002")
        })

    def post_response(self, handler, args):
        handler.set_http_status(404)
        handler.view_json({
            "message": handler.get_message("CE-0002")
        })

    def put_response(self, handler, args):
        handler.set_http_status(404)
        handler.view_json({
            "message": handler.get_message("CE-0002")
        })

    def patch_response(self, handler, args):
        handler.set_http_status(404)
        handler.view_json({
            "message": handler.get_message("CE-0002")
        })

    def delete_response(self, handler, args):
        handler.set_http_status(404)
        handler.view_json({
            "message": handler.get_message("CE-0002")
        })
