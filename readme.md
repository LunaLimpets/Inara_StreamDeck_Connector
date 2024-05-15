
## Features
- Request and display data from Inara.cz on your Stream Deck

- Get the Highest Price Exports for the station you are in.
- Find Material Traders nearest to the system you are in.
- Find A commodity price Nearby your home station.
- WIP Support for "Best" Trade routes.
- Without opening a browser, the target systems are copied to the clipboard, with the press of a button.
- Customizable Fonts, Colors
- New Release Notifications




## Instructions
You can either use the exe files in the releases, or run the python files directly if you want to tinker.
# Exe files:
1. Download InaraStreamDeck.Zip from the  [releases tab](https://github.com/LunaLimpets/Inara_StreamDeck_Connector/releases) tab
2. Extract to a folder of you choosing.
3. [Go to Configuration](#config)


# HID Backend 
Follow the instructions for your operating system [here](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html).

# Python Files 

1. **Download**: 
    - Download from the [releases tab](https://github.com/LunaLimpets/Inara_StreamDeck_Connector/releases), or clone the repository
   
2. **Download and Install Python**:
    - [Python Download](https://www.python.org/downloads/)
    - Tested on Python 3.11.5
    - Check the box that says "Add Python x.x to PATH"
   
3. **Verify Python Installation**:
    - Open a command prompt (on Windows) or terminal (on macOS/Linux).
    - Type `python --version` and press Enter.

4. **Navigate to Project Directory**:
    - Open your CMD prompt and Navigate to the project directory.
   
5. **Install project requirements from requirements.txt**:
    ```
    pip install -r requirements.txt
    ```


<a name="config"></a>
## Config.json Update

- **Elite Savegamefolder Location**

     Update the path in config.json.

     Typically Located in : "C:/Users/username/Saved Games/Frontier Developments/Elite Dangerous/"


- **URL Updates**

     Use Inara's UI to customize trade settings such as distances, sorting types, landing pads, etc.
     
     Ensure to search before copying. 
     
     Note that "Sol" in material traders and trade routes is programmatically replaced with the current system from logs.
     
     Support for setting your home system's favorite commodity.

   
## Setting up the Stream Deck

Currently, there are four functions:

- **favorite_commodity** 
- **material_traders**
- **trade_routes nearest**
- **trade_routes best** (WIP)

I recommend creating two profiles:

- "ED Material Select"
- "ED Trade Routes"

You can name them as you prefer. In these profiles:

- Add a Navigation:switch profile button with a black background.
- Set the profile target to wherever you will be calling the functions from (e.g., Elite Dangerous page 2).
- Copy the button to every space except the top right and bottom right buttons. The Material select function uses the middle right button as well.
- Optionally, add a "Loading" title to one of your buttons.


**Adding the functions**:

In your Elite Dangerous profile or wherever you want to call these functions from:

- Create a multi-action button. 
    - The first action should be "Navigation:Switch Profile" (Target is either "ED Material Select" or "ED Trade Routes"). 
    - The second action should be "System Open" your chosen script out of the following:

        If you chose the exe files
        ```
        "C:\Your\Path\to\ProjectFolder\favorite_commodity.exe"
        "C:\Your\Path\to\ProjectFolder\material_traders.exe"
        "C:\Your\Path\to\ProjectFolder\trade_routes.exe" nearest
        "C:\Your\Path\to\ProjectFolder\trade_routes.exe" best
        ```

        If you chose the python files
        ```
        C:\Your\Path\To\Pythonw.exe C:\Your\Path\to\ProjectFolder\favorite_commodity.py
        C:\Your\Path\To\Pythonw.exe C:\Your\Path\to\ProjectFolder\material_traders.py
        C:\Your\Path\To\Pythonw.exe C:\Your\Path\to\ProjectFolder\trade_routes.py nearest
        C:\Your\Path\To\Pythonw.exe C:\Your\Path\to\ProjectFolder\trade_routes.py best
        ```

        Make sure to use **pythonw**.exe to run these scripts in the background to avoid pop-ups.

Customize the style and name of your multi-actions, and you're good to go. 

Feel free to customize your experience in the config.json file, src folder, or anywhere else.

Please use the "Issues" tab to report any problems or to request new features.


Thanks to:
- Dean Camera of https://python-elgato-streamdeck.readthedocs.io/en/stable/# for the Stream deck interface
- Bekena Studio for the creative commons Icons
- Inara.cz for providing an invaluble resource for our beloved game.
