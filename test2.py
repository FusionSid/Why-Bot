from easy_pil import Canvas, Editor, Font, Text, font

LEVELS_AND_XP = {
    '0': 0,
    '1': 100,
    '2': 255,
    '3': 475,
    '4': 770,
    '5': 1150,
    '6': 1625,
    '7': 2205,
    '8': 2900,
    '9': 3720,
    '10': 4675,
    '11': 5775,
    '12': 7030,
    '13': 8450,
    '14': 10045,
    '15': 11825,
    '16': 13800,
    '17': 15980,
    '18': 18375,
    '19': 20995,
    '20': 23850,
    '21': 26950,
    '22': 30305,
    '23': 33925,
    '24': 37820,
    '25': 42000,
    '26': 46475,
    '27': 51255,
    '28': 56350,
    '29': 61770,
    '30': 67525,
    '31': 73625,
    '32': 80080,
    '33': 86900,
    '34': 94095,
    '35': 101675,
    '36': 109650,
    '37': 118030,
    '38': 126825,
    '39': 136045,
    '40': 145700,
    '41': 155800,
    '42': 166355,
    '43': 177375,
    '44': 188870,
    '45': 200850,
    '46': 213325,
    '47': 226305,
    '48': 239800,
    '49': 253820,
    '50': 268375,
    '51': 283475,
    '52': 299130,
    '53': 315350,
    '54': 332145,
    '55': 349525,
    '56': 367500,
    '57': 386080,
    '58': 405275,
    '59': 425095,
    '60': 445550,
    '61': 466650,
    '62': 488405,
    '63': 510825,
    '64': 533920,
    '65': 557700,
    '66': 582175,
    '67': 607355,
    '68': 633250,
    '69': 659870,
    '70': 687225,
    '71': 715325,
    '72': 744180,
    '73': 773800,
    '74': 804195,
    '75': 835375,
    '76': 867350,
    '77': 900130,
    '78': 933725,
    '79': 968145,
    '80': 1003400,
    '81': 1039500,
    '82': 1076455,
    '83': 1114275,
    '84': 1152970,
    '85': 1192550,
    '86': 1233025,
    '87': 1274405,
    '88': 1316700,
    '89': 1359920,
    '90': 1404075,
    '91': 1449175,
    '92': 1495230,
    '93': 1542250,
    '94': 1590245,
    '95': 1639225,
    '96': 1689200,
    '97': 1740180,
    '98': 1792175,
    '99': 1845195,
    '100': 1899250
}



user_name = "FusionSid"
xp = 1161
level = 5
level_xp = LEVELS_AND_XP[f'{level}']
next_level_up = LEVELS_AND_XP[f'{level+1}']
p1 = next_level_up - level_xp # amount needed to get from a - b
p2 = next_level_up - xp
p3 = p1 - p2

print(user_name, xp, level, level_xp, next_level_up, p1, p2, p3)

background = Editor(Canvas((900, 300), color="#23272A"))
profile = Editor("shopimages/goose.png").resize((150, 150)).circle_image()

# For profile to use users profile picture load it from url using the load_image/load_image_async function
# profile_image = load_image(str(ctx.author.avatar_url))
# profile = Editor(profile_image).resize((150, 150)).circle_image()

poppins = Font.poppins(size=40)
poppins_small = Font.poppins(size=30)

card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

background.polygon(card_right_shape, "#2C2F33")
background.paste(profile, (30, 30))

background.rectangle((30, 220), width=650, height=40, fill="#494b4f", radius=20)
background.bar(
    (30, 220),
    max_width=650,
    height=40,
    percentage=user_data["percentage"],
    fill="#3db374",
    radius=20,
)
background.text((200, 40), user_data["name"], font=poppins, color="white")

background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
background.text(
    (200, 130),
    f"Level : {user_data['level']} "
    + f" XP : {user_data['xp']}",
    font=poppins_small,
    color="white",
)


background.show()