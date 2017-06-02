import json

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user

from chats.models import Room, Message


@channel_session_user_from_http
def ws_connect(message):
    print('connect')
    message.reply_channel.send({"accept": True})
    prefix, label = message['path'].strip('/').split('/')
    room = Room.objects.get(name=label)
    Group('chat-'+label).add(message.reply_channel)
    message.channel_session['room'] = room.name


@channel_session_user
def ws_message(message):
    label = message.channel_session['room']
    room = Room.objects.get(name=label)
    print(message['path'])
    print(type(message.content))
    # chat_message = Message.objects.create(
    #     room=room, message=message.content['text'], user=message.user)
    # Group('chat-'+label).send({'text': message['text']})


@channel_session_user
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('chat-'+label).discard(message.reply_channel)
