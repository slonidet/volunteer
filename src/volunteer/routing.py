from channels.routing import route
from chats.consumers import ws_connect, ws_disconnect, ws_message

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/?P<room>[a-z0-9]+"),
    route("websocket.receive", ws_message, path=r"^/?P<room>[a-z0-9]+"),
    route("websocket.disconnect", ws_disconnect, path=r"^/?P<room>[a-z0-9]+"),
]
