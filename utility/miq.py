import io
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
import requests
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()

DISCORD_EMOJI_RE = re.compile(r"<(a?):([a-zA-Z0-9_]{1,32}):([0-9]{17,22})>")
UNICODE_EMOJI_RE = re.compile(
    r"[\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9-\u21aa\u231a-\u231b\u2328\u23cf\u23e9-\u23f3\u23f8-\u23fa\u24c2\u25aa-\u25ab\u25b6\u25c0\u25fb-\u25fe\u2600-\u2604\u260e\u2611\u2614-\u2615\u2618\u261d\u2620\u2622-\u2623\u2626\u262a\u262e-\u262f\u2638-\u263a\u2640\u2642\u2648-\u2653\u265f\u2660\u2663\u2665-\u2666\u2668\u267b\u267e-\u267f\u2692-\u2697\u2699\u269b-\u269c\u26a0-\u26a1\u26aa-\u26ab\u26b0-\u26b1\u26bd-\u26be\u26c4-\u26c5\u26c8\u26ce-\u26cf\u26d1\u26d3-\u26d4\u26e9\u26ea\u26f0-\u26f5\u26f7-\u26fa\u26fd\u2702\u2705\u2708-\u270d\u270f\u2712\u2714\u2716\u271d\u2721\u2728\u2733-\u2734\u2744\u2747\u274c\u274e\u2753-\u2755\u2757\u2763-\u2767\u2771-\u2793\u2795-\u2797\u27a1\u27b0\u27bf\u2934-\u2935\u2b05-\u2b07\u2b1b-\u2b1c\u2b50\u2b55\u3030\u303d\u3297\u3299\U00010102\U00010107\U00010183\U00010188\U0001018a\U0001037f\U00010850\U00010857\U0001087f\U00010aa1\U00010ad1\U00010ae6\U00010b39\U00010b3f\U00010b5f\U00010b7f\U00010b99\U00010b9f\U00010ba9\U00010bac\U00010bb9\U00010bbf\U00010bc9\U00010bcf\U00010bd9\U00010bdf\U00010be9\U00010bef\U00010bf9\U00010bff\U00010c39\U00010c3f\U00010c59\U00010c5f\U00010c79\U00010c7f\U00010c99\U00010c9f\U00010ca9\U00010cac\U00010cb9\U00010cbf\U00010cc9\U00010ccf\U00010cd9\U00010cdf\U00010ce9\U00010cef\U00010cf9\U00010cff\U00010d39\U00010d3f\U00010d59\U00010d5f\U00010d79\U00010d7f\U00010d99\U00010d9f\U00010da9\U00010dac\U00010db9\U00010dbf\U00010dc9\U00010dcf\U00010dd9\U00010ddf\U00010de9\U00010def\U00010df9\U00010dff\U0001F004\U0001F0cf\U0001F170-\U0001F171\U0001F17e-\U0001F17f\U0001F18e\U0001F191-\U0001F19a\U0001F201-\U0001F202\U0001F21a\U0001F22f\U0001F232-\U0001F23a\U0001F250-\U0001F251\U0001F300-\U0001F321\U0001F324-\U0001F393\U0001F396-\U0001F397\U0001F399-\U0001F39b\U0001F39e-\U0001F3c1\U0001F3c3-\U0001F3d3\U0001F3d5-\U0001F3f7\U0001F3f8-\U0001F4fd\U0001F4ff-\U0001F53d\U0001F549-\U0001F54e\U0001F550-\U0001F567\U0001F56f\U0001F570\U0001F573-\U0001F57a\U0001F587\U0001F58a-\U0001F58d\U0001F590\U0001F595-\U0001F596\U0001F5a4\U0001F5a8\U0001F5b1\U0001F5b2\U0001F5bd\U0001F5c2-\U0001F5c4\U0001F5d1-\U0001F5d3\U0001F5dc-\U0001F5de\U0001F5e1\U0001F5e3\U0001F5e8\U0001F5ef\U0001F5f3\U0001F5fa-\U0001F64f\U0001F680-\U0001F6c5\U0001F6cb-\U0001F6d2\U0001F6d5-\U0001F6d7\U0001F6dd-\U0001F6df\U0001F6e0-\U0001F6ea\U0001F6f0\U0001F6f3-\U0001F6fc\U0001F700-\U0001F773\U0001F780-\U0001F7d4\U0001F7e0-\U0001F7eb\U0001F7f0\U0001F800-\U0001F80b\U0001F810-\U0001F847\U0001F850-\U0001F859\U0001F860-\U0001F887\U0001F890-\U0001F8ad\U0001F8b0-\U0001F8b1\U0001F8b8-\U0001F8ba\U0001F90d-\U0001F93a\U0001F93c-\U0001F945\U0001F947-\U0001F978\U0001F97a-\U0001F9cb\U0001F9cd-\U0001F9ff\U0001FA70-\U0001FA7c\U0001FA80-\U0001FA88\U0001FA90-\U0001FABd\U0001FAC0-\U0001FAC5\U0001FAd0-\U0001FAd6\U0001Fae0-\U0001Fae8\U0001Faf0-\U0001Faf8]+",
    flags=re.UNICODE,
)
COMBINED_EMOJI_RE = re.compile(
    r"<a?:[a-zA-Z0-9_]{1,32}:[0-9]{17,22}>|" + UNICODE_EMOJI_RE.pattern,
    flags=re.UNICODE | re.DOTALL,
)

