

def get_valid_value(request):


    import random
    def get_randon_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))



    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    image = Image.new("RGB", (280, 40), get_randon_color())


    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("abbs/static/font/kumo.ttf", size=35)

    keep_valid_codes = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_lower_alf = chr(random.randint(97, 122))
        random_upper_alf = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_lower_alf, random_upper_alf])[0]
        print(random_char, "===")
        draw.text((20 + i * 50, 0), random_char, fill=get_randon_color(), font=font)
        keep_valid_codes += random_char

    width = 280
    height = 40
    ## add zaodian
    # for i in range(1400):
    #     draw.point((random.randint(0,width),random.randint(0,height)),fill=get_randon_color())
    # for i in range(10):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_randon_color())
    # for i in range(40):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_randon_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_randon_color())

    f = BytesIO()
    image.save(f, "png")
    data = f.getvalue()
    print("valid_codes:", keep_valid_codes)

    request.session["keep_valid_codes"] = keep_valid_codes

    return data