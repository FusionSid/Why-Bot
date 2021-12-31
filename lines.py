def get_lines():
    lines = 0
    files = ['main.py', 'keep_alive.py', 'add_help.py', 'cogs/Economy.py', 'cogs/Fun.py', 'cogs/Fusion.py', 'Cogs/Google.py', 'cogs/Help.py', "cogs/Minecraft.py", "cogs/Moderation.py", "cogs/Music.py", "cogs/Other.py", "cogs/Reddit.py", "cogs/Slash.py", "cogs/TextConvert.py", "cogs/Ticket.py", "cogs/Utilities.py"]
    for i in files:
        count = 0
        with open(i, 'r') as f:
            for line in f:
                count += 1
        lines += count
    return lines