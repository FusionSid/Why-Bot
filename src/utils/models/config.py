""" (module) classes

A bunch of useful classes to use in the discord bot
"""


class Config:
    """
    A config class for the bot

    Attributes
        join_alert_channel
        leave_alert_channel
        online_alert_channel
        owner_id
    """

    def __init__(self, data):
        self.dm_reply_channel = (
            data["dm_reply_channel"] if data["dm_reply_channel"] is not None else 0
        )

        self.join_alert_channel = (
            data["join_alert_channel"] if data["join_alert_channel"] is not None else 0
        )

        self.leave_alert_channel = (
            data["leave_alert_channel"]
            if data["leave_alert_channel"] is not None
            else 0
        )

        self.online_alert_channel = (
            data["online_alert_channel"]
            if data["online_alert_channel"] is not None
            else 0
        )

        self.suggestion_channel = (
            data["suggestion_channel"] if data["suggestion_channel"] is not None else 0
        )

        self.bug_report_channel = (
            data["bug_report_channel"] if data["bug_report_channel"] is not None else 0
        )
