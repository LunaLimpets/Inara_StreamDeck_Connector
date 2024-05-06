import re  #Extraction
import threading #Keybinding
import time #Longpresses
import sys #CLI arguments
import webbrowser #Opening Link
from bs4 import BeautifulSoup #Data Processing
from PIL import Image, ImageDraw, ImageFont #KeyImageGen
from StreamDeck.DeviceManager import DeviceManager #Streamdeck Connection
from StreamDeck.ImageHelpers import PILHelper #KeyImageGen
import requests #Data Retreival

from helpers import get_current_station, get_current_system, font_path, get_font_size, max_font_size, clip, clean, arrow_image_path, close_image_path, config


MODE = sys.argv[1] if len(sys.argv) > 1 else 'nearest'

# Threshold for considering a press as a long press (in seconds)
LONG_PRESS_THRESHOLD = config.get('LONG_PRESS_THRESHOLD', 1.0)
key_press_times = {}

url = None
current_page = int(0)
trade_data = None
total_pages = int(0)

def extract_pairs(result, pairs, index_one, index_two):
    # print(pairs)
    for item_pair in pairs[index_one:index_two]:
        info = item_pair.find_all('div')
        # print(info[0].text)
        # print(info[1].text)
        # print("=="*8)
        label = clean(info[0].text.strip())
        value = clean(info[1].text.split('|')[0].strip()).split('/', maxsplit=1)[0]

        # print(label, value)
        result[label] = value


def count_items(input_list):
    count = 0
    for item in input_list:
        if isinstance(item, str):  # Count strings as one item
            count += 1
        elif isinstance(item, dict):  # Count each key-value pair as one item
            count += len(item)
        else:
            count += 1  # For other types of items, count as one
    return count


def request_trade_routes(): #TODO ADD TESTING METHODS
    system = get_current_system()
    station = get_current_station()

    systemurl = f'%5B{system.replace(" ", "+")}%5D'
    stationurl = station.replace(" ", "+")

    #print(MODE)
    if MODE == 'nearest':
        url_with_settings = config.get("nearest_trade_routes_url_from__titan_city_sol")
        url = url_with_settings.replace("Titan+City+%5BSol%5D",f"{stationurl}+{systemurl}")
    else:
        url_with_settings = config.get("best_trade_routes_url_from__sol")
        url = url_with_settings.replace("Sol",f"{systemurl[3:-3]}")
    # clip(url)

    response =  requests.get(url, timeout=10)
    print(response.status_code)
    if response.status_code == 200:
        return response.text #TODO get testing data for both modes
    else:
        return response.status_code



