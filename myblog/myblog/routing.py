#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: routing.py
# @Time: 2020-06-01 15:58
# @Email: winston.wz.he@gmail.com
# @Desc:
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})