from os import path, scandir
from collections import namedtuple
import icon_get

File = namedtuple("File", ["name", "icon_path", "file_path"])

CONST_INFO = """
[Rainmeter]
Author=tibneo.deviantart.com
Name=Mid Dock


------------------------------------------------------------------------

;Metadata added by RainBrowser
;http://rainmeter.net/RainCMS/?q=Rainmeter101_AnatomyOfASkin

[Metadata]
Name=
Config=
Description=
Instructions=
Version=
Tags=
License=
Variant=
Preview=

;End of added Metadata


;-----------------------------------------------------------------------
;            MEASURES                         MEASURES


[MeasurePower]
Measure=Plugin
Plugin=Plugins\PowerPlugin.dll
PowerState=PERCENT

[MeasureBin]
Measure=Plugin
Plugin=RecycleManager.dll
RecycleType=COUNT
Drives=ALL

[MeasureBin2]
Measure=Plugin
Plugin=RecycleManager.dll
RecycleType=SIZE
Drives=ALL

[BinAction]
Measure=Calc
Formula=MeasureBin
IfAboveAction=!execute [!RainmeterHideMeter IconEmpty][!RainmeterShowMeter IconFull]
IfAboveValue=0
IfEqualAction=!execute [!RainmeterHideMeter IconFull][!RainmeterShowMeter IconEmpty]
IfEqualValue=0


;---------------------------------------------------------------------------
;   APPLICATIONS

"""

APP_PATH = "." # 'C:\\Users\\Family\\Desktop\\Root\\Games' # Insert folder file
INI_PATH = "." # "C:\\Users\\Family\\Documents\\Rainmeter\\Skins\\Dektos by Tibneo\\Dock\\Left"
VALID_EXTENSIONS = ['.lnk', '.exe', '.url']

TEMPLATE = """
[{}]
Meter=Button
Y=2R
ButtonImage="{}"
ButtonCommand=!execute ["{}"]
"""



def get_valid_files():
    directory = scandir(APP_PATH)

    are_files = filter(lambda x: x.is_file(), directory)

    valid_files = []
    for file in are_files:
        name, extension = path.splitext(file.name)
        if extension not in VALID_EXTENSIONS:
            continue

        # Get icon
        try:
            icon_path = icon_get.get_icon(name)
        except Exception as error:
            icon_path = ""
            print(error)
            raise

        valid_files.append(File(name, icon_path, file.path))

    return valid_files

if __name__ == "__main__":
    valid_files = get_valid_files()
    with open(path.join(INI_PATH + "Left Dock.ini"), "w") as ini_file:
        ini_file.write(CONST_INFO)
        for file in valid_files:
            ini_file.write(TEMPLATE.format(file.name, file.icon_path, file.file_path))