def strip_markdown_headers(text):
    return re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

def clean_emoji(text):
    return DISCORD_EMOJI_RE.sub("", text)

def get_clean_text_for_width(text):
    return clean_emoji(text.replace("~~", ""))

def get_text_visual_width(text, font, draw):
    dummy_text = "あHg"
    dummy_bbox = draw.textbbox((0, 0), dummy_text, font=font, anchor="lt")
    font_height = dummy_bbox[3] - dummy_bbox[1]
    
    emoji_size = int(font_height * 0.9)
    width = 0
    last_end = 0
    
    for m in COMBINED_EMOJI_RE.finditer(text):
        part = text[last_end : m.start()]
        width += draw.textlength(part, font=font)
        width += emoji_size
        last_end = m.end()
    
    width += draw.textlength(text[last_end:], font=font)
    return width

def wrap_text(text, font, draw, max_width, use_word_wrap):
    lines = []
    FORBIDDEN_START = ("。", "、", "？", "！", "!", "?", ")", "」", "』", "”", "）")

    for raw_line in text.split("\n"):
        process_tokens = []
        last_end = 0
        
        for m in COMBINED_EMOJI_RE.finditer(raw_line):
            text_part = raw_line[last_end:m.start()]
            if text_part:
                if use_word_wrap:
                    for t in tokenizer.tokenize(text_part):
                        process_tokens.append({'type': 'text', 'content': t.surface})
                else:
                    for char in text_part:
                        process_tokens.append({'type': 'text', 'content': char})
            process_tokens.append({'type': 'emoji', 'content': m.group(0)})
            last_end = m.end()
        
        if last_end < len(raw_line):
            text_part = raw_line[last_end:]
            if use_word_wrap:
                for t in tokenizer.tokenize(text_part):
                    process_tokens.append({'type': 'text', 'content': t.surface})
            else:
                for char in text_part:
                    process_tokens.append({'type': 'text', 'content': char})

        current_line = ""
        current_width = 0
        font_height = font.size
        emoji_size = int(font_height * 0.9)

        for token in process_tokens:
            content = token['content']
            token_width = emoji_size if token['type'] == 'emoji' else draw.textlength(content, font=font)
            
            if content in FORBIDDEN_START and current_line == "" and len(lines) > 0:
                lines[-1] += content
                continue 

            if current_width + token_width <= max_width:
                current_line += content
                current_width += token_width
            else:
                if current_line:
                    lines.append(current_line)
                current_line = content
                current_width = token_width
        
        if current_line:
            lines.append(current_line)
    return lines

def draw_text_with_strikethrough_and_emojis(img, draw, position, text, font, fill, is_active=False):
    x, y = position
    cursor_x = x
    current_active = is_active
    
    parts = re.split(r"(~~)", text)
    
    for part in parts:
        if part == "~~":
            current_active = not current_active
            continue
        if not part:
            continue
            
        cursor_x = draw_text_with_emojis(
            img, draw, (cursor_x, y), part, font, fill, strikethrough=current_active
        )
            
    return current_active

