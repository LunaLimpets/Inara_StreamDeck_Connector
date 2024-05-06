import threading #Keybinding
import time #Longpress detection
import requests #Data Retreival
from PIL import Image, ImageDraw, ImageFont #KeyImageGen
from StreamDeck.DeviceManager import DeviceManager #Streamdeck connnection
from StreamDeck.ImageHelpers import PILHelper #KeyImageGen
from bs4 import BeautifulSoup #Data Extraction
from helpers import get_current_system, font_path, get_font_size, center_text, left_align_array_strings, max_font_size, clip, clean, arrow_image_path, config




number_of_rows = config.get("number_of_rows_UNTESTEDBEYONDTHREE")
LONG_PRESS_THRESHOLD = config.get("LONG_PRESS_THRESHOLD")
key_press_times = {}
system = None


# Global variables to track the current page and total number of pages
current_page_raw = 0 # pylint: disable-msg=C0103
current_page_manufactured = 0 # pylint: disable-msg=C0103
current_page_encoded = 0 # pylint: disable-msg=C0103
total_pages_raw = 0 # pylint: disable-msg=C0103
total_pages_manufactured = 0 # pylint: disable-msg=C0103
total_pages_encoded = 0 # pylint: disable-msg=C0103
raw_data = []
manufactured_data = []
encoded_data = []


# Render images
def render_key_image(deck, info):
    # Create a blank image with the same dimensions as a Stream Deck key (72x72 pixels)
    IMAGE_WIDTH = 72
    IMAGE_HEIGHT = 72
    images = []

    background_color = config.get("background_color")
    text_color = config.get("text_color")
    highlight_color = config.get("highlight_color")
    # Create the image for the first key combining station name and key number
    key_image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=background_color)
    draw = ImageDraw.Draw(key_image)
    #Draw the labels
    if info in ['raw', 'manufactured', 'encoded']:
        font_size = get_font_size(draw, info, max_font_size, IMAGE_WIDTH, IMAGE_HEIGHT)
        font = ImageFont.truetype(font_path, font_size)
        x, y = center_text(draw, info, font, IMAGE_WIDTH, IMAGE_HEIGHT)
        draw.text((x, y), info, font=font, fill=config.get("text_color"))

    #Draw the data for the information keys
    else:
        # # Extract vital information
        global system
        station = info.get('station', '')
        system = info.get('system', '')
        distance = info.get('distance', '')
        station_distance = info.get('station_distance', '')
        printables = [system, station,  distance, station_distance]
        fonts, locations = left_align_array_strings(draw, printables, IMAGE_WIDTH, IMAGE_HEIGHT)
        for i, printable in enumerate(printables):
            if i == 0:
                fill = highlight_color
            else:
                fill = text_color
            draw.text(locations[i], printable, font=fonts[i], fill=fill)

    images.append(PILHelper.to_native_key_format(deck, key_image))
    return images

# Function to update the keys for an array
def update_keys_for_data(deck, info, column, row):
    key_images = render_key_image(deck, info)
    for key_image in key_images:
        key = column  + 5 * row
        deck.set_key_image(key, key_image)


def update_keys(deck, data_list, page, row):
    # Update key with information for the current page
    start_index = page
    end_index = page + 3
    for i, data in enumerate(data_list[start_index:end_index]):
        if end_index < len(data_list):  # Check if index is within the bounds of the data_list
            update_keys_for_data(deck, data, i+1, row)

