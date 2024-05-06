import threading
import time
import webbrowser #Opening Link
from PIL import Image, ImageDraw
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import requests
from bs4 import BeautifulSoup
from helpers import  center_align_strings, clip, clean, arrow_image_path, close_image_path, config, update_image_path
from check_version import check_for_updates


# Global variables
current_page = 0 # pylint: disable-msg=C0103
total_pages = 0 # pylint: disable-msg=C0103
market_data = []
key_press_times = {}
LONG_PRESS_THRESHOLD = config.get('LONG_PRESS_THRESHOLD', 1.0)
IMAGE_WIDTH = 72
IMAGE_HEIGHT = 72
to_update = False

def render_key_image(deck, info):
    # Info is a list of dictionaries

    images = []
    # print(info)

    background_color = config.get("background_color")
    text_color = config.get("text_color")
    highlight_color = config.get("highlight_color")


    # Extract station name and key number
    station_name = info.get('station', '')
    system = info.get('system', '')


    # Create the image for the first key combining station name and key number
    first_image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=background_color)
    draw = ImageDraw.Draw(first_image)

    fonts, locations = center_align_strings(draw, [system, station_name], IMAGE_WIDTH, IMAGE_HEIGHT)
    draw.text(locations[0], system, font=fonts[0], fill=highlight_color)
    draw.text(locations[1], station_name, font=fonts[1], fill=text_color)
    images.append(PILHelper.to_native_key_format(deck, first_image))

    # Render the remaining values on separate images
    for key, value in list(info.items())[2:]:
        value_image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=background_color)
        draw = ImageDraw.Draw(value_image)
        fonts, locations = center_align_strings(
            draw, [str(key), str(value)], IMAGE_WIDTH, IMAGE_HEIGHT)
        draw.text(locations[0], str(key), font=fonts[0], fill=text_color)
        draw.text(locations[1], str(value), font=fonts[1], fill=text_color)
        images.append(PILHelper.to_native_key_format(deck, value_image))

    return images


# Function to update the keys for 3 systems at a time
def update_keys_for_object(deck, info, index):
    # Update key with information
    key_images = render_key_image(deck, info)
    for i, key_image in enumerate(key_images):
        key = i + 5 * index
        deck.set_key_image(key, key_image)


# Function to select the 3 dictionaries to be displayed (One per row of keys)
def update_keys(deck, object_list, page): #TODO? Update for more keys
    start_index = page * 3
    end_index = min((page + 1) * 3, len(object_list))
    for index in range(start_index, end_index):
        info = object_list[index]
        update_keys_for_object(deck, info, index - start_index)


# Function to handle key press events
def key_change_callback(deck, key, state):
    object_list = market_data
    global current_page
    if state:
        if key == 9: # select nothing
            if to_update:
                webbrowser.open(config.get("releases_url"))
            deck.close()
        elif key == 4:  # Previous page
            current_page = max(0, current_page - 1)
            update_keys(deck, object_list, current_page)
        elif key == 14:  # Next page
            current_page = min(total_pages - 1, current_page + 1)
            update_keys(deck, object_list, current_page)
        else:
            # Determine which dictionary in the object_list corresponds to the pressed key
            key_index = key // 5
            object_index = key % 5
            if object_index < len(object_list):
                info = object_list[key_index + current_page * 3]
                # Copy system to clipboard when system or station name is pressed
                clip(info.get('system', ''))
                deck.reset()
                deck.close()
                #TODO? Place a key for navigation/trade instructions
    else:  # Key released
        press_duration = time.time() - key_press_times.get(key, 0)
        if press_duration >= LONG_PRESS_THRESHOLD:
            if key == 4:
                current_page = 0
                update_keys(deck, object_list, current_page)
        key_press_times.pop(key, None)


# Get data from Inara
def request_market_data(): #TODO add testing method
    #Url for Home system / Commodity
    url = config.get("favorite_commodity_from_home_url")
    response =  requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.text #TODO get test data
    else:
        return response.status_code

# Extract the data from HTML response
def extract_market_data():
    global total_pages

    response = request_market_data()
    if type(response) == str:
        soup = BeautifulSoup(response, features="lxml")
        table = soup.find("table")
        rows = table.find_all('tr')
        rows.pop(0)

        for row in rows:
            system = row.find('span', {'class':'uppercase nowrap'}).text
            station = row.find('span', {'class':'standardcase standardcolor nowrap'}).text[:-2]
            tds = row.find_all('td', {'class': 'alignright lineright'})
            demand = tds[0].text
            if len(tds) == 1:
                price = row.find('span',
                                 {'data-tooltiptext':"Observed price range in a short period before the update."})
                price = price.text.split()[0]
            else:
                price = tds[1].text[:-3]
            updated = row.find('td', {'class': 'minor alignright small'}).text[:-4]
            data = {
                'system': system,
                'station': station,
                'demand': clean(demand),
                'price': clean(price),
                'updated': clean(updated)
                    }
            market_data.append(data)
    total_pages = (len(market_data) - 1) // 3 + 1


# Main function
def main():
    global to_update
    to_update = check_for_updates(config)
    extract_market_data()
    streamdecks = DeviceManager().enumerate()

    #print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for deck in streamdecks: #TODO add deck select
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        # print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
        #     deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        # ))

        deck.set_brightness(config.get("deck_brightness"))

        # Update keys initially for the first page
        update_keys(deck, market_data, current_page)

        # Set close and navigation buttons with updated image paths
        deck.set_key_image(9, PILHelper.to_native_key_format(deck,
            Image.open(close_image_path).convert('RGB')))
        deck.set_key_image(4, PILHelper.to_native_key_format(deck,
            Image.open(arrow_image_path).convert('RGB')))
        deck.set_key_image(14, PILHelper.to_native_key_format(deck,
            Image.open(arrow_image_path).convert('RGB').rotate(180)))

        if to_update:
                        deck.set_key_image(
                9, PILHelper.to_native_key_format(
                    deck, Image.open(update_image_path).convert('RGB')))
        


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
