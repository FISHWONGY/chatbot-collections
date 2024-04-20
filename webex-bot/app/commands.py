from webex_bot.models.command import Command


class Ping(Command):
    def __init__(self):
        super().__init__(
            command_keyword="!ping",
            help_message="!ping - a simple ping command",
            card=None,
        )

    def execute(self, message, attachment_actions, activity):
        return "pong!"
