from collections import namedtuple

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

VALID_EXTENSIONS = ['.lnk', '.exe', '.url']

TEMPLATE = """
[{}]
Meter=Button
Y=2R
ButtonImage="{}"
ButtonCommand=!execute ["{}"]
"""

ICON_SIZE = 48, 48
