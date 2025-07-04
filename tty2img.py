from PIL import Image, ImageDraw, ImageFont, ImageColor
import pyte

try:
    import fclist
    import freetype
except ModuleNotFoundError:
    freetype = None

def tty2img(
        screen,
        fgDefaultColor='#00ff00',
        bgDefaultColor='black',
        fontName='DejaVuSansMono.ttf',
        boldFontName='DejaVuSansMono-Bold.ttf',
        italicsFontName='DejaVuSansMono-Oblique.ttf',
        boldItalicsFontName='DejaVuSansMono-BoldOblique.ttf',
        fallbackFonts=['DroidSansFallback', 'Symbola'],
        fontSize=17,
        lineSpace=0,
        marginSize=5,
        antialiasing=0,
        showCursor=False,
        logFunction=None
    ):
    if antialiasing > 1:
        lineSpace = lineSpace * antialiasing
        marginSize = marginSize * antialiasing
        fontSize = fontSize * antialiasing

    normalFont = [ImageFont.truetype(fontName, fontSize), None]
    boldFont = [ImageFont.truetype(boldFontName, fontSize), None]
    italicsFont = [ImageFont.truetype(italicsFontName, fontSize), None]
    boldItalicsFont = [ImageFont.truetype(boldItalicsFontName, fontSize), None]

    if freetype:
        normalFont[1] = freetype.Face(normalFont[0].path)
        boldFont[1] = freetype.Face(boldFont[0].path)
        italicsFont[1] = freetype.Face(italicsFont[0].path)
        boldItalicsFont[1] = freetype.Face(boldItalicsFont[0].path)

    bbox = normalFont[0].getbbox('X')
    charWidth = bbox[2] - bbox[0]
    charHeight = sum(normalFont[0].getmetrics()) + lineSpace
    imgWidth = charWidth * screen.columns + 2 * marginSize
    imgHeight = charHeight * screen.lines + 2 * marginSize

    image = Image.new('RGBA', (imgWidth, imgHeight), bgDefaultColor)
    draw = ImageDraw.Draw(image)

    showCursor = showCursor and (not screen.cursor.hidden)

    for line in screen.buffer:
        point, char, lchar = [marginSize, line * charHeight + marginSize], -1, -1
        for char in sorted(screen.buffer[line].keys()):
            cData = screen.buffer[line][char]

            point[0] += charWidth * (char - lchar - 1)
            lchar = char

            if cData.data == "":
                continue

            bgColor = cData.bg if cData.bg != 'default' else bgDefaultColor
            fgColor = cData.fg if cData.fg != 'default' else fgDefaultColor

            if cData.reverse:
                bgColor, fgColor = fgColor, bgColor

            if showCursor and line == screen.cursor.y and char == screen.cursor.x:
                bgColor, fgColor = fgColor, bgColor

            bgColor = _convertColor(bgColor)
            fgColor = _convertColor(fgColor)

            if bgColor != bgDefaultColor:
                draw.rectangle(((point[0], point[1]), (point[0] + charWidth, point[1] + charHeight)), fill=bgColor)

            if cData.bold and cData.italics:
                font = boldItalicsFont
            elif cData.bold:
                font = boldFont
            elif cData.italics:
                font = italicsFont
            else:
                font = normalFont

            extraWidth = 0
            if freetype and not font[1].get_char_index(cData.data):
                foundFont = False
                for fname in fallbackFonts:
                    for ff in fclist.fclist(family=fname, charset=hex(ord(cData.data))):
                        foundFont = True
                        font = [ImageFont.truetype(ff.file, fontSize), None]
                        bbox = font[0].getbbox(cData.data)
                        extraWidth = max(0, bbox[2] - bbox[0] - charWidth)
                        break
                    if foundFont:
                        break
                else:
                    if logFunction:
                        logFunction("Missing glyph for " + hex(ord(cData.data)) + " Unicode symbols (" + cData.data + ")")

            if cData.underscore:
                draw.line(((point[0], point[1] + charHeight - 1), (point[0] + charWidth, point[1] + charHeight - 1)), fill=fgColor)

            if cData.strikethrough:
                draw.line(((point[0], point[1] + charHeight // 2), (point[0] + charWidth, point[1] + charHeight // 2)), fill=fgColor)

            draw.text(point, cData.data, fill=fgColor, font=font[0])

            point[0] += charWidth + extraWidth

        if showCursor and line == screen.cursor.y and (not screen.cursor.x in screen.buffer[line]):
            point[0] += (screen.cursor.x - char - 1) * charWidth
            draw.rectangle(((point[0], point[1]), (point[0] + charWidth, point[1] + charHeight)), fill=fgDefaultColor)

    if antialiasing > 1:
        return image.resize((imgWidth // antialiasing, imgHeight // antialiasing), Image.ANTIALIAS)
    else:
        return image

def _convertColor(color):
    if color[0] != "#" and not color in ImageColor.colormap:
        return "#" + color
    return color
