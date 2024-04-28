"""
Rename media files using timestamps defined in EXIF metadata.
Motivated by data export from iCloud.

Actually, you should consider exiftool (https://exiftool.org)
exiftool -r '-FileName<CreateDate' -d %Y%m%d_%H%M%S%%-c.%%e icloud_photos/*.JPEG
exiftool -r '-FileName<CreationDate' -d %Y%m%d_%H%M%S%%-c.%%e icloud_videos/*.MOV
"""

import os
import sys
from datetime import datetime, timedelta
from exiftool import ExifToolHelper

location = sys.argv[1]

if location.strip()[0] == "/":
    # absolute path, ook
    pass
else:
    pwd = os.path.dirname(os.path.abspath(__file__))
    location = os.path.join(pwd, location)

for name in os.listdir(location):
    if name == ".DS_Store":
        continue
    abs_name = os.path.join(location, name)
    print(name, abs_name)
    _, extension = name.rsplit('.', 1)

    with ExifToolHelper() as exif:
        tags = exif.get_tags([abs_name], tags=["CreationDate"])[0]
        print(tags)

#    Creation Date                   : 2016:11:19 06:27:18-08:00
    if "QuickTime:CreationDate" in tags:
        ctime_str = tags["QuickTime:CreationDate"]
        dt = ctime_str[:19]
        tz = ctime_str[19:22]
        dt = datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        dt += timedelta(hours=int(tz))
        new_name = datetime.strftime(dt, "%Y%m%d_%H%M%S") + "." + extension.upper()
        print(dt, tz, f"{new_name=}")
    else:
        print("NO EXIF")
