from PIL import Image, ImageDraw, ImageFont


def render_one_character(trzcionka, character, width, height, oversize=4):
    font = ImageFont.truetype(trzcionka, height+oversize)
    PIL_image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(PIL_image)
    draw.text((0, -oversize), character, fill=1, font=font)
    pixels = PIL_image.load()
    hex_values = []
    for y in range(height):
        value = 0
        for x in range(width - 1 , 0, -1):
            value = value | pixels[x, y]
            value = value << 1
        hex_values.append(value)
    return hex_values
   

def render_font(parameters):
    lines = []

    template = """
    static const Font_TypeDef {font_name} = {{
		{width},           // Font width
		{height},          // Font height
		{bytes_per_character},          // Bytes per character
		FONT_H,      // Horizontal font scan lines
		{first_character},          // First character: space
		{last_character},         // Last character: '~'
		{unknown_character},         // Unknown character: '~'
		{{
            {data}
        }}
    }};
    """

    for c in range(parameters["first_character"], parameters["last_character"] + 1):
        char = chr(c)
        hexes = render_one_character(parameters["font"], char, parameters["width"], parameters["height"], parameters["oversize"])

        line = ""
        for h in hexes:
            line += f"{hex(h)},"

        line += f" // {char} ({hex(c)})"
        lines.append(line)
    
    parameters["data"] = "\n".join(lines)

    return template.format(**parameters)


if __name__ == "__main__":

    print(render_font(
        {
            "font_name": "BigFont",
            "width": 8,
            "height": 12,
            "bytes_per_character": 12,
            "first_character": 32,
            "last_character": 126,
            "unknown_character": 126,
            "font": "Ubuntu-C.ttf",
            "oversize": 4
        }
    ))
