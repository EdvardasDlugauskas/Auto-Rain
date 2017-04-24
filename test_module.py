import icon_get
import unittest
import mainutils
import icon

test_ini = """
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


[video editor]
Meter=Button
Y=2R
ButtonImage="E:\Desktop\Test junk\video editor icon.png"
ButtonCommand=!execute ["E:\Desktop\Test junk\video editor.exe"]

[stackoverflow help]
Meter=Button
Y=2R
ButtonImage="E:\Desktop\Test junk\stackoverflow help icon.png"
ButtonCommand=!execute ["E:\Desktop\Test junk\stackoverflow help.exe"]

[movie maker]
Meter=Button
Y=2R
ButtonImage="E:\Desktop\Test junk\movie maker icon.png"
ButtonCommand=!execute ["E:\Desktop\Test junk\movie maker.exe"]

[Terraria]
Meter=Button
Y=2R
ButtonImage="E:\Desktop\Test junk\Terraria icon.png"
ButtonCommand=!execute ["E:\Desktop\Test junk\Terraria.url"]"""


class SmokeTests(unittest.TestCase):
    def test_get_urls(self):
        T = icon_get.get_urls
        assert T("minecraft")
        assert T("Dota 2")
        assert T("Photoshop")

    def test_sorting_by_ini(self):
        icon_names = ["Terraria", "movie maker", "video editor", "stackoverflow help", "new program"]
        icons = [icon.Icon(name=icon_name, image_save_path=".", app_path=".") for icon_name in icon_names]

        correctly_sorted_names = ["new program", "video editor", "stackoverflow help", "movie maker", "Terraria"]
        icons = mainutils.sort_by_ini(icons, ini_str=test_ini)

        for correct_name, actual_icon in zip(correctly_sorted_names, icons):
            assert actual_icon.name == correct_name, "Incorrectly sorted icons"
