""" (module) classes

A bunch of useful classes to use in the discord bot
"""

class Config():
    """
    A config class for the bot

    Attributes
        join_alert_channel 
        leave_alert_channel 
        online_alert_channel 
        owner_id 
    """
    def __init__(self, data):
        self.dm_reply_channel = data["dm_reply_channel"]
        self.join_alert_channel = data["join_alert_channel"]
        self.leave_alert_channel = data["leave_alert_channel"]
        self.online_alert_channel = data["online_alert_channel"]