def get_trade_routes():
    results = []
    global trade_data
    global total_pages


    #print(response.status_code)
    trade_route_response = request_trade_routes()

    soup = BeautifulSoup(trade_route_response, features="lxml")
    # divs = soup.find_all('div')
    if MODE == 'nearest':
        divs = soup.find_all('div', {'class':"mainblock traderoutebox taggeditem"})
    if MODE == 'best':
        divs = soup.find_all('div', {'class':"mainblock traderoutebox"})
    #print(len(divs))
    try: #TODO update best info extraction
        while len(results) < 15:
            for div in divs:
                # print(div)
                station_one_info = div.text.split("|")
                system_one = re.findall(r'\b\w+(?:\s+\w+)*\b', station_one_info[1][:-2].strip())[0]
                trade_type = re.findall(r'\b(?:To|From)\b', station_one_info[0])
                station_one = re.findall(r'\b\w+(?:\s+\w+)*\b',
                                         station_one_info[0].strip())[0][len(
                                             trade_type[0]):] if trade_type else ''
                if trade_type == 'To':
                    trade_type = "Import"
                else:
                    trade_type = 'Export'
                # print(station_one, system_one, trade_type)

                station_one_data = {
                    'station' : station_one,
                    'system' : system_one,
                    'trade_type' : trade_type,
                }

                item_pairs = div.find_all('div', {'class': 'itempaircontainer'})
                #print('num of items: ', len(item_pairs))
                if len(item_pairs) != 13:
                    trade_type = "round trip"


                station_two_info = div.text.split("|")
                station_two_info = [clean(info.strip()) for info in station_two_info]

                # print(station_two_info)
                station_two = station_two_info[1][len(system_one):].split(" ")[1:]

                if type(station_two) == list:
                    station_two = " ".join(station_two)

                # print('station_two: ', station_two)

                trade_type_two = station_two_info[1][len(system_one):].split(" ")[0]
                # print('trade_type_two', trade_type_two)
                system_two = station_two_info[2].split("S")[0].strip()
                # print(system_two)

                station_two_data = {
                    'station' : station_two,
                    'system' : system_two
                }
                route_data = {}
                # print(station_one_data)

                # print(station_two_data)

                if trade_type == "round trip":
                    # print('round_trip')
                    extract_pairs(station_one_data, item_pairs, 0, 7)
                    extract_pairs(station_two_data, item_pairs, 7, 14)
                    extract_pairs(route_data, item_pairs, 14, -1)
                else:
                    # print('single_trip')
                    extract_pairs(station_one_data, item_pairs, 0, 4)
                    extract_pairs(station_two_data, item_pairs, 4, 8)
                    extract_pairs(route_data, item_pairs, 8, -1)
                # print(station_one_data)

                # print(station_two_data)

                # clip(div)
                profit_per_hour = div.find_all(
                    'div', {'class':"itempairvalue itempairvalueright"})[-1].text
                route_data['profit_per_hour'] = profit_per_hour
                # print('profit_per_hour: ', profit_per_hour)
                # print(station_one_data)
                # print(station_two_data)
                # print(route_data)
                # clip(route_data)

                result = [
                    ["Updated", route_data.get("Updated", '-')],
                    [station_one_data.get("station", '-'), station_one_data.get(
                        "system", '-'), station_one_data.get('Station distance', '-')],
                    [station_two_data.get("station", '-'), station_two_data.get(
                        "system", '-'), station_two_data.get('Station distance', '-')],
                    ["Route Distance", route_data.get('Route distance', '-')],
                    ["UP NAV"],
                    ["Profit Per Hour", route_data.get('profit_per_hour', '-')],
                    ["Buy", station_one_data.get(
                        'Buy', '-'), {"Supply": station_one_data.get('Supply', '-')}],
                    ["Sell", station_two_data.get(
                        'Sell', '-'), {"Demand": station_two_data.get('Demand', '-')}],
                    ["Profit Per Unit", route_data.get('Profit per unit', '-')],
                    ["Cancel"],
                    ['Press to open url'],
                    ["Sell", station_one_data.get(
                        'Sell', '-'), {"Demand": station_one_data.get('Demand', '-')}],
                    ["Buy", station_two_data.get(
                        'Buy', '-'), {"Supply": station_two_data.get('Supply', '-')}],
                    ["Profit Per Trip", route_data.get("Profit per trip", '-')],
                    ["Down Nav"]

                ]
                if result[6] == ['Buy', '-', {'Supply': '-'}]:
                    #print("++"*16)
                    #print(result[6], result[7], result[-4], result[-3])
                    result[6], result[-4] = result[-4], result[6]
                    result[7], result[-3] = result[-3], result[7]
                    result[-4] = ['Buy', '-',{ 'Supply': '-'}]
                    result[-3] = ['Sell', '-',{ 'Demand': '-'}]
                    #print(result[6], result[7], result[-4], result[-3])
                    #print("++"*16)
                #print("**"*10)
                #print(f'adding {MODE} {trade_type}')
                if MODE == "nearest":
                    if trade_type == 'round trip' or trade_type_two == 'To':
                        results.append(result)
                else:
                    results.append(result)
    except IndexError as e:
        print('collection failed')
        print(e)

    # clip(results)
    trade_data = results
    total_pages = len(trade_data)
    return True