# Function to handle key press events
def key_change_callback(deck, key, state):
    global current_page_raw
    global current_page_manufactured
    global current_page_encoded
    info = False

    if state: # Key pressed
        key_index = key % 5
        key_press_times[key] = time.time()
        #print(key)
        if key == 0:  # prev page raw
            current_page_raw = max(0, current_page_raw - 1)
            update_keys(deck, raw_data, current_page_raw, 0)
        elif key == 4:  # Next Page Raw
            current_page_raw = min(total_pages_raw, current_page_raw + 1)
            update_keys(deck, raw_data, current_page_raw, 0)
        if key == 5:  # prev page manufactured
            current_page_manufactured = max(0, current_page_manufactured - 1)
            update_keys(deck, manufactured_data, current_page_manufactured, 1)
        elif key == 9:  # Next Page manufactured
            current_page_manufactured = min(total_pages_manufactured - 1, current_page_manufactured + 1)
            update_keys(deck, manufactured_data, current_page_manufactured, 1)
        if key == 10:  # prev page encoded
            current_page_encoded = max(0, current_page_encoded - 1)
            update_keys(deck, encoded_data, current_page_encoded, 2)
        elif key == 14:  # Next Page encoded
            current_page_encoded = min(total_pages_encoded - 1, current_page_encoded + 1)
            update_keys(deck, encoded_data, current_page_encoded, 2)
        elif 1<= key <=3:
            info = raw_data[key_index - 1 + current_page_raw * 3]
        elif 6<= key <=8:
            info = manufactured_data[key_index - 1 + current_page_manufactured * 3]
        elif 11<= key <=13:
            info = encoded_data[key_index - 1 + current_page_encoded * 3]
        # Copy system to clipboard when system or station name is pressed
        if info:
            clip(info.get('system', ''))
            #print(info)
            deck.reset()
            deck.close()
    else:  # Key released
        press_duration = time.time() - key_press_times.get(key, 0)
        if press_duration >= LONG_PRESS_THRESHOLD:
            if key == 0:
                current_page_raw = 0
                update_keys(deck, raw_data, current_page_raw, 0)
            elif key == 5:
                current_page_manufactured = 0
                update_keys(deck, manufactured_data, current_page_manufactured, 1)
            elif key == 10:
                current_page_encoded = 0
                update_keys(deck, encoded_data, current_page_encoded, 2)
        key_press_times.pop(key, None)


def get_material_data(): #TODO ADD testing method
    system = get_current_system()
    systemurl = system.replace(" ", "+")
    base_url = config.get("material_traders_url_from_sol")

    url = base_url.replace("Sol", systemurl)
    response =  requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.text #TODO get test data
    else:
        return response.status_code


    # Function to collect and parse the data


def extract_materials_data():
    global total_pages_raw
    global total_pages_manufactured
    global total_pages_encoded

    result = []
    html = get_material_data() #TODO add test html
    soup = BeautifulSoup(html, features="lxml")

    table = soup.find("table")
    rows = table.find_all('tr')
    rows.pop(0)

    for row in rows:
        # print(row.prettify())
        trader_type = row.find('td').text
        # print(trader_type)
        sys_station = row.find_all('a')
        system = sys_station[1].text
        station = sys_station[0].text
        distance = row.find('td', {'class':'alignright minor'}).text
        # print(distance)
        station_distance = row.find('td', {'class':'alignright minor lineright'}).text
        # print(station_distance)

        data = {
            'system': clean(system),
            'station': clean(station),
            'trader_type': clean(trader_type),
            'distance': clean(distance),
            'station_distance':clean(station_distance)
        }
        result.append(data)
        #print(data)



    for station in result:
        material_type = station['trader_type']
        match material_type:
            case 'Manufactured':
                manufactured_data.append(station)
            case 'Encoded':
                encoded_data.append(station)
            case 'Raw':
                raw_data.append(station)
            case _:
                print(f'{station} failed sort')


    total_pages_raw = (len(raw_data) - 1) // 3 + 1
    total_pages_manufactured = (len(manufactured_data) - 1) // 3 + 1
    total_pages_encoded = (len(encoded_data) - 1) // 3 + 1


# Main function
def main():
    extract_materials_data()

    streamdecks = DeviceManager().enumerate()

    #print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for deck in streamdecks:  #TODO add var to select deck
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        # print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
        #     deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        # ))

        deck.set_brightness(config.get("deck_brightness"))

        #Set the label Keys
        for i, trader_type in enumerate(['raw', 'manufactured', 'encoded']):
            update_keys_for_data(deck, trader_type, 0, i)

        # Update keys initially for the first page
        update_keys(deck, raw_data,  0, 0)
        update_keys(deck, manufactured_data,  0, 1)
        update_keys(deck, encoded_data, 0, 2)

        # Set navigation buttons
        for i in [4, 9, 14]:
            deck.set_key_image(
                i, PILHelper.to_native_key_format(
                    deck, Image.open(arrow_image_path).convert('RGB').rotate(270)))

        # Register key press functions
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass
        deck.close()

if __name__ == "__main__":

    main()
