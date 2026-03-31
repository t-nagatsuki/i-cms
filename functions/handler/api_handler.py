# -*- coding: utf-8 -*-

import json
import traceback
from functions.handler.base_handler import BaseHandler
from functions.common.except_common import ExceptCommon
from tornado.log import app_log
from tornado import web

class ApiHandler(BaseHandler):
    def initialize(self, api, ctrl_define):
        try:
            super().initialize(api, ctrl_define)
            # ログイン状態管理
            self.prm_cmn["account_id"] = self.get_cookie_value("account_id")
            self.prm_cmn["login_token"] = self.get_cookie_value("login_token")
            self.prm_cmn["login"] = False
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            app_log.error(e)
            app_log.error(traceback.format_exc())

    def prepare(self):
        super().prepare()
        try:
            self.prm_body = json.loads(self.request.body)
        except json.JSONDecodeError:
            self.prm_body = {}

    def get(self, *args):
        """
        GETリクエスト処理
        """
        self.proc_access("get", args)

    def post(self, *args):
        """
        POSTリクエスト処理
        """
        self.proc_access("post", args)

    def put(self, *args):
        """
        PUTリクエスト処理
        """
        self.proc_access("put", args)

    def delete(self, *args):
        """
        DELETEリクエスト処理
        """
        self.proc_access("delete", args)

    def proc_access(self, mode, args):
        try:
            if self.is_error:
                self.set_http_status(500, "CE-9999", ["管理者にお問い合わせください。"])
                self.view_json({
                    "error": {
                        "code": "CE-9999",
                        "message": self.get_message("CE-9999", ["管理者にお問い合わせください。"])
                    }
                })
                return
            operation = self.get_operation()
            if len(operation) > 0:
                self.prm_req["page"] = operation[0]["return_operation"]
            key = self.request.path
            for page in self.pages:
                if self.prm_cmn.get("maintenance", "0") == "1" and not page.maintenance_use:
                    if not page.check_login() or not self.prm_cmn.get("admin", False):
                        self.set_http_status(503)
                        self.view_json({
                            "error": {
                                "code": "CE-0004",
                                "message": self.get_message("CE-0004")
                            }
                        })
                        return
                if page.need_login:
                    if not self.check_login():
                        self.set_http_status(401)
                        self.view_json({
                            "error": {
                                "code": "CE-0002",
                                "message": self.get_message("CE-0002")
                            }
                        })
                        return
                    self.append_access_hist()
                if page.need_auth != "" and not self.prm_cmn.get("auth", {}).get(page.need_auth, False):
                    self.set_http_status(401)
                    self.view_json({
                        "error": {
                            "code": "CE-0002",
                            "message": self.get_message("CE-0002")
                        }
                    })
                    return
                if mode == "get":
                    page.get_response(self, args)
                elif mode == "post":
                    page.post_response(self, args)
                elif mode == "put":
                    page.put_response(self, args)
                elif mode == "delete":
                    page.delete_response(self, args)
                return
            self.set_http_status(404, "CE-0006", [key])
            self.view_json({
                "error": {
                    "code": "CE-0006",
                    "message": self.get_message("CE-0006", [key])
                }
            })
        except web.HTTPError as e:
            raise e
        except ExceptCommon as e:
            self.set_http_status(500, e.msg_id, e.param)
            self.view_json({
                "error": {
                    "code": e.msg_id,
                    "message": self.get_message(e.msg_id, e.param)
                }
            })
        except Exception as e:
            self.append_log(self.prm_cmn.get("account_id", "Non Login"), "alert")
            print(e)
            #print(traceback.format_exc())
            self.set_http_status(500, "CE-9999", [str(e)])
            self.view_json({
                "error": {
                    "code": "CE-9999",
                    "message": self.get_message("CE-9999", [str(e)])
                }
            })
