from channels.routing import route
from chats.consumers import ws_connect, ws_disconnect, ws_message, \
    ws_connect_admin

channel_routing = [
    route("websocket.connect", ws_connect_admin,
          path=r"^/api/admin/chats/rooms/(?P<room>[0-9]+)/messages/"),
    route("websocket.connect", ws_connect,
          path=r"^/api/chats/rooms/(?P<room>[0-9]+)/messages/"),

    route("websocket.receive", ws_message,
          path=r"^/api/chats/rooms/(?P<room>[0-9]+)/messages/"),
    route("websocket.receive", ws_message,
          path=r"^/api/admin/chats/rooms/(?P<room>[0-9]+)/messages/"),

    route("websocket.disconnect", ws_disconnect),
]
