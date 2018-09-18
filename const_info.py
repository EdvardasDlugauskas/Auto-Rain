from collections import namedtuple

File = namedtuple("File", ["name", "icon_path", "file_path"])

CONST_INFO = """
[Rainmeter]

"""

VALID_EXTENSIONS = ['.lnk', '.exe', '.url']

TEMPLATE = """
[{}]
Meter=Button
Y=23R
ButtonImage="{}"
ButtonCommand=!execute ["{}"]
"""

ICON_SIZE = 60, 60
