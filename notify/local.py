# Include in your local.py

import sys
from datetime import datetime

import pync
from django.conf import settings
from django.core.management.commands.runserver import Command


def check_migrations_with_notification(self):
    """ Show a notification when the server is running. """

    # You can change the parameters as you like
    pync.notify(
        "Running using settings '%s'" % settings.SETTINGS_MODULE,
        title="Django",
        subtitle=datetime.now().strftime('%B %d, %Y - %X'),
        # Any URL for the notification icon
        appIcon='https://i.imgur.com/24eIvxL.jpg',
        # Any "Sound Effects" from OSX's sound system preferences
        sound='Submarine',
        # Identifier of notification, replaces any existing notification
        group=settings.SETTINGS_MODULE,
    )
    # Call original function
    original_check_migrations(self)


# Notification is shown only for `runserver` command
if 'runserver' in sys.argv[1]:
    original_check_migrations = Command.check_migrations
    Command.check_migrations = check_migrations_with_notification
