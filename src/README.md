# Folder Structure:

```ansi
.
├── README.md
├── cogs/
├── config.yaml
├── core
│   ├── db/
│   ├── helpers/
│   ├── models/
│   └── utils/
├── logfiles/
├── main.py
├── requirements.txt
├── scripts/
└── setup.py
```
---

### cogs/
This folder contains the cogs for the bot. It is full of subfolder for further orginization of the cogs.

---

### config.yaml
This is created after running the setup script and it contains the config for the bot.

---

### core/

This folder contains the rest of the bots code. All code thats not in one of the cog folder will be in here. Its full of useful classes, database functions/setup functions, helpers and utils

#### db/
This folder contains database related functions. Mostly for setting up tables or rows in the db.

#### helpers/
This folder is full of helper code for the bot. Things like checks, exeptions, logging, http and much more

#### models/
This folder is for the classes that help coding easier. 

#### utils/
This folder has utilities to speedup development. Things like calculators and formatters are found here.

---

### logfiles/

This folder wont be there until you run the bot. After running there will be 2 log files in this folder. `main.log` and `discord.log`. The discord log file is created by pycord while running and is reset everytime the bot is run. `main.log` however is created by the program and it contains error logs and debug messages which are caused at runtime.

---

### main.py

This file is a script and is used to start the bot. It handles loading all the cogs and connecting to the discord API.

---

### scripts/

This folder contains scripts.

---

### setup.py

This file is used to setup the bot and the config files. Without running this the bot will NOT work as it is not set up correctly