def draw_text_with_emojis(img, draw, position, text, font, fill, strikethrough=False):
    x, y = position
    cursor_x = x
    last_end = 0

    dummy_text = "あHg"
    dummy_bbox = draw.textbbox((0, 0), dummy_text, font=font, anchor="lt")
    font_height = dummy_bbox[3] - dummy_bbox[1]
    
    line_y = y + (font_height // 2)

    def draw_strikethrough(start_x, end_x):
        if strikethrough:
            draw.line([(start_x, line_y), (end_x, line_y)], fill=fill, width=2)

    for m in COMBINED_EMOJI_RE.finditer(text):
        if m.start() > last_end:
            part = text[last_end : m.start()]
            if part:
                draw.text((cursor_x, line_y), part, font=font, fill=fill, anchor="lm")
                w = draw.textlength(part, font=font) 
                draw_strikethrough(cursor_x, cursor_x + w)
                cursor_x += w

        token = m.group(0)
        emoji_url = None
        
        if token.startswith("<"):
            parts = token.strip("<>").split(":")
            if len(parts) >= 3:
                emoji_url = f"https://cdn.discordapp.com/emojis/{parts[2]}.png"
        else:
            emoji_url = f"https://emojicdn.elk.sh/{token.strip()}"

        if emoji_url:
            try:
                resp = requests.get(emoji_url, timeout=3)
                if resp.status_code == 200:
                    with io.BytesIO(resp.content) as i:
                        emoji_img = Image.open(i).convert("RGBA")
                    
                    emoji_size = int(font_height * 0.9)
                    emoji_img = emoji_img.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)

                    y_offset = line_y - (emoji_size // 2)
                    img.paste(emoji_img, (int(cursor_x), int(y_offset)), emoji_img)
                    
                    draw_strikethrough(cursor_x, cursor_x + emoji_size)
                    cursor_x += emoji_size
                    last_end = m.end()
                    continue
            except Exception:
                pass

        draw.text((cursor_x, line_y), token, font=font, fill=fill, anchor="lm")
        bbox = draw.textbbox((cursor_x, line_y), token, font=font, anchor="lm")
        w = bbox[2] - bbox[0]
        draw_strikethrough(cursor_x, cursor_x + emoji_size)
        cursor_x += emoji_size
        last_end = m.end()

    if last_end < len(text):
        tail = text[last_end:]
        if tail:
            draw.text((cursor_x, line_y), tail, font=font, fill=fill, anchor="lm")
            w = draw.textlength(tail, font=font)
            draw_strikethrough(cursor_x, cursor_x + w)
            cursor_x += w

    return cursor_x

def get_best_fit_font(text, draw, max_width, max_height, font_path, use_word_wrap):
    for size in range(32, 14, -2): 
        font = ImageFont.truetype(font_path, size)
        lines = wrap_text(text, font, draw, max_width, use_word_wrap)
        line_height = size + 8
        if len(lines) * line_height <= max_height:
            return font, lines, line_height
    font = ImageFont.truetype(font_path, 16)
    return font, wrap_text(text, font, draw, max_width, use_word_wrap), 24

def create_quote_image(
    author,
    text,
    avatar_bytes,
    background,
    textcolor,
    color: bool,
    negapoji: bool = False,
    fake: bool = False,
    right_gradient: bool = False,
):
    width, height = 800, 400
    background_color = background
    text_color = textcolor

    img = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    avatar_bytes = io.BytesIO(avatar_bytes)
    avatar_size = (400, 400)
    avatar = Image.open(avatar_bytes).convert("RGBA")
    avatar = avatar.resize(avatar_size)
    avatar_bytes.close()

    gradient_mask = Image.new("L", avatar_size, 255)
    half_width = avatar_size[0] // 2
    for x in range(avatar_size[0]):
        alpha = 255
        if right_gradient:
            if x >= half_width:
                rel_x = x - half_width
                alpha = int(255 * (1 - (rel_x / half_width)))
        else:
            alpha = int(255 * (1 - (x / avatar_size[0])))
        for y in range(avatar_size[1]):
            gradient_mask.putpixel((x, y), alpha)
    
    slant_mask = Image.new("L", avatar_size, 255)
    draw_slant = ImageDraw.Draw(slant_mask)
    
    poly_points = [(320, 0), (400, 0), (400, 400), (360, 400)]
    draw_slant.polygon(poly_points, fill=0)
    
    combined_mask = ImageChops.multiply(gradient_mask, slant_mask)
    
    avatar.putalpha(combined_mask)
    img.paste(avatar, (0, height - avatar_size[1]), avatar)

    text_x = 420
    max_text_width = width - text_x - 50
    max_text_height = height - 80

    text = strip_markdown_headers(text)

    font, lines, line_height = get_best_fit_font(text, draw, max_text_width, max_text_height, "data/DiscordFont.ttf", True)
    
    try:
        name_font = ImageFont.truetype("data/DiscordFont.ttf", max(14, font.size - 8))
        logo_font = ImageFont.truetype("data/DiscordFont.ttf", 20)
    except:
        name_font = ImageFont.truetype("data/DiscordFont.ttf", max(14, font.size - 8))
        logo_font = ImageFont.load_default()

    text_block_height = len(lines) * line_height
    text_y = (height - text_block_height) // 2

    strikethrough_active = False

    for i, line in enumerate(lines):
        clean_line = line.replace("~~", "")
        line_width = get_text_visual_width(clean_line, font, draw)
        line_x = text_x + (max_text_width - line_width) // 2
        
        strikethrough_active = draw_text_with_strikethrough_and_emojis(
            img, draw, (line_x, text_y + i * line_height), 
            line, font, textcolor, is_active=strikethrough_active
        )

    author_text = author
    bbox = draw.textbbox((0, 0), author_text, font=name_font)
    author_width = bbox[2] - bbox[0]
    author_x = (width + text_x - 50 - author_width) // 2
    author_y = text_y + len(lines) * line_height + 10
    draw.text((author_x, author_y), author_text, font=name_font, fill=text_color)

    if fake:
        draw.text((580, 0), "FakeQuote - SharkBot", font=logo_font, fill=text_color)
    else:
        draw.text((700, 0), "SharkBot", font=logo_font, fill=text_color)

    if negapoji:
        return ImageOps.invert(img.convert("RGB"))

    return img if color else img.convert("L")