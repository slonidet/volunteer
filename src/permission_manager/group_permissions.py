PERMISSIONS = {
    'super': [
        {'app_label': 'badges', 'model': 'Badge', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'chats', 'model': 'Room', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'chats', 'model': 'Message', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'events', 'model': 'Event', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'events', 'model': 'Participation', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'gallery', 'model': 'Photo', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'gallery', 'model': 'Album', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'gallery', 'model': 'Video', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'hall_of_fame', 'model': 'HallOfFame', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'interviews', 'model': 'Interviewer', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'interviews', 'model': 'Interview', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'news', 'model': 'News', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'notices', 'model': 'Notice', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Place', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Position', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Shift', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Period', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Day', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'UserPosition', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Team', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'static', 'model': 'Page', 'actions': ('view', 'add', 'change')},
        {'app_label': 'user_tests', 'model': 'Test', 'actions': ('view', 'add', 'change')},
        {'app_label': 'user_tests', 'model': 'Task', 'actions': ('view', 'add', 'change')},
        {'app_label': 'user_tests', 'model': 'Question', 'actions': ('view', 'add', 'change')},
        {'app_label': 'user_tests', 'model': 'AnswerOptions', 'actions': ('view', 'add', 'change')},
        {'app_label': 'user_tests', 'model': 'UserTest', 'actions': ('view', 'add', 'change')},
        {'app_label': 'user_tests', 'model': 'UserAnswer', 'actions': ('view', 'add', 'change')},
        {'app_label': 'users', 'model': 'User', 'actions': ('view', 'add', 'change')},
        {'app_label': 'users', 'model': 'Profile', 'actions': ('view', 'add', 'change')},
        {'app_label': 'users', 'model': 'ProfileAttachment', 'actions': ('view', 'add', 'change')},
        {'app_label': 'users', 'model': 'ProfileComment', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'users', 'model': 'Story', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'users', 'model': 'StoryComment', 'actions': ('view', 'add', 'change', 'delete')},
    ],
    'admin': [
        {'app_label': 'chats', 'model': 'Room', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'chats', 'model': 'Message', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'events', 'model': 'event', 'actions': ('view', 'add', 'change')},
        {'app_label': 'events', 'model': 'participation', 'actions': ('view', 'change')},
        {'app_label': 'gallery', 'model': 'photo', 'actions': ('view', 'add', 'change')},
        {'app_label': 'gallery', 'model': 'album', 'actions': ('view', 'add', 'change')},
        {'app_label': 'gallery', 'model': 'video', 'actions': ('view', 'add', 'change')},
        {'app_label': 'hall_of_fame', 'model': 'HallOfFame', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'interviews', 'model': 'Interviewer', 'actions': ('view', 'add', 'change')},
        {'app_label': 'interviews', 'model': 'Interview', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'news', 'model': 'News', 'actions': ('view', 'add', 'change')},
        {'app_label': 'notices', 'model': 'Notice', 'actions': ('view', 'add', 'change')},
        {'app_label': 'schedules', 'model': 'Place', 'actions': ('view', 'add', 'change')},
        {'app_label': 'schedules', 'model': 'Position', 'actions': ('view', 'add', 'change')},
        {'app_label': 'schedules', 'model': 'Shift', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Period', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Day', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'UserPosition', 'actions': ('view', 'add', 'change', 'delete')},
        {'app_label': 'schedules', 'model': 'Team', 'actions': ('view', 'add', 'change')},
        {'app_label': 'static', 'model': 'Page', 'actions': ('view', 'change')},
        {'app_label': 'user_tests', 'model': 'Test', 'actions': ('view', )},
        {'app_label': 'user_tests', 'model': 'Task', 'actions': ('view', )},
        {'app_label': 'user_tests', 'model': 'Question', 'actions': ('view', )},
        {'app_label': 'user_tests', 'model': 'AnswerOptions', 'actions': ('view', )},
        {'app_label': 'users', 'model': 'User', 'actions': ('view', )},
        {'app_label': 'users', 'model': 'Profile', 'actions': ('view', )},
        {'app_label': 'users', 'model': 'ProfileAttachment', 'actions': ('view', )},
        {'app_label': 'users', 'model': 'ProfileComment', 'actions': ('view', 'add', 'change')},
        {'app_label': 'users', 'model': 'Story', 'actions': ('view', 'change')},
        {'app_label': 'users', 'model': 'StoryComment', 'actions': ('view', 'add', 'change', 'delete')},
    ],
    'senior': [
        {'app_label': 'schedules', 'model': 'Place', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Position', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Shift', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Period', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Day', 'actions': ('view', )},
    ],
    'volunteer': [
        {'app_label': 'schedules', 'model': 'Place', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Position', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Shift', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Period', 'actions': ('view', )},
        {'app_label': 'schedules', 'model': 'Day', 'actions': ('view', )},

    ],
}
