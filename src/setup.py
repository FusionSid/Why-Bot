import json


dm_reply_channel = int(input("Enter the ID for the dm_reply_channel"))
join_alert_channel = int(input("Enter the ID for the join_alert_channel"))
leave_alert_channel = int(input("Enter the ID for the leave_alert_channel"))
online_alert_channel = int(input("Enter the ID for the online_alert_channel"))


config = {
    "dm_reply_channel": dm_reply_channel,
    "join_alert_channel": join_alert_channel,
    "leave_alert_channel": leave_alert_channel,
    "online_alert_channel": online_alert_channel,
}


with open("config.json", "w") as f:
    json.dump(config, f, indent=4)


print("Setup Complete :)")
