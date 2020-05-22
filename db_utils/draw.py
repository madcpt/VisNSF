import xml.dom.minidom as xd
# import xml.etree.ElementTree as ET
# tree = ET.parse('country_data.xml')
# root = tree.getroot()

import os
import numpy as np

Files = []
for root, dirs, files, in os.walk('2020'):
    Files = files
length = len(Files)


# AwardTitle, AwardAmount, Investigator/First Name, Last Name, EmailAddress

Col = {}
for i in range(length):
    f = '2020/' + Files[i]
    doc = xd.parse(f)
    root = doc.documentElement
    AwardTitle = root.getElementsByTagName('AwardTitle')[0].firstChild.data
    Amount = root.getElementsByTagName('AwardAmount')[0].firstChild.data
    Amount = int(Amount)
    try:
        FName = root.getElementsByTagName('FirstName')[0].firstChild.data
        LName = root.getElementsByTagName('LastName')[0].firstChild.data
        name = FName + ' ' + LName
        email = root.getElementsByTagName('EmailAddress')[0].firstChild.data
        inv = (name,email)
    except Exception:
        continue
    else:
        if AwardTitle in Col:
            if inv in Col[AwardTitle]:
                continue
            else:
                Col[AwardTitle].append(inv)
        else:
            Col[AwardTitle] = [Amount,inv]







