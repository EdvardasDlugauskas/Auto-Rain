from collections import namedtuple

File = namedtuple("File", ["name", "icon_path", "file_path"])

CONST_INFO = """
[Rainmeter]

"""

VALID_EXTENSIONS = ['.lnk', '.exe', '.url']

TEMPLATE = """
[{}]
Meter=Button
Y=2R
ButtonImage="{}"
ButtonCommand=!execute ["{}"]
"""

ICON_SIZE = 50, 50