def render_key_image(deck, info):  #TODO update to helper method center strings, or fix spacing
    # Info is a list of lists, with the sub-lists containing strings or dictionaries.
    # Create a blank image with the same dimensions as a Stream Deck key (72x72 pixels)
    IMAGE_WIDTH = 72
    IMAGE_HEIGHT = 72
    images = []

    background_color = config.get("background_color")
    text_color = config.get("text_color")
    highlight_color = config.get("highlight_color")
    trade_route_spacing_multiplier = config.get('trade_route_spacing_multiplier')

    # Render each list of items on its own key
    for item_container in info:
        value_image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=background_color)
        draw = ImageDraw.Draw(value_image)
        number_of_items = count_items(item_container)
        placed_items = 0

        # Place each item_container in the list
        for i, printable in enumerate(item_container, 1):
            #place strings on their own line
            if isinstance(printable, str):
                font_size = get_font_size(draw, printable, max_font_size, IMAGE_WIDTH, IMAGE_HEIGHT)
                font = ImageFont.truetype(font_path, font_size)
                _, _, w, h = draw.textbbox((0, 0), printable, font=font)
                placed_items += 1
                x_placement = (IMAGE_WIDTH - font.getbbox(printable)[2]) / 2
                vertical_gap_strings = (
                    IMAGE_HEIGHT - font.getbbox(
                        printable)[3]) / (number_of_items + 1) * trade_route_spacing_multiplier
                y_placement = vertical_gap_strings * placed_items
                if i == 1:
                    draw.text((x_placement, y_placement - 0.5*h),
                              printable, font=font, fill=highlight_color)
                else:
                    draw.text((x_placement, y_placement), printable, font=font, fill=text_color)

            #place dictionaries on the same line
            elif isinstance(printable, dict):
                for key, value in printable.items():
                    placed_items += 1
                    message = f"{key} {value}"
                    font_size = get_font_size(
                        draw, message, max_font_size, IMAGE_WIDTH, IMAGE_HEIGHT)
                    font = ImageFont.truetype(font_path, font_size)
                    _, _, w, h = draw.textbbox((0, 0), message, font=font)

                    x_placement = (IMAGE_WIDTH - w) / 2
                    y_gap = (IMAGE_HEIGHT - font.getbbox(message)[3]) / (
                        number_of_items + 1) * trade_route_spacing_multiplier
                    y_placement = y_gap * placed_items
                    draw.text((x_placement, y_placement), message, font=font, fill=text_color)

        #Save image for troubleshooting
        #value_image.save(f'key_{k}.png')
        images.append(PILHelper.to_native_key_format(deck, value_image))

    return images


# Function to update the keys for an array
def update_keys_for_item_container(deck, info, row):
    # Update key with information
    key_images = render_key_image(deck, info)
    # print(f'placing {len(key_images)}')
    for i, key_image in enumerate(key_images):
        key = i + 5 * (row - 1)
        # print(f'on key {key}')
        if key not in [4, 9, 14]:
            deck.set_key_image(key, key_image)


# Function to update the keys with information from the item_container for the current page
def update_keys(deck, trade_data, page):
    # Update key with information for the current page
    start_index = 0
    end_index = len(trade_data)
    if start_index <= page <= end_index:
        update_keys_for_item_container(deck, trade_data[page][:5], 1)
        update_keys_for_item_container(deck, trade_data[page][5:9], 2)
        update_keys_for_item_container(deck, trade_data[page][10:], 3)


# Function to handle key press events
def key_change_callback(deck, key, state):
    global current_page
    #print(key)
    if state: # Key Pressed
        key_press_times[key] = time.time()
        if key == 9: # select nothing
            deck.close()
        elif key == 4:  # Previous page
            current_page = max(0, current_page - 1)
            update_keys(deck, trade_data, current_page)
        elif key == 14:  # Next page
            current_page = min(total_pages - 1, current_page + 1)
            update_keys(deck, trade_data, current_page)
        elif key == 1 or key == 0:
            clip(trade_data[current_page][1][1])
            deck.reset()
            deck.close()
        elif key == 2:
            #print(trade_data[current_page][2])
            clip(trade_data[current_page][2][1])
            deck.reset()
            deck.close()
        elif key == 10:
            webbrowser.open(url)

    else:  # Key released
        press_duration = time.time() - key_press_times.get(key, 0)
        if press_duration >= LONG_PRESS_THRESHOLD:
            if key == 4:
                current_page = 0
                update_keys(deck, trade_data, current_page)
        key_press_times.pop(key, None)


# Main function
def main():
    get_trade_routes()
    print(f'Got {len(trade_data)} trades')


    streamdecks = DeviceManager().enumerate()

    # print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for deck in streamdecks: #TODO add var to select deck
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        # print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
        #     deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        # ))

        deck.set_brightness(config.get("deck_brightness"))

        # Register key press functions
        deck.set_key_callback(key_change_callback)
        # Set the Initial data keys
        update_keys_for_item_container(deck, trade_data[current_page][:5], 1)
        update_keys_for_item_container(deck, trade_data[current_page][5:9], 2)
        update_keys_for_item_container(deck, trade_data[current_page][10:], 3)

        # Set close and navigation buttons
        deck.set_key_image(9, PILHelper.to_native_key_format(
            deck, Image.open(close_image_path).convert('RGB')))
        deck.set_key_image(4, PILHelper.to_native_key_format(
            deck, Image.open(arrow_image_path).convert('RGB')))
        deck.set_key_image(14, PILHelper.to_native_key_format(
            deck, Image.open(arrow_image_path).convert('RGB').rotate(180)))

        # Wait until all application threads have terminated
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass
        deck.close()

if __name__ == "__main__":
    main()
