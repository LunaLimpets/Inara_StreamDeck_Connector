import json
import os
import glob
import re
import sys
from enum import Enum
from unicodedata import normalize
from PIL import ImageFont
import pyperclip

def get_script_dir():
    # Check if running as an executable
    if getattr(sys, 'frozen', False):
        # Running as an executable
        return os.path.dirname(sys.executable)
    else:
        # Running as a script
        return os.path.dirname(os.path.abspath(__file__))

# Get the script directory
script_dir = get_script_dir()

config_file_path = os.path.join(script_dir, "config.json")
arrow_image_path = os.path.join(script_dir, "src/arrow.png")
close_image_path = os.path.join(script_dir, "src/close.png")
update_image_path = os.path.join(script_dir, "src/Update.png")
failed_image_path = os.path.join(script_dir, "src/NoTrades.png")

with open(config_file_path, "r", encoding='utf-8') as config_file:
    config = json.load(config_file)




# Update image paths
font_file = config.get('font_file')
font_path = os.path.join(script_dir, "src", font_file)
print(font_path)
max_font_size = config['max_font_size']

def clip(text):
    pyperclip.copy(str(text))


def clean(input_text):
    out_text = normalize('NFKD', input_text).encode('ascii','ignore')
    final = str(out_text, 'utf-8')
    return final


def center_text(draw, data, font, IMAGE_WIDTH, IMAGE_HEIGHT):
    _, _, w, h = draw.textbbox((0, 0), data, font=font)
    x, y = ((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2)
    return x, y


def get_font_size(draw, text, font_size, max_width, max_height):
    font = ImageFont.truetype(font_path, font_size)
    min_font_size = config.get('min_font_size')
    while draw.textbbox(
        (0, 0), text, font=font
        )[2] > max_width or draw.textbbox((0, 0), text, font=font)[3] > max_height:
        font = ImageFont.truetype(font_path, font_size)
        if font_size == min_font_size:
            break
        font_size -= 1
    return font_size


def left_align_array_strings(draw, printables, IMAGE_WIDTH, IMAGE_HEIGHT):
    # Calculate the y-coordinate for each string to left-align them vertically
    total_items = len(printables)
    min_vertical_margin = config.get('min_vertical_margin')
    left_align_margin = config.get('left_align_margin')
    left_align_font_size = config.get('left_align_font_size')
    left_align_font = ImageFont.truetype(font_path, left_align_font_size)

    locations = []

    fonts = []
    h_s = [draw.textbbox((0, 0), text, font=left_align_font)[3] for text in printables]
    print(printables)
    for i in range(total_items):
        y_placement = (IMAGE_HEIGHT / total_items) * (i + 1) - h_s[i] - min_vertical_margin/2
        locations.append((left_align_margin, y_placement))
        fonts.append(left_align_font)
    return(fonts, locations)


def center_align_strings(draw, printables, IMAGE_WIDTH, IMAGE_HEIGHT):
    # Calculate the y-coordinate for each string to left-align them vertically
    if type(printables) == str:
        printables = [printables]
    total_items = len(printables)
    min_vertical_margin = config.get('min_vertical_margin')
    available_vertical_space = (IMAGE_HEIGHT - min_vertical_margin *2) / total_items
    x_s = []
    heights = []

    fontsizes = []
    fonts = []
    locations = []
    print(printables)
    for printable in printables:
        font_size =  get_font_size(
            draw, printable, max_font_size, IMAGE_WIDTH, available_vertical_space
        )
        fontsizes.append(font_size)
        font = ImageFont.truetype(font_path, font_size)
        fonts.append(font)
        x, _ = center_text(draw, printable, font, IMAGE_WIDTH, IMAGE_HEIGHT)
        x_s.append(x)

        h =  draw.textbbox((0, 0), printable, font=font)[3]
        heights.append(h-min_vertical_margin)

    for i in range(total_items):
        y_placement = (IMAGE_HEIGHT/(total_items+1))* (i + 1) - heights[i]
        x_placement = x_s[i]
        locations.append((x_placement, y_placement))
    return(fonts, locations)


def get_font(draw, text, max_font_size, max_width, max_height):
    font_size = get_font_size(draw, text, max_font_size, max_width, max_height)
    font = ImageFont.truetype(font_path, font_size)
    return font


def get_latest_log_data(): #TODO look into if this works 100%
    logs = config.get("save_game_location") + "*.log"
    # do we need to use https://github.com/MagicMau/EliteJournalReader
    #print(logs)
    list_of_files = glob.glob(logs)
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r', encoding="utf-8") as fp:
        # print(latest_file)
        data = fp.read()
        concat_data = re.sub(r"\}\n\{", "},{", data)
        json_data_as_str = f"[{concat_data}]"
        json_data = json.loads(json_data_as_str)
    return json_data


def get_current_system():
    json_data = get_latest_log_data()
    system = "Sol"
    for event in json_data:
        if 'StarSystem' in event.keys():
            system = event['StarSystem']
        else:
            # print('nothing found')
            pass

    return system


def get_current_station():
    station = "Titan City"
    json_data = get_latest_log_data()
    for event in json_data:
        if 'StationName' in event.keys():
            station = event.get('StationName')
        else:
            # print('nothing found')
            pass
    return station


class TestDataRequestTypes(Enum):
    TRADE_BEST = "trade_best"
    TRADE_EXPORT = "trade_nearest"
    MATERIAL_TRADERS = "materials"
    FAVORITE_COMMODITY = "commodity"


DEBUG_MODE = bool(config.get("debug"))
if DEBUG_MODE:
    from test_data import trade_route_html, trade_route_best_div_0, trade_route_to_keys
    from test_data import material_traders_html, trade_route_best_html
    from test_data import raw_data_to_keys, encoded_data_to_keys, manufactured_data_to_keys
    from test_data import favorite_commodity_html, favorite_commodity_to_keys

    def test_data(test_data_request_type: TestDataRequestTypes):
        match test_data_request_type:
            case TestDataRequestTypes.TRADE_BEST:
                trade_routes = {
                    "response_html" : trade_route_best_html,
                    "div0" : trade_route_best_div_0,
                    "to_keys" : trade_route_to_keys
                }
                return trade_routes
            case TestDataRequestTypes.TRADE_EXPORT:
                trade_routes = {
                    'response_html' : trade_route_html,
                    "to_keys" : trade_route_to_keys               
                }
                return trade_routes
            case TestDataRequestTypes.MATERIAL_TRADERS:
                materials = {
                    'response_html' : material_traders_html,
                    'to_keys' : {
                        "raw" : raw_data_to_keys,
                        "manufactured" : manufactured_data_to_keys,
                        "encoded" : encoded_data_to_keys
                    }
                }
                return materials
            case TestDataRequestTypes.FAVORITE_COMMODITY:
                commodity = {
                    'response_html' : favorite_commodity_html,
                    'to_keys' : favorite_commodity_to_keys
                }
                return commodity
