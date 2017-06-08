import json

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user

from chats.models import Room, Message
from users.models import User


@channel_session_user_from_http
def ws_connect(message, room):

    user = message.user
    room_object = Room.objects.get(id=room)
    room_users = User.objects.filter(team=room_object.team)

    # if user in room_users:
    message.reply_channel.send({"accept": True})
    Group('chats-'+room).add(message.reply_channel)
    message.channel_session['room'] = room_object.id
    print('connected')
    # else:
    #     message.reply_channel.send({"accept": False})


@channel_session_user
def ws_message(message, room):
    print('message')
    # message_data = json.loads(message['text'])
    room_object = Room.objects.get(id=room)
    chat_message = Message.objects.create(
        room=room_object, text=message.content['text'], sender=message.user)
    print(chat_message)
    Group('chats-'+room).send({'text': message.content['text']})


@channel_session_user
def ws_disconnect(message):
    room = message.channel_session['room']
    Group('chats-'+str(room)).discard(message.reply_channel)
