from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGBA", (900, 300), "#24272a")
profile = Image.open("test.png").resize((250, 250))


def round_corners(image: Image.Image):
    background = Image.new("RGBA", size=image.size, color=(255, 255, 255, 0))
    holder = Image.new("RGBA", size=image.size, color=(255, 255, 255, 0))
    mask = Image.new("RGBA", size=image.size, color=(255, 255, 255, 0))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        (2, 2) + (image.size[0] - 2, image.size[1] - 2),
        radius=10,
        fill="black",
    )
    holder.paste(image, (0, 0))
    return Image.composite(holder, background, mask)


img = round_corners(img)

blank = Image.new("RGBA", size=img.size, color=(255, 255, 255, 0))
blank.paste(profile, (25, 25))
img = Image.alpha_composite(img, blank)

draw = ImageDraw.Draw(img)
font = ImageFont.truetype(f"f.ttf", 40)
draw.text((300, 50), "FusionSid#3645", fill="white", font=font, align="center")
font = ImageFont.truetype(f"f.ttf", 35)
draw.text((700, 50), "#1", fill="white", font=font, align="center")


position = (300, 225)
ratio = 600 / 100
to_width = (ratio * 55 + position[0]) / 1.05

height = 40 + position[1]

draw.rounded_rectangle(
    position + (to_width, height),
    fill="#ffffff",
    outline=None,
    width=1,
)

draw.rounded_rectangle(
    (position[0] - 3, position[1] - 3)
    + ((ratio * 100 + position[0] + 3) / 1.05, height + 3),
    outline="#ffffff",
    width=3,
)

img.save("e.png")
# draw.rounded_rectangle(
#     position + (to_width, height),
#     radius=10,
#     fill="#00fa81",
#     outline=outline,
#     width=stroke_width,
# )
