import json

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user

from chats.models import Room, Message
from chats.serializers import MessageSerializer
from users.models import User


@channel_session_user_from_http
def ws_connect(message, room):

    room_object = Room.objects.get(id=room)
    room_users = User.objects.filter(team=room_object.team)

    if message.user in room_users:
        message.reply_channel.send({"accept": True})
        Group('chats-'+room).add(message.reply_channel)
        message.channel_session['room'] = room_object.id
    else:
        message.reply_channel.send({"accept": False})


@channel_session_user_from_http
def ws_connect_admin(message, room):

    if message.user.has_perm(Message):

        room_object = Room.objects.get(id=room)
        message.reply_channel.send({"accept": True})
        Group('chats-'+room).add(message.reply_channel)
        message.channel_session['room'] = room_object.id


@channel_session_user
def ws_message(message, room):
    message_data = json.loads(message['text'])
    room_object = Room.objects.get(id=room)
    chat_message = Message.objects.create(
        room=room_object, text=message_data['text'], sender=message.user)
    serialized_message = MessageSerializer(instance=chat_message)
    Group('chats-'+room).send({'text': json.dumps(serialized_message.data)})


@channel_session_user
def ws_disconnect(message):
    room = message.channel_session['room']
    Group('chats-'+str(room)).discard(message.reply_channel